from scipy.signal import welch, filtfilt
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import butter, hilbert
import networkx as nx
from time import time
import numpy as np
import pylab as pl
import igraph
import os

def filter_matrix(A, low, high):
    """
    return a binary matrix with elements that be between low and high values

    :param A: [2d np.array] input 2d array
    :param low: [float] lower value
    :param high: [float] higher value
    """

    n = A.shape[0]
    assert (len(A.shape) == 2)
    filt = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(n):
            if (A[i][j] > low) and (A[i][j] < high):
                filt[i][j] = 1

    return filt

def find_intersection_matrices(A, B):

    """
    find the overlap of two matrices

    :param A: [2d integer np.array]
    :param B: [2d integer np.array]
    :return: [2d integer np.array] the overlap matrix with binary values
    """
    assert (np.asarray(A).shape == np.asarray(B).shape)
    assert(isinstance(A[0][0].item(), int))

    row, col = A.shape
    C = np.zeros((row, col), dtype=int)

    for i in range(row):
        for j in range(col):

            if (A[i][j] == B[i][j]) and (A[i][j] != 0):
                C[i][j] = 1

    return C


def hellinger(p, q):

    """
    In probability and statistics, the Hellinger distance is used to quantify the similarity between two probability distributions.

    :param p: [array] positive distribution
    :param q: [array] positive distribution
    :return: [float] distance between distributions

    -  example :
    
    >>> def distribution(N, dim=1, loc=0, scale=1, normal=False):
    >>>    dist = []
    >>>    for i in range(N):
    >>>        dist.append(np.random.normal(loc=loc, scale=scale, size=dim))
    >>>    if normal:
    >>>        return np.asarray(dist) / N
    >>>    return np.asarray(dist)
    >>> 
    >>> N = 100
    >>> dim = 2
    >>> A = distribution(N, dim=2, loc=20, scale=1.0, normal=1)
    >>> B = distribution(N, dim=2, loc=20, scale=5.5, normal=1)
    >>> C = distribution(N, dim=2, loc=45, scale=1.0, normal=1)
    >>> print("hellinger distance between A, B is ", hellinger3(np.abs(A), np.abs(B)))
    >>> print("hellinger distance between A, C is ", hellinger3(np.abs(A), np.abs(C)))
    >>> print("hellinger distance between B, C is ", hellinger3(np.abs(B), np.abs(C)))
    >>> plt.scatter([x for x, _ in A], [y for _, y in A], label='distribution A')
    >>> plt.scatter([x for x, _ in B], [y for _, y in B], label='distribution B')
    >>> plt.scatter([x for x, _ in C], [y for _, y in C], label='distribution C')
    >>> plt.legend()
    >>> plt.show()

    """
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / np.sqrt(2)


def distances(A, B, metric="euclidean"):
    """
    distance between distr
    it is specially used to compare the distribution of e.g. correlation matrices with a referenced distribution.

    :param A: [np.array] input distribution
    :param B: [np.array] input distribution
    :param metric: [str] or function, optional, The distance metric to use. The distance function can be ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, ‘euclidean’, ‘hamming’, ‘jaccard’, ‘jensenshannon’, ‘kulsinski’, ‘mahalanobis’, ‘matching’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’.
    :return: [float] distance

        
    >>> A = np.random.normal(loc=0, scale=1, size=100)
    >>> B = np.random.normal(loc=5, scale=2.5, size=100)
    >>> distances(A, B)

    """
    from scipy.spatial.distance import pdist

    assert (len(A) == len(B)), "two array must have the same length"
    
    return pdist(np.vstack((A, B)), metric=metric)


