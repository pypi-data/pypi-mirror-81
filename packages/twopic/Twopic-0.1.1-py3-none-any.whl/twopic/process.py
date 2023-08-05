from collections import Counter
from itertools import dropwhile
from pathlib import Path
from typing import List

import nltk
import numpy as np
import pandas as pd
import tensorflow_hub as hub
from absl import logging
from nltk.corpus import stopwords
from pandas import DataFrame, Series
from tqdm import tqdm
from twittenizer import Tokenizer

from model import set_local_model

# Reduce logging output.
logging.set_verbosity(logging.ERROR)

# *###########################
# *--------- CLASSES ---------
# *###########################


class Embedding:
    def __init__(self, vector):
        self.vector: np.ndarray = vector

    @property
    def size(self):
        print(self.vector.size)


class Model:
    """
    Language model used to generate the vector representation of the words.

    >>> model = Model()
    """

    def __init__(
        self,
        model_url,
        model_root=r"C:\Users\ju\Code\Twopic\models",
    ):
        model = set_local_model(model_url, model_root)
        self.model = hub.load(model)

    def word_similarity(self, string1: str, string2: str):
        """Retourne le produit vectoriel"""
        words = [string1, string2]
        embed1, embed2 = self.model(words)
        corr = np.inner(embed1, embed2)
        print(corr)

    def set_embedding_vector(self, word: str) -> Embedding:
        vector = self.model([word]).numpy()[0]
        return Embedding(vector)

    def _model_url(self, url: str) -> Path:
        url: Path = Path(url)
        return url

    def _download_path(self, url: Path) -> Path:
        pass


class Dataset:
    """
    Dataframe with preprocessing methods.

    >>> target = Dataset("../../data/english.csv",["tweet_id", "text", "source", "type", "label"])
    >>> target.preprocess_dataset(drop=["tweet_id", "source", "type", "label"])

    >>> source = Dataset("../../data/words.csv", ["words", "label", "labels"])
    >>> source.preprocess_dataset(drop=["label"],stopwords=False, tokenize=False,lower=False, strip_labels=True)
    >>> source.dataset.dropna(inplace=True)
    """

    def __init__(self, path, columns_names, is_vocab=False):
        self.dataset: DataFrame = self._set_dataset(path, columns_names)

        self.is_preprocessed = False

    def _set_dataset(self, path: str, columns_names: List[str]):
        """Load the dataset"""
        _path = Path(path)

        if _path.suffix == ".csv":
            return pd.read_csv(_path, header=0, names=columns_names, encoding="utf-8")
        elif _path.suffix == ".tsv":
            return pd.read_csv(
                _path,
                sep="\t",
                header=0,
                names=columns_names,
                encoding="utf-8",
            )

    # TODO Replace with callback?
    def preprocess_dataset(
        self,
        stemmer=False,
        drop=["tweet_id", "source", "type", "informativeness"],
        stopwords=True,
        tokenize=True,
        lower=True,
        strip_labels=False,
    ):
        """
        Preprocess the dataset:
            - Drop specified columns
            - Stem the words
            - Remove stopwords
            - Tokenize the dataset
        """
        self.is_preprocessed = True
        if drop:
            self.dataset.drop(drop, axis=1, inplace=True)
        if lower:
            self.dataset["text"] = self.dataset["text"].str.lower()
        if stemmer:
            from nltk.stem.snowball import SnowballStemmer

            stemmer = SnowballStemmer("english")
            self.dataset["text"] = self.dataset["text"].apply(
                lambda x: " ".join([stemmer.stem(word) for word in x.split()])
            )
        if stopwords:
            self.dataset["text"] = self.dataset["text"].apply(
                lambda x: " ".join(
                    [word for word in x.split() if word not in (get_stopwords())]
                )
            )
        if tokenize:
            tk = Tokenizer()
            self.dataset["text"] = self.dataset.apply(
                lambda row: tk.tokenize(row["text"]), axis=1
            )
        if strip_labels:
            self.dataset.labels = self.dataset.labels.str.strip()


