from collections import namedtuple
from queue import Queue
from threading import Event, Thread

import pytest

from pyaxo_ng import Axolotl


def test_init_conversation(axolotl_a, axolotl_b,
                           a_identity_keys, b_identity_keys,
                           a_handshake_keys, b_handshake_keys,
                           a_ratchet_keys, b_ratchet_keys,
                           exchange):
    conv_a = axolotl_a.init_conversation(
        axolotl_b.name,
        priv_identity_key=a_identity_keys[0],
        identity_key=a_identity_keys[1],
        priv_handshake_key=a_handshake_keys[0],
        other_identity_key=b_identity_keys[1],
        other_handshake_key=b_handshake_keys[1],
        priv_ratchet_key=a_ratchet_keys[0],
        ratchet_key=a_ratchet_keys[1],
        other_ratchet_key=b_ratchet_keys[1])

    conv_b = axolotl_b.init_conversation(
        axolotl_a.name,
        priv_identity_key=b_identity_keys[0],
        identity_key=b_identity_keys[1],
        priv_handshake_key=b_handshake_keys[0],
        other_identity_key=a_identity_keys[1],
        other_handshake_key=a_handshake_keys[1],
        priv_ratchet_key=b_ratchet_keys[0],
        ratchet_key=b_ratchet_keys[1],
        other_ratchet_key=a_ratchet_keys[1])

    exchange(conv_a, conv_b)

    o = b'Test msg'
    c = conv_a.encrypt(o)
    p = conv_b.decrypt(c)
    assert o == p
    assert c != o and c != p

def test_init_nonthreaded_conversations(
        axolotl_a, axolotl_b, axolotl_c,
        a_identity_keys, b_identity_keys, c_identity_keys,
        a_handshake_keys, b_handshake_keys, c_handshake_keys,
        a_ratchet_keys, b_ratchet_keys, c_ratchet_keys,
        exchange):
    conversations = initialize_conversations(
        axolotl_a, a_identity_keys, a_handshake_keys, a_ratchet_keys,
        axolotl_b, b_identity_keys, b_handshake_keys, b_ratchet_keys,
        axolotl_c, c_identity_keys, c_handshake_keys, c_ratchet_keys)

    exchange(conversations.ab, conversations.ba)
    exchange(conversations.ac, conversations.ca)
    exchange(conversations.bc, conversations.cb)


def test_init_threaded_conversations(
        threaded_axolotl_a, threaded_axolotl_b, threaded_axolotl_c,
        a_identity_keys, b_identity_keys, c_identity_keys,
        a_handshake_keys, b_handshake_keys, c_handshake_keys,
        a_ratchet_keys, b_ratchet_keys, c_ratchet_keys,
        exchange):
    conversations = initialize_conversations(
        threaded_axolotl_a, a_identity_keys, a_handshake_keys, a_ratchet_keys,
        threaded_axolotl_b, b_identity_keys, b_handshake_keys, b_ratchet_keys,
        threaded_axolotl_c, c_identity_keys, c_handshake_keys, c_ratchet_keys)

    run_threaded_exchanges(exchange, conversations)


def test_create_conversation(axolotl_a, axolotl_b,
                             a_identity_keys, b_identity_keys,
                             a_handshake_keys, b_handshake_keys,
                             a_ratchet_keys, b_ratchet_keys,
                             exchange):
    mkey = b'masterkey'

    conv_a = axolotl_a.create_conversation(
        other_name=axolotl_b.name,
        mkey=mkey,
        mode=True,
        priv_identity_key=a_identity_keys[0],
        identity_key=a_identity_keys[1],
        other_identity_key=b_identity_keys[1],
        other_ratchet_key=b_ratchet_keys[1])

    conv_b = axolotl_b.create_conversation(
        other_name=axolotl_a.name,
        mkey=mkey,
        mode=False,
        priv_identity_key=b_identity_keys[0],
        identity_key=b_identity_keys[1],
        other_identity_key=a_identity_keys[1],
        priv_ratchet_key=b_ratchet_keys[0],
        ratchet_key=b_ratchet_keys[1])

    exchange(conv_a, conv_b)


