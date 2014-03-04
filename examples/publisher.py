#!/usr/bin/env python

"""
    Amqp client exemple

"""
import asyncio
import aioamqp


@asyncio.coroutine
def produce():
    protocol = yield from aioamqp.connect('localhost', 5672)

    try:
        yield from protocol.start_connection()
    except aioamqp.ClosedConnection:
        print("closed connections")
        return

    queue_name = 'py2.queue'
    channel = yield from protocol.channel()
    yield from asyncio.wait_for(channel.queue(queue_name, durable=False, auto_delete=True), timeout=10)

    while True:
        yield from channel.publish("py3.message", '', queue_name)
        yield from asyncio.sleep(10)
    yield from asyncio.wait_for(protocol.client_close(), timeout=10)


asyncio.get_event_loop().run_until_complete(produce())