class Vocab:
    """
    Un vocab est constitue d'un vocabulaire de mots, associes (ou non) a un label
    Les labels peuvent etre encodes
    On peut generer le vecteur representatif d'un mot

    >>> vocab_target = Vocab(target, "text", is_tweets=True, thresh=5)
    >>> vocab_source = Vocab(source)
    """

    def __init__(
        self,
        dataset,
        from_column: str = "",
        from_dataframe=False,
        is_tweets=False,
        thresh: int = 0,
    ):
        if not from_dataframe:
            self.table = self._set_vocab(dataset, from_column, is_tweets, thresh)
        else:
            self.table = dataset
        self.initial_words_count: int = self.table.words.count()

    def __add__(self, vocab_to_add):
        vocab_intermediate = self.table.append(vocab_to_add.table, ignore_index=True)
        vocab_intermediate.drop_duplicates(
            subset="words", inplace=True, ignore_index=True
        )
        return Vocab(vocab_intermediate, from_dataframe=True)

    def _set_vocab(self, dataset, from_column, is_tweets=False, thresh: int = 0):
        """
        Charge le vocabulaire d'apres un dataset.
        Si le dataset est constitue de tweets, scinde les tweets en mots uniques et
        charge le dans le vocab.
        Sinon charge directement dans le vocab.
        """
        if is_tweets:
            if dataset.is_preprocessed:
                # Si le contenu de text est une liste de mots
                vocab_count = Counter(
                    [word for tweet in dataset.dataset[from_column] for word in tweet]
                )
            else:
                # Si le contenu est une str contenant les mots
                vocab_count = Counter(
                    [
                        word
                        for tweet in dataset.dataset[from_column]
                        for word in tweet.split(" ")
                    ]
                )

            if thresh:
                # Frequence minimale pour qu'un mot soit comptabilise
                vocab_count_thresh = Counter(
                    {
                        k: vocab_count
                        for k, vocab_count in vocab_count.items()
                        if vocab_count >= thresh
                    }
                )
                return pd.DataFrame(
                    {
                        "words": list(set(vocab_count_thresh.elements())),
                        "labels": "none",
                    }
                )
            else:
                return pd.DataFrame(
                    {"words": list(set(vocab_count.elements())), "labels": "none"}
                )
        else:
            new_dataset = dataset.dataset
            return new_dataset

    def encode_labels(self, source_column="labels", new_column="labels_encoded"):
        if self.table["labels"].size == 0:
            print("Can't encode labels because they don't exist")
        else:
            from sklearn.preprocessing import LabelEncoder

            self.table[source_column] = self.table[source_column].str.strip()
            self.table[source_column] = self.table[source_column].fillna("none")

            le = LabelEncoder()
            self.table[new_column] = le.fit_transform(
                self.table[source_column].astype(str)
            )
            self.table[new_column] = self.table[new_column].astype("int8")
            self.label_encoder = le

    def generate_embedding(self, model: Model):
        for index, word in tqdm(self.table.iterrows()):
            self.table.at[index, "embeddings"] = model.set_embedding_vector(
                word["words"]
            )

    def get_word_index(self, word: str) -> int:
        return int(self.table.words[self.table.words == word].index[0])

    def get_word_vector(self, word: str) -> np.array:
        index = self.get_word_index(word)
        try:
            return self.table.embeddings[index].vector
        except AttributeError:
            raise AttributeError(
                "Word vectors not generated, use generate_embedding() before."
            )

    @property
    def words(self):
        return self.table.words.values

    @property
    def number_words(self):
        return len(self.table.labels)

    @property
    def word_vectors(self):
        vectors: List[np.array] = []
        try:
            word_vector_series = self.table.embeddings
        except AttributeError:
            raise AttributeError(
                "Word vectors not generated, use generate_embedding() before."
            )
        for vector in tqdm(word_vector_series):
            vectors.append(vector.vector)
        return vectors


class Correlation:
    def __init__(self, vocab_source: Vocab, vocab_target: Vocab, model: Model):
        self.model = model
        self.vocab = self._set_vocab(vocab_source, vocab_target)
        self.corr = self._set_corr()

    def _set_corr(self) -> DataFrame:
        word_vectors_map = {}
        for _, word, _, word_vector in self.vocab.table.itertuples():
            word_vectors_map[word] = word_vector.vector
        word_vectors_df = pd.DataFrame(word_vectors_map)
        return word_vectors_df.corr()

    def _set_vocab(self, vocab_source: Vocab, vocab_target: Vocab) -> Vocab:
        full_vocab = vocab_source + vocab_target
        full_vocab.generate_embedding(self.model)
        return full_vocab

    def most_similar_radius(self, word: str, radius: float = 0.55) -> Series:
        words_inside_radius = self.corr[word][self.corr[word] > radius]
        words_inside_radius_sorted = words_inside_radius.sort_values(ascending=False)
        return words_inside_radius_sorted[1:]


# *#############################
# *--------- FUNCTIONS ---------
# *#############################


def get_stopwords():
    try:
        return stopwords.words("english")
    except LookupError:
        nltk.download("stopwords")
        return stopwords.words("english")


def get_unique_words(dataset: pd.DataFrame) -> List[List[str]]:
    vocab_count: Counter = Counter()
    vocab_count.update([word for tweet in dataset["text"] for word in tweet])

    for key, _ in dropwhile(
        lambda key_count: key_count[1] >= 5, vocab_count.most_common()
    ):
        del vocab_count[key]

    vocab: List[List[str]] = [[word] for word in set(vocab_count.elements())]

    return vocab


if __name__ == "__main__":
    model = Model()
    target = Dataset(
        "data/english.csv", ["tweet_id", "text", "source", "type", "label"]
    )
    target.preprocess_dataset(drop=["tweet_id", "source", "type", "label"])
    source = Dataset("data/words.csv", ["words", "label", "labels"])
    source.preprocess_dataset(
        drop=["label"], stopwords=False, tokenize=False, lower=False, strip_labels=True
    )
    source.dataset.dropna(inplace=True)
    vocab_target = Vocab(target, "text", is_tweets=True, thresh=5)
    vocab_source = Vocab(source)
    corr = Correlation(vocab_source, vocab_target, model)