def test_create_nonthreaded_conversations(
        axolotl_a, axolotl_b, axolotl_c,
        a_identity_keys, b_identity_keys, c_identity_keys,
        a_handshake_keys, b_handshake_keys, c_handshake_keys,
        a_ratchet_keys, b_ratchet_keys, c_ratchet_keys,
        exchange):
    mkey_ab = b'masterkey_ab'
    mkey_ac = b'masterkey_ac'
    mkey_bc = b'masterkey_bc'

    conversations = create_conversations(
        axolotl_a, a_identity_keys, a_handshake_keys, a_ratchet_keys,
        axolotl_b, b_identity_keys, b_handshake_keys, b_ratchet_keys,
        axolotl_c, c_identity_keys, c_handshake_keys, c_ratchet_keys,
        mkey_ab, mkey_ac, mkey_bc)

    exchange(conversations.ab, conversations.ba)
    exchange(conversations.ac, conversations.ca)
    exchange(conversations.bc, conversations.cb)


def test_create_threaded_conversations(
        threaded_axolotl_a, threaded_axolotl_b, threaded_axolotl_c,
        a_identity_keys, b_identity_keys, c_identity_keys,
        a_handshake_keys, b_handshake_keys, c_handshake_keys,
        a_ratchet_keys, b_ratchet_keys, c_ratchet_keys,
        exchange):
    mkey_ab = b'masterkey_ab'
    mkey_ac = b'masterkey_ac'
    mkey_bc = b'masterkey_bc'

    conversations = create_conversations(
        threaded_axolotl_a, a_identity_keys, a_handshake_keys, a_ratchet_keys,
        threaded_axolotl_b, b_identity_keys, b_handshake_keys, b_ratchet_keys,
        threaded_axolotl_c, c_identity_keys, c_handshake_keys, c_ratchet_keys,
        mkey_ab, mkey_ac, mkey_bc)

    run_threaded_exchanges(exchange, conversations)


@pytest.fixture()
def threaded_axolotl_a():
    return Axolotl('Angie', dbpassphrase=None)


@pytest.fixture()
def threaded_axolotl_b():
    return Axolotl('Barb', dbpassphrase=None)


@pytest.fixture()
def threaded_axolotl_c():
    return Axolotl('Charlie', dbpassphrase=None)


class ThreadedExchange(Thread):
    def __init__(self, exchange, axolotl_x, axolotl_y, event, queue):
        super(ThreadedExchange, self).__init__()
        self.daemon = True
        self.exchange = exchange
        self.axolotl_x = axolotl_x
        self.axolotl_y = axolotl_y
        self.event = event
        self.queue = queue

    def run(self):
        self.event.wait()
        try:
            self.exchange(self.axolotl_x, self.axolotl_y)
        except AssertionError:
            self.queue.put(False)
        else:
            self.queue.put(True)


Conversations = namedtuple('Conversations', 'ab ac ba bc ca cb')


def initialize_conversations(
        axolotl_a, a_identity_keys, a_handshake_keys, a_ratchet_keys,
        axolotl_b, b_identity_keys, b_handshake_keys, b_ratchet_keys,
        axolotl_c, c_identity_keys, c_handshake_keys, c_ratchet_keys):
    ab = axolotl_a.init_conversation(
        other_name=axolotl_b.name,
        priv_identity_key=a_identity_keys[0],
        identity_key=a_identity_keys[1],
        priv_handshake_key=a_handshake_keys[0],
        other_identity_key=b_identity_keys[1],
        other_handshake_key=b_handshake_keys[1],
        priv_ratchet_key=a_ratchet_keys[0],
        ratchet_key=a_ratchet_keys[1],
        other_ratchet_key=b_ratchet_keys[1])

    ac = axolotl_a.init_conversation(
        other_name=axolotl_c.name,
        priv_identity_key=a_identity_keys[0],
        identity_key=a_identity_keys[1],
        priv_handshake_key=a_handshake_keys[0],
        other_identity_key=c_identity_keys[1],
        other_handshake_key=c_handshake_keys[1],
        priv_ratchet_key=a_ratchet_keys[0],
        ratchet_key=a_ratchet_keys[1],
        other_ratchet_key=c_ratchet_keys[1])

    ba = axolotl_b.init_conversation(
        other_name=axolotl_a.name,
        priv_identity_key=b_identity_keys[0],
        identity_key=b_identity_keys[1],
        priv_handshake_key=b_handshake_keys[0],
        other_identity_key=a_identity_keys[1],
        other_handshake_key=a_handshake_keys[1],
        priv_ratchet_key=b_ratchet_keys[0],
        ratchet_key=b_ratchet_keys[1],
        other_ratchet_key=a_ratchet_keys[1])

    bc = axolotl_b.init_conversation(
        other_name=axolotl_c.name,
        priv_identity_key=b_identity_keys[0],
        identity_key=b_identity_keys[1],
        priv_handshake_key=b_handshake_keys[0],
        other_identity_key=c_identity_keys[1],
        other_handshake_key=c_handshake_keys[1],
        priv_ratchet_key=b_ratchet_keys[0],
        ratchet_key=b_ratchet_keys[1],
        other_ratchet_key=c_ratchet_keys[1])

    ca = axolotl_c.init_conversation(
        other_name=axolotl_a.name,
        priv_identity_key=c_identity_keys[0],
        identity_key=c_identity_keys[1],
        priv_handshake_key=c_handshake_keys[0],
        other_identity_key=a_identity_keys[1],
        other_handshake_key=a_handshake_keys[1],
        priv_ratchet_key=c_ratchet_keys[0],
        ratchet_key=b_ratchet_keys[1],
        other_ratchet_key=a_ratchet_keys[1])

    cb = axolotl_c.init_conversation(
        other_name=axolotl_b.name,
        priv_identity_key=c_identity_keys[0],
        identity_key=c_identity_keys[1],
        priv_handshake_key=c_handshake_keys[0],
        other_identity_key=b_identity_keys[1],
        other_handshake_key=b_handshake_keys[1],
        priv_ratchet_key=c_ratchet_keys[0],
        ratchet_key=c_ratchet_keys[1],
        other_ratchet_key=b_ratchet_keys[1])

    return Conversations(ab, ac, ba, bc, ca, cb)


