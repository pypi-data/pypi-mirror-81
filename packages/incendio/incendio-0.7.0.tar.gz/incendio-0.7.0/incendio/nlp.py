# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/05_nlp.ipynb (unless otherwise specified).

__all__ = ['tokenizer', 'tokenize', 'tokenize_many', 'Vocabulary', 'Embeddings', 'back_translate',
           'postprocess_embeddings', 'compress_embeddings']


# Cell
from collections import Counter
from functools import partial
import multiprocessing
import numpy as np
from sklearn.decomposition import PCA
import spacy
from textblob import TextBlob
import torch
from tqdm.auto import tqdm

from htools import save, load


# Cell
tokenizer = partial(spacy.load, name='en_core_web_sm',
                    disable=('ner', 'parser', 'tagger'))


# Cell
def tokenize(text, nlp):
    """Word tokenize a single string.

    Parameters
    ----------
    x: str
        A piece of text to tokenize.
    nlp: spacy tokenizer, e.g. spacy.lang.en.English
        By default, a spacy tokenizer with a small English vocabulary
        is used. NER, parsing, and tagging are disabled. Any spacy
        tokenzer can be passed in, but keep in mind other configurations
        may slow down this function dramatically.

    Returns
    -------
    list[str]: List of word tokens from a single input string.
    """
    return [tok.text for tok in nlp(text)]


# Cell
def tokenize_many(rows, nlp=None, chunk=1_000):
    """Word tokenize a sequence of strings using multiprocessing. The max
    number of available processes are used.

    Parameters
    ----------
    rows: Iterable[str]
        A sequence of strings to tokenize. This could be a list, a column of
        a DataFrame, etc.
    nlp: spacy tokenizer, e.g. spacy.lang.en.English
        By default, a spacy tokenizer with a small English vocabulary
        is used. NER, parsing, and tagging are disabled. Any spacy
        tokenzer can be passed in, but keep in mind other configurations
        may slow down this function dramatically.
    chunk: int
        This determines how many items to send to multiprocessing at a time.
        The default of 1,000 is usually fine, but if you have extremely
        long pieces of text and memory is limited, you can always decrease it.
        Very small chunk sizes may increase processing time. Note that larger
        values will generally cause the progress bar to update more choppily.

    Returns
    -------
    list[list[str]]: Each nested list of word tokens corresponds to one
    of the input strings.
    """
    tokenize_ = partial(tokenize, nlp=nlp or tokenizer())
    length = len(rows)
    with multiprocessing.Pool() as p:
        res = list(tqdm(p.imap(tokenize_, rows, chunksize=chunk),
                        total=length))
    return res


