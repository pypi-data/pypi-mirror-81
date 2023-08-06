from DataStructure.Cache.CacheLinkedList cimport CacheLinkedList


cdef class LRUCache(object):

    cdef int __cacheSize
    cdef dict __map
    cdef CacheLinkedList __cache

    cpdef bint contains(self, key: object)
    cpdef object get(self, key: object)
    cpdef add(self, key: object, data: object)