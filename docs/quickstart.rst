.. _quickstart:

Quickstart
==========

.. contents:: :local:

.. NOTE:: All code starting with a ``$`` is meant to run on your terminal.
    All code starting with a ``>>>`` is meant to run in a python interpreter,
    like `ipython <https://pypi.org/project/ipython/>`_.

Installation
------------

platon.py can be installed (preferably in a :ref:`virtualenv <setup_environment>`)
using ``pip`` as follows:

.. code-block:: shell

   $ pip install platon.py


.. NOTE:: If you run into problems during installation, you might have a
    broken environment. See the troubleshooting guide to :ref:`setting up a
    clean environment <setup_environment>`.


Using Web3
----------

This library depends on a connection to an Platon node. We call these connections
*Providers* and there are several ways to configure them. The full details can be found
in the :ref:`Providers<providers>` documentation. This Quickstart guide will highlight
a couple of the most common use cases.


Provider: Local platon Node
**************************

For locally run nodes, an IPC connection is the most secure option, but HTTP and
websocket configurations are also available. By default, `platon
<https://devdocs.platon.network/docs/zh-CN/Become_PlatON_Main_Verification>`_
exposes port ``6789`` to serve HTTP requests and ``6790`` for websocket requests. Connecting
to this local node can be done as follows:

.. code-block:: python

   >>> from platon import Web3

   # IPCProvider:
   >>> w3 = Web3(Web3.IPCProvider('./path/to/node.ipc'))

   # HTTPProvider:
   >>> w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:6789'))

   # WebsocketProvider:
   >>> w3 = Web3(Web3.WebsocketProvider('ws://127.0.0.1:6790'))

   >>> w3.isConnected()
   True

If you stick to the default ports or IPC file locations, you can utilize a
:ref:`convenience method <automatic_provider>` to automatically detect the provider
and save a few keystrokes:

.. code-block:: python

   >>> from platon.chains import w3
   >>> w3.isConnected()
   True

.. _first_w3_use:

Getting Blockchain Info
-----------------------

It's time to start using platon.py! Once properly configured, the ``w3`` instance will allow you
to interact with the Platon blockchain. Try getting all the information about the latest block:

.. code-block:: python

    >>> w3.platon.get_block('latest')
    {'gasLimit': 6283185,
     'gasUsed': 0,
     'hash': HexBytes('0x53b983fe73e16f6ed8178f6c0e0b91f23dc9dad4cb30d0831f178291ffeb8750'),
     'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'),
     'miner': '0x0000000000000000000000000000000000000000',
     'nonce': HexBytes('0x0000000000000000'),
     'number': 0,
     'parentHash': HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'),
     'receiptsRoot': HexBytes('0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421'),
     'size': 622,
     'stateRoot': HexBytes('0x1f5e460eb84dc0606ab74189dbcfe617300549f8f4778c3c9081c119b5b5d1c1'),
     'timestamp': 0,
     'transactions': [],
     'transactionsRoot': HexBytes('0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421'),

platon.py can help you read block data, sign and send transactions, deploy and interact with contracts,
and a number of other features.

Many of the typical things you'll want to do will be in the :class:`w3.platon <web3.platon.Platon>` API,
so that is a good place to start.

If you want to dive straight into contracts, check out the section on :ref:`contracts`,
including a :ref:`contract_example`, and how to create a contract instance using
:meth:`w3.platon.contract() <web3.platon.Platon.contract>`.

.. NOTE:: It is recommended that your development environment have the ``PYTHONWARNINGS=default``
    environment variable set. Some deprecation warnings will not show up
    without this variable being set.
