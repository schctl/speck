import os

from speck.cache import BufferedCacheManager, FileCacheManager

# Utils --------------------

def __test_dump_read(manager):
    manager.dump('x-test-1', [1, 2, 3, 4])
    manager.dump('x-test-2', [2, 4, 6, 8])

    assert manager.read('x-test-1') == [1, 2, 3, 4]
    assert manager.read('x-test-2') == [2, 4, 6, 8]

def __test_cleanup(manager):
    manager.dump('x-test-1', [1, 2, 3, 4])
    manager.dump('x-test-2', [2, 4, 6, 8])

    manager.cleanup('x-test-*')
    assert list(manager.find_all()) == []

# Tests --------------------

def test_buffered():
    cache = BufferedCacheManager()
    __test_dump_read(cache)
    __test_cleanup(cache)

def test_file():
    cache = FileCacheManager('.test-cache')
    __test_dump_read(cache)
    __test_cleanup(cache)

# --------------------------

if __name__ == '__main__':
    test_buffered()
    test_file()