# Cell
class Vocabulary:

    def __init__(self, w2idx, w2vec=None, idx_misc=None, corpus_counts=None,
                 all_lower=True):
        """Defines a vocabulary object for NLP problems, allowing users to
        encode text with indices or embeddings.

        Parameters
        -----------
        w2idx: dict[str, int]
            Dictionary mapping words to their integer index in a vocabulary.
            The indices must allow for idx_misc to be added to the dictionary,
            so in the default case this should have a minimum index of 2. If
            a longer idx_misc is passed in, the minimum index would be larger.
        w2vec: dict[str, np.array]
            Dictionary mapping words to their embedding vectors stored as
            numpy arrays (optional).
        idx_misc: dict
            A dictionary mapping non-word tokens to indices. If none is passed
            in, a default version will be used with keys for unknown tokens
            and padding. A customized version might pass in additional tokens
            for repeated characters or all caps, for example.
        corpus_counts: collections.Counter
            Counter dict mapping words to their number of occurrences in a
            corpus (optional).
        all_lower: bool
            Specifies whether the data you've passed in (w2idx, w2vec, i2w) is
            all lowercase. Note that this will NOT change any of this data. If
            True, it simply lowercases user-input words when looking up their
            index or vector.
        """
        if not idx_misc:
            idx_misc = {'<PAD>': 0,
                        '<UNK>': 1}
        self.idx_misc = idx_misc
        # Check that space has been left for misc keys.
        assert len(idx_misc) == min(w2idx.values())

        # Core data structures.
        self.w2idx = {**self.idx_misc, **w2idx}
        self.i2w = [word for word, idx in sorted(self.w2idx.items(),
                                                 key=lambda x: x[1])]
        self.w2vec = w2vec or dict()

        # Miscellaneous other attributes.
        if w2vec:
            self.dim = len(w2vec[self[-1]])
        else:
            self.dim = 1
        self.corpus_counts = corpus_counts
        self.embedding_matrix = None
        self.w2vec['<UNK>'] = np.zeros(self.dim)
        self.all_lower = all_lower

    @classmethod
    def from_glove_file(cls, path, max_lines=float('inf'), idx_misc=None):
        """Create a new Vocabulary object by loading GloVe vectors from a text
        file. The embeddings are all lowercase so the user does not have the
        option to set the all_lower parameter.

        Parameters
        -----------
        path: str
            Path to file containing glove vectors.
        max_lines: int, float (optional)
            Loading the GloVe vectors can be slow, so for testing purposes
            it can be helpful to read in a subset. If no value is provided,
            all 400,000 lines in the file will be read in.
        idx_misc: dict
            Map non-standard tokens to indices. See constructor docstring.
        """
        w2idx = dict()
        w2vec = dict()
        misc_len = 2 if not idx_misc else len(idx_misc)

        with open(path, 'r') as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                word, *values = line.strip().split(' ')
                w2idx[word] = i + misc_len
                w2vec[word] = np.array(values, dtype=np.float)

        return cls(w2idx, w2vec, idx_misc)

    @classmethod
    def from_tokens(cls, tokens, idx_misc=None, all_lower=True):
        """Construct a Vocabulary object from a list or array of tokens.

        Parameters
        -----------
        tokens: list[str]
            The word-tokenized corpus.
        idx_misc: dict
            Map non-standard tokens to indices. See constructor docstring.
        all_lower: bool
            Specifies whether your tokens are all lowercase.

        Returns
        --------
        Vocabulary
        """
        misc_len = 2 if not idx_misc else len(idx_misc)
        counts = Counter(tokens)
        w2idx = {word: i for i, (word, freq)
                 in enumerate(counts.most_common(), misc_len)}
        return cls(w2idx, idx_misc=idx_misc, corpus_counts=counts,
                   all_lower=all_lower)

    @staticmethod
    def from_pickle(path):
        """Load a previously saved Vocabulary object.

        Parameters
        -----------
        path: str
            Location of pickled Vocabulary file.

        Returns
        --------
        Vocabulary
        """
        return load(path)

    def save(self, path, verbose=True):
        """Pickle Vocabulary object for later use. We can then quickly load
        the object using torch.load(path), which can be much faster than
        re-computing everything when the vocab size becomes large.

        Parameters
        -----------
        path: str
            Where to save the output file.
        verbose: bool
            If True, print message showing where the object was saved to.
        """
        save(self, path, verbose)

    def filter_tokens(self, tokens, max_words=None, min_freq=0, inplace=False,
                      recompute=False):
        """Filter your vocabulary by specifying a max number of words or a min
        frequency in the corpus. When done in place, this also sorts vocab by
        frequency with more common words coming first (after idx_misc).

        Parameters
        -----------
        tokens: list[str]
            A tokenized list of words in the corpus (must be all lowercase
            when self.all_lower=True, such as when using GloVe vectors). There
            is no need to hold out test data here since we are not using
            labels.
        max_words: int (optional)
            Provides an upper threshold for the number of words in the
            vocabulary. If no value is passed in, no maximum limit will be
            enforced.
        min_freq: int (optional)
            Provides a lower threshold for the number of times a word must
            appear in the corpus to remain in the vocabulary. If no value is
            passed in, no minimum limit will be enforced.

            Note that we can specify values for both max_words and min_freq
            if desired. If no values are passed in for either, no pruning of
            the vocabulary will be performed.
        inplace: bool
            If True, will change the object's attributes
            (w2idx, w2vec, and i2w) to reflect the newly filtered vocabulary.
            If False, will not change the object, but will simply compute word
            counts and return what the new w2idx would be. This can be helpful
            for experimentation, as we may want to try out multiple values of
            min_freq to decide how many words to keep. After the first call,
            the attribute corpus_counts can also be examined to help determine
            the desired vocab size.
        recompute: bool
            If True, will calculate word counts from the given tokens. If
            False (the default), this will use existing counts if there are
            any.

            The idea is that if we call this method, then realize we want
            to change the corpus, we should calculate new word counts.
            However, if we are simply calling this method multiple times on
            the same corpus while deciding on the exact vocab size we want,
            we should not recompute the word counts.

        Returns
        --------
        dict or None: When called inplace, nothing is returned. When not
        inplace,
        """
        misc_len = len(self.idx_misc)
        if recompute or not self.corpus_counts:
            self.corpus_counts = Counter(tokens)
        filtered = {word: i for i, (word, freq)
                    in enumerate(self.corpus_counts.most_common(max_words),
                                 misc_len)
                    if freq >= min_freq}
        filtered = {**self.idx_misc, **filtered}

        if inplace:
            # Relies on python3.7 dicts retaining insertion order.
            self.i2w = list(filtered.keys())
            self.w2idx = filtered
            self.w2vec = {word: self.vector(word) for word in filtered}
        else:
            return filtered

    def build_embedding_matrix(self, inplace=False):
        """Create a 2D numpy array of embedding vectors where row[i]
        corresponds to word i in the vocabulary. This can be used to
        initialize weights in the model's embedding layer.

        Parameters
        -----------
        inplace: bool
            If True, will store the output in the object's embedding_matrix
            attribute. If False (default behavior), will simply return the
            matrix without storing it as part of the object. In the
            recommended case where inplace==False, we can store the output
            in another variable which we can use to initialize the weights in
            Torch, then delete the object and free up memory using
            gc.collect().
        """
        emb = np.zeros((len(self), self.dim))
        for i, word in enumerate(self):
            emb[i] = self.vector(word)

        if inplace:
            self.embedding_matrix = emb
        else:
            return emb

    def idx(self, word):
        """This will map a word (str) to its index (int) in the vocabulary.
        If a string is passed in and the word is not present, the index
        corresponding to the <UNK> token is returned.

        Parameters
        -----------
        word: str
            A word that needs to be mapped to an integer index.

        Returns
        --------
        int: The index of the given word in the vocabulary.

        Examples
        ---------
        >>> vocab.idx('the')
        2
        """
        if self.all_lower and word not in self.idx_misc:
            word = word.lower()
        return self.w2idx.get(word, self.w2idx['<UNK>'])

    def vector(self, word):
        """This maps a word to its corresponding embedding vector. If not
        contained in the vocab, a vector of zeros will be returned.

        Parameters
        -----------
        word: str
            A word that needs to be mapped to a vector.

        Returns
        --------
        np.array
        """
        if self.all_lower and word not in self.idx_misc:
            word = word.lower()
        return self.w2vec.get(word, self.w2vec['<UNK>'])

    def encode(self, text, nlp, max_len, pad_end=True, trim_start=True):
        """Encode text so that each token is replaced by its integer index in
        the vocab.

        Parameters
        -----------
        text: str
            Raw text to be encoded.
        nlp: spacy.lang.en.English
            Spacy tokenizer. Typically want to disable 'parser', 'tagger', and
            'ner' as they aren't used here and slow down the encoding process.
        max_len: int
            Length of output encoding. If text is shorter, it will be padded
            to fit the specified length. If text is longer, it will be
            trimmed.
        pad_end: bool
            If True, add padding to the end of short sentences. If False, pad
            the start of these sentences.
        trim_start: bool
            If True, trim off the start of sentences that are too long. If
            False, trim off the end.

        Returns
        --------
        np.array[int]: Array of length max_len containing integer indices
            corresponding to the words passed in.
        """
        output = np.ones(max_len) * self.idx('<PAD>')
        encoded = [self.idx(tok.text) for tok in nlp(text)]

        # Trim sentence in case it's longer than max_len.
        if len(encoded) > max_len:
            if trim_start:
                encoded = encoded[len(encoded) - max_len:]
            else:
                encoded = encoded[:max_len]

        # Replace zeros at start or end, depending on choice of pad_end.
        if pad_end:
            output[:len(encoded)] = encoded
        else:
            output[max_len-len(encoded):] = encoded
        return output.astype(int)

    def decode(self, idx):
        """Convert a list of indices to a string of words/tokens.

        Parameters
        -----------
        idx: list[int]
            A list of integers indexing into the vocabulary. This will often
            be the output of the encode() method.

        Returns
        --------
        list[str]: A list of words/tokens reconstructed by indexing into the
            vocabulary.
        """
        return [self[i] for i in idx]

    def __getitem__(self, i):
        """This will map an index (int) to a word (str).

        Parameters
        -----------
        i: int
            Integer index for a word.

        Returns
        --------
        str: Word corresponding to the given index.

        Examples
        ---------
        >>> vocab = Vocabulary(w2idx, w2vec)
        >>> vocab[1]
        '<UNK>'
        """
        return self.i2w[i]

    def __len__(self):
        """Number of words in vocabulary."""
        return len(self.w2idx)

    def __iter__(self):
        for word in self.w2idx.keys():
            yield word

    def __contains__(self, word):
        return word in self.w2idx.keys()

    def __eq__(self, obj):
        if not isinstance(obj, Vocabulary):
            return False

        ignore = {'w2vec', 'embedding_matrix'}
        attrs = [k for k, v in hdir(vocab).items()
                 if v == 'attribute' and k not in ignore]
        return all([getattr(self, attr) == getattr(obj, attr)
                    for attr in attrs])

    def __repr__(self):
        msg = f'Vocabulary({len(self)} words'
        if self.dim > 1:
            msg += f', {self.dim}-D embeddings'
        return msg + ')'


# Cell
class Embeddings:
    """Embeddings object. Lets us easily map word to index, index to
    word, and word to vector. We can use this to find similar words,
    build analogies, or get 2D representations for cdting.
    """

    def __init__(self, mat, w2i, mat_2d=None):
        """
        Parameters
        ----------
        mat: str
            Numpy array of embeddings where row i corresponds to ID i
            in w2i.
        w2i: dict[str, int]
            Dictionary mapping word to its index in the vocabulary.
        mat_2d: np.array
            Matrix output of PCA after compressing mat to vectors of length 2.
            If None, it will be computed from mat and cached.
        """
        self.mat = mat
        self.w2i = w2i
        self.i2w = [w for w, i in sorted(self.w2i.items(), key=lambda x: x[1])]
        self.mat_2d = mat_2d or PCA(n_components=2).fit_transform(self.mat)
        self.n_embeddings, self.dim = self.mat.shape

    @classmethod
    def from_text_file(cls, path, max_words=float('inf'), print_freq=10_000):
        """Create a new Embeddings object from a raw text file using the
        GloVe format (each row contains a word and its embedding as
        space-separated floats).

        Parameters
        ----------
        path: str
            Location of csv file containing GloVe vectors.
        max_words: int, float
            Set maximum number of words to read in from file. This can be used
            during development to reduce wait times when loading data.
        Returns
        -------
        Embeddings: Newly instantiated object.
        """
        w2i = dict()
        mat = []
        with open(path, 'r') as f:
            for i, line in enumerate(f):
                # Faster testing
                if i >= max_words: break
                word, *nums = line.strip().split()
                w2i[word] = i
                mat.append(np.array(nums, dtype=float))
                if i % print_freq == 0: print(i, word)
        return cls(np.array(mat), w2i)

    @classmethod
    def from_pickle(cls, path):
        """If an Embeddings object previously saved its data in a pickle file,
        loading it that way can avoid repeated computation.

        Parameters
        ----------
        path: str
            Location of pickle file.

        Returns
        -------
        Embeddings: Newly instantiated object using the data that was stored in
            the pickle file.
        """
        return cls(**load(path))

    def save(self, path, verbose=True):
        """Save data to a compressed pickle file. This reduces the amount of
        space needed for storage (the csv is much larger) and can let us
        avoid running PCA and building the embedding matrix again.

        Parameters
        ----------
        path: str
            Path that object will be saved to.
        verbose

        Returns
        -------
        None
        """
        data = dict(mat=self.mat,
                    w2i=self.w2i,
                    mat_2d=self.mat_2d)
        save(data, path, verbose=verbose)

    def vec(self, word):
        """Look up the embedding for a given word. Return None if not found.

        Parameters
        ----------
        word: str
            Input word to look up embedding for.

        Returns
        -------
        np.array: Embedding corresponding to the input word. If word not in
            vocab, return None.
        """
        idx = self[word]
        if idx is not None:
            return self.mat[idx]

    def vec_2d(self, word):
        """Look up the compressed embedding for a word (PCA was used to shrink
        dimensionality to 2). Return None if the word is not present in vocab.

        Parameters
        ----------
        word: str
            Input work to look up.

        Returns
        -------
        np.array: Compressed embedding of length 2. None if not found.
        """
        idx = self[word]
        if idx is not None:
            return self.mat_2d[idx]

    def _distances(self, vec, distance='cosine'):
        """Find distance from an input vector to every other vector in the
        embedding matrix.

        Parameters
        ----------
        vec: np.array
            Vector for the input word.
        distance: str
            Specifies what distance metric to use for calculations.
            One of ('euclidean', 'manhattan', 'cosine'). In a high dimensional
            space, cosine is often a good choice.

        Returns
        -------
        np.array: The i'th value corresponds to the distance to word i in the
            vocabulary.
        """
        if distance == 'euclidean':
            dists = self.norm(self.mat - vec)
        elif distance == 'cosine':
            dists = self.cosine_distance(vec, self.mat)
        elif distance == 'manhattan':
            dists = self.manhattan_distance(vec, self.mat)
        return dists

    def nearest_neighbors(self, word, n=5, distance='cosine', digits=3):
        """Find the most similar words to a given word. This wrapper to
        allows the user to pass in a word. To pass in a vector, use
        _nearest_neighbors().

        Parameters
        ----------
        word: str
            A word that must be in the vocabulary.
        n: int
            Number of neighbors to return.
        distance: str
            Distance method to use when computing nearest neighbors. One of
            ('euclidean', 'manhattan', 'cosine').
        digits: int
            Digits to round output distances to.

        Returns
        -------
        dict[str, float]: Dictionary mapping word to distance.
        """
        # Error handling for words not in vocab.
        if word not in self:
            return None
        return self._nearest_neighbors(self.vec(word), n, distance, digits)

    def _nearest_neighbors(self, vec, n=5, distance='cosine', digits=3,
                           skip_first=True):
        """Internal function behind nearest_neighbors(). This can be used if
        we want to pass in a vector instead of a word. For more details, see
        the wrapper method.

        Parameters
        ----------
        vec: np.array
        n: int
        distance: str
        digits: int
        skip_first: bool
            If True, the nearest result will be sliced off (this is desirable
            when searching for a word's nearest neighbors, where we don't want
            to return the word itself). When finding analogies or performing
            embedding arithmetic, however, we likely don't want to slice off
            the first result.

        Returns
        -------
        dict[str, float]: Dictionary mapping word to distance.
        """
        dists = self._distances(vec, distance)
        idx = np.argsort(dists)[slice(skip_first, skip_first+n)]
        return {self.i2w[i]: round(dists[i], digits) for i in idx}

    def analogy(self, a, b, c, n=5, **kwargs):
        """Fill in the analogy: A is to B as C is to ___. Note that we always
        treat A and B as valid candidates to fill in the blank. C is
        only considered as a candidate in the trivial case where A=B, in which
        case C should be the first choice.
        Parameters
        ----------
        a: str
            First word in analogy.
        b: str
            Second word in analogy.
        c: str
            Third word in analogy.
        n: int
            Number of candidates to return. Note that we specify this
            separately fro kwargs since we need to alter its value before
            passing it to _nearest_neighbors(). This will allow us to remove
            the word c as a candidate if it is returned.
        kwargs: distance (str), digits (int)
            See _nearest_neighbors for details.
        Returns
        -------
        list[str]: Best candidates to complete the analogy in descending order
            of likelihood.
        """
        # If any words missing from vocab, arithmetic w/ None will throw error.
        try:
            vec = self.vec(b) - self.vec(a) + self.vec(c)
        except TypeError:
            return None

        # Except for trivial edge case, return 1 extra value in case neighbors
        # includes c, which will be removed in these situations.
        a, b, c = a.lower(), b.lower(), c.lower()
        trivial = (a == b)
        neighbors = self._nearest_neighbors(vec,
                                            n=n+1-trivial,
                                            skip_first=False,
                                            **kwargs)
        if not trivial and c in neighbors:
            neighbors.pop(c)

        # Relies on dicts being ordered in python >= 3.6.
        return list(neighbors)[:n]

    def cbow(self, *args):
        """Wrapper to _cbow() that allows us to pass in strings instead of
        vectors.

        Parameters
        ----------
        args: str
            Multiple words to average over.

        Returns
        -------
        np.array: Average of all input vectors. This will have the same
            embedding dimension as each input.
        """
        vecs = [arg for arg in map(self.vec, args) if arg is not None]
        if vecs:
            return self._cbow(*vecs)

    def _cbow(self, *args):
        """Internal helper for cbow(). Can also use this directly if you want
        to pass in vectors instead of words.

        Parameters
        ----------
        args: np.array
            Word vectors to average.

        Returns
        -------
        np.array: Average of all input vectors. This will have the same
            embedding dimension as each input.
        """
        return np.mean(args, axis=0)

    def cbow_neighbors(self, *args, n=5, **kwargs):
        """Wrapper to cbow(). This lets us pass in words, compute their
        average embedding, then return the words nearest this embedding. The
        input words are not considered to be candidates for neighbors (e.g. if
        you input the words 'happy' and 'cheerful', the neighbors returned will
        not include those words even if they are the closest to the mean
        embedding). The idea here is to find additional words that may be
        similar to the group you've passed in.

        Parameters
        ----------
        args: str
            Input words to average over.
        n: int
            Number of neighbors to return.
        kwargs: distance (str), digits (int)
            See _nearest_neighbors() for details.

        Returns
        -------
        dict[str, float]: Dictionary mapping word to distance from the average
            of the input words' vectors.
        """
        vec_avg = self.cbow(*args)
        if vec_avg is None:
            return
        neighbors = self._nearest_neighbors(vec_avg, n=len(args)+n,
                                            skip_first=False, **kwargs)

        # Lowercase to help remove duplicates.
        args = set(arg.lower() for arg in args)
        return {word: neighbors[word] for word in
                [n for n in neighbors if n not in args][:n]}

    @staticmethod
    def norm(vec):
        """Compute L2 norm of a vector. Euclidean distance between two vectors
        can be found by the operation norm(vec1 - vec2).

        Parameters
        ----------
        vec: np.array
            Input vector.

        Returns
        -------
        float: L2 norm of input vector.
        """
        return np.sqrt(np.sum(vec ** 2, axis=-1))

    @staticmethod
    def manhattan_distance(vec1, vec2):
        """Compute L1 distance between two vectors.

        Parameters
        ----------
        vec1: np.array
        vec2: np.array

        Returns
        -------
        float or np.array: Manhattan distance between vec1 and vec2. If two
            vectors are passed in, the output will be a single number. When
            computing distances between a vector and a matrix, the output
            will be a vector (np.array).
        """
        return np.sum(abs(vec1 - vec2), axis=-1)

    def cosine_distance(self, vec1, vec2):
        """Compute cosine distance between two vectors.

        Parameters
        ----------
        vec1: np.array
        vec2: np.array

        Returns
        -------
        float or np.array: Cosine distance between vec1 and vec2. If two
            vectors are passed in, the output will be a single number. When
            computing distances between a vector and a matrix, the output
            will be a vector (np.array).
        """
        return 1 - (np.sum(vec1 * vec2, axis=-1) /
                    (self.norm(vec1) * self.norm(vec2)))

    def __getitem__(self, word):
        return self.w2i.get(word.lower())

    def __len__(self):
        return self.n_embeddings

    def __contains__(self, word):
        return word.lower() in self.w2i

    def __iter__(self):
        """Yields words in vocabulary."""
        yield from self.w2i.keys()

    def __repr__(self):
        return f'Embeddings(len={len(self)}, dim={self.dim})'


# Cell
def back_translate(text, to, from_lang='en'):
    """
    Parameters
    ----------

    Returns
    -------
    str: Same language and basically the same content as the original text,
        but usually with slightly altered grammar, sentence structure, and/or
        vocabulary.
    """
    return str(
        TextBlob(text)\
        .translate(to=to)\
        .translate(from_lang=to, to=from_lang)
    )


# Cell
def postprocess_embeddings(emb, d=None):
    """Implements the algorithm from the paper:

    All-But-The-Top: Simple and Effective Post-Processing
    for Word Representations (https://arxiv.org/pdf/1702.01417.pdf)

    There are three steps:
    1. Compute the mean embedding and subtract this from the
    original embedding matrix.
    2. Perform PCA and extract the top d components.
    3. Eliminate the principal components from the mean-adjusted
    embeddings.

    Parameters
    ----------
    emb: np.array
        Embedding matrix of size (vocab_size, embedding_length).
    d: int
        Number of components to use in PCA. Defaults to
        embedding_length/100 as recommended by the paper.
    """
    d = d or emb.shape[1] // 100
    emb_adj = emb - emb.mean(0)
    u = PCA(d).fit(emb_adj).components_
    return emb_adj - emb@u.T@u


# Cell
def compress_embeddings(emb, new_dim, d=None):
    """Reduce embedding dimension as described in the paper:

    Simple and Effective Dimensionality Reduction for Word Embeddings
    (https://lld-workshop.github.io/2017/papers/LLD_2017_paper_34.pdf)

    Parameters
    ----------
    emb: np.array
        Embedding matrix of size (vocab_size, embedding_length).
    d: int
        Number of components to use in the post-processing
        method described here: https://arxiv.org/pdf/1702.01417.pdf
        Defaults to embedding_length/100 as recommended by the paper.

    Returns
    -------
    np.array: Compressed embedding matrix of shape (vocab_size, new_dim).
    """
    emb = postprocess_embeddings(emb, d)
    emb = PCA(new_dim).fit_transform(emb)
    return postprocess_embeddings(emb, d)