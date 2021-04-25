from speck.cache import BufferedCacheManager, FileCacheManager

# Utils --------------------

def __test_dump_read(manager):
    manager.dump('x-test-1', [1, 2, 3, 4])
    manager.dump('x-test-2', "some-str")

    assert manager.read('x-test-1') == [1, 2, 3, 4]
    assert manager.read('x-test-2') == "some-str"

def __test_cleanup(manager):
    manager.dump('x-test-1', [1, 2, 3, 4])
    manager.dump('x-test-2', "some-str")

    manager.cleanup('x-test-*')
    assert list(manager.find_all()) == []

def __test_duplicate(manager):
    manager.dump('x-test-1', [1, 2, 3, 4])
    manager.dump('x-test-1', "some-str")

    assert manager.read('x-test-1') == "some-str"

def __test_all(manager):
    __test_dump_read(manager)
    __test_cleanup(manager)
    __test_duplicate(manager)

# Tests --------------------

def test_buffered():
    __test_all(BufferedCacheManager())

def test_file():
    __test_all(FileCacheManager('.test-cache'))

# --------------------------

if __name__ == '__main__':
    test_buffered()
    test_file()
