#!python
#cython: language_level=3

cimport numpy as np


cdef str __version__ = "0.0.3"


cdef class AudioClassifier:
    cdef list _classes, _cache_x, _cache_y

    cdef public int alpha

    cpdef void fit(self, np.ndarray X, np.ndarray y) except *
    cpdef np.ndarray predict(self, np.ndarray X)