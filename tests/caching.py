# coding: utf-8
"""
    tests.caching
    ~~~~~~~~~~~~~

    Tests for :mod:`brownie.caching`.

    :copyright: 2010 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import time

from attest import Tests, Assert, TestBase, test

from brownie.caching import cached_property, LRUCache


caching_tests = Tests()


@caching_tests.test
def test_cached_property():
    class Foo(object):
        def __init__(self):
            self.counter = 0

        @cached_property
        def spam(self):
            self.counter += 1
            return self.counter
    foo = Foo()
    Assert(foo.spam) == 1
    Assert(foo.spam) == 1


class TestLRUCache(TestBase):
    @test
    def decorate(self):
        @LRUCache.decorate(2)
        def foo(*args, **kwargs):
            time.sleep(.1)
            return args, kwargs

        tests = [
            (('foo', 'bar'), {}),
            (('foo', 'bar'), {'spam': 'eggs'}),
            ((1, 2), {})
        ]
        times = []

        for test in tests:
            args, kwargs = test
            old = time.time()
            Assert(foo(*args, **kwargs)) == test
            new = time.time()
            uncached_time = new - old

            old = time.time()
            Assert(foo(*args, **kwargs)) == test
            new = time.time()
            cached_time = new - old
            Assert(cached_time) < uncached_time
            times.append((uncached_time, cached_time))
        old = time.time()
        foo(*tests[0][0], **tests[0][1])
        new = time.time()
        Assert(new - old) > times[0][1]

    @test
    def basics(self):
        cache = LRUCache(maxsize=2)
        cache[1] = 2
        cache[3] = 4
        cache[5] = 6
        # Assert(cache.items()) == [(3, 4), (5, 6)]

caching_tests.register(TestLRUCache)
