from concurrent.futures.thread import ThreadPoolExecutor
from decimal import Decimal

from django.db import connections


def quantize_balance(balance, digits=2):
    return str(Decimal(balance).quantize(Decimal("1." + "0" * digits)))


def call_concurrently(concurrency, calls_count, target, args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    thread_pool_executer = ThreadPoolExecutor(max_workers=concurrency)

    def make_concurrent_query():
        try:
            return target(*args, **kwargs)
        finally:
            # Close all thread local connections to allow close pytest connection in
            # main thread.
            connections.close_all()

    futures = [
        thread_pool_executer.submit(make_concurrent_query) for _ in range(calls_count)
    ]
    thread_pool_executer.shutdown()
    return futures