def create_conversations(
        axolotl_a, a_identity_keys, a_handshake_keys, a_ratchet_keys,
        axolotl_b, b_identity_keys, b_handshake_keys, b_ratchet_keys,
        axolotl_c, c_identity_keys, c_handshake_keys, c_ratchet_keys,
        mkey_ab, mkey_ac, mkey_bc):
    ab = axolotl_a.create_conversation(
        other_name=axolotl_b.name,
        mkey=mkey_ab,
        mode=True,
        priv_identity_key=a_identity_keys[0],
        identity_key=a_identity_keys[1],
        other_identity_key=b_identity_keys[1],
        other_ratchet_key=b_ratchet_keys[1])

    ac = axolotl_a.create_conversation(
        other_name=axolotl_c.name,
        mkey=mkey_ac,
        mode=False,
        priv_identity_key=a_identity_keys[0],
        identity_key=a_identity_keys[1],
        other_identity_key=c_identity_keys[1],
        priv_ratchet_key=a_ratchet_keys[0],
        ratchet_key=a_ratchet_keys[1])

    ba = axolotl_b.create_conversation(
        other_name=axolotl_a.name,
        mkey=mkey_ab,
        mode=False,
        priv_identity_key=b_identity_keys[0],
        identity_key=b_identity_keys[1],
        other_identity_key=a_identity_keys[1],
        priv_ratchet_key=b_ratchet_keys[0],
        ratchet_key=b_ratchet_keys[1])

    bc = axolotl_b.create_conversation(
        other_name=axolotl_c.name,
        mkey=mkey_bc,
        mode=True,
        priv_identity_key=b_identity_keys[0],
        identity_key=b_identity_keys[1],
        other_identity_key=c_identity_keys[1],
        other_ratchet_key=c_ratchet_keys[1])

    ca = axolotl_c.create_conversation(
        other_name=axolotl_a.name,
        mkey=mkey_ac,
        mode=True,
        priv_identity_key=c_identity_keys[0],
        identity_key=c_identity_keys[1],
        other_identity_key=a_identity_keys[1],
        other_ratchet_key=a_ratchet_keys[1])

    cb = axolotl_c.create_conversation(
        other_name=axolotl_b.name,
        mkey=mkey_bc,
        mode=False,
        priv_identity_key=c_identity_keys[0],
        identity_key=c_identity_keys[1],
        other_identity_key=b_identity_keys[1],
        priv_ratchet_key=c_ratchet_keys[0],
        ratchet_key=c_ratchet_keys[1])

    return Conversations(ab, ac, ba, bc, ca, cb)


def run_threaded_exchanges(exchange, conversations):
    event = Event()

    queue_ab = Queue()
    exchange_ab = ThreadedExchange(exchange,
                                   conversations.ab, conversations.ba,
                                   event, queue_ab)

    queue_ac = Queue()
    exchange_ac = ThreadedExchange(exchange,
                                   conversations.ac, conversations.ca,
                                   event, queue_ac)

    queue_bc = Queue()
    exchange_bc = ThreadedExchange(exchange,
                                   conversations.bc, conversations.cb,
                                   event, queue_bc)

    exchange_ab.start()
    exchange_ac.start()
    exchange_bc.start()

    event.set()

    assert queue_ab.get() and queue_ac.get() and queue_bc.get()
