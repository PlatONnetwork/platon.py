.. _overview:

Overview
========

The purpose of this page is to give you a sense of everything platon.py can do
and to serve as a quick reference guide. You'll find a summary of each feature
with links to learn more. You may also be interested in the
:ref:`Examples <examples>` page, which demonstrates some of these features in
greater detail.


Configuration
~~~~~~~~~~~~~

After installing platon.py (via ``pip install web3``), you'll need to specify the
provider and any middleware you want to use beyond the defaults.


Providers
---------

Providers are how platon.py connects to the blockchain. The library comes with the
following built-in providers:

- ``Web3.IPCProvider`` for connecting to ipc socket based JSON-RPC servers.
- ``Web3.HTTPProvider`` for connecting to http and https based JSON-RPC servers.
- ``Web3.WebsocketProvider`` for connecting to ws and wss websocket based JSON-RPC servers.

.. code-block:: python

   >>> from platon import Web3

   # IPCProvider:
   >>> w3 = Web3(Web3.IPCProvider('./path/to/node.ipc'))

   # HTTPProvider:
   >>> w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

   # WebsocketProvider:
   >>> w3 = Web3(Web3.WebsocketProvider('ws://127.0.0.1:8546'))

   >>> w3.isConnected()
   True

For more information, (e.g., connecting to remote nodes, provider auto-detection,
using a test provider) see the :ref:`Providers <providers>` documentation.


Middleware
----------

Your platon.py instance may be further configured via middleware.

platon.py middleware is described using an onion metaphor, where each layer of
middleware may affect both the incoming request and outgoing response from your
provider. The documentation includes a :ref:`visualization <Modifying_Middleware>`
of this idea.

Several middleware are :ref:`included by default <default_middleware>`. You may add to
(:meth:`add <Web3.middleware_onion.add>`, :meth:`inject <Web3.middleware_onion.inject>`,
:meth:`replace <Web3.middleware_onion.replace>`) or disable
(:meth:`remove <Web3.middleware_onion.remove>`,
:meth:`clear <Web3.middleware_onion.clear>`) any of these middleware.


Your Keys
~~~~~~~~~

Private keys are required to approve any transaction made on your behalf. The manner in
which your key is secured will determine how you create and send transactions in platon.py.

A local node, like `Pnode <https://node.platon.org/>`_, may manage your keys for you.
You can reference those keys using the :attr:`web3.platon.accounts <web3.platon.Platon.accounts>`
property.

A hosted node, like `Infura <https://infura.io/>`_, will have no knowledge of your keys.
In this case, you'll need to have your private key available locally for signing
transactions.

Full documentation on the distinction between keys can be found :ref:`here <platon-account>`.


Base API
~~~~~~~~

The :ref:`Web3 <web3_base>` class includes a number of convenient utility functions:


Encoding and Decoding Helpers
-----------------------------

- :meth:`Web3.is_encodable() <web3.w3.is_encodable>`
- :meth:`Web3.toBytes() <web3.Web3.toBytes>`
- :meth:`Web3.toHex() <web3.Web3.toHex>`
- :meth:`Web3.toInt() <web3.Web3.toInt>`
- :meth:`Web3.toJSON() <web3.Web3.toJSON>`
- :meth:`Web3.toText() <web3.Web3.toText>`


Address Helpers
---------------

- :meth:`Web3.isAddress() <web3.Web3.isAddress>`
- :meth:`Web3.isChecksumAddress() <web3.Web3.isChecksumAddress>`
- :meth:`Web3.toChecksumAddress() <web3.Web3.toChecksumAddress>`


Currency Conversions
--------------------

- :meth:`Web3.fromVon() <web3.Web3.fromVon>`
- :meth:`Web3.toVon() <web3.Web3.toVon>`


Cryptographic Hashing
---------------------

- :meth:`Web3.keccak() <web3.Web3.keccak>`
- :meth:`Web3.solidityKeccak() <web3.Web3.solidityKeccak>`


web3.platon API
~~~~~~~~~~~~

The most commonly used APIs for interacting with Platon can be found under the
``web3.platon`` namespace.  As a reminder, the :ref:`Examples <examples>` page will
demonstrate how to use several of these methods.


Fetching Data
-------------

Viewing account balances (:meth:`get_balance <web3.platon.Platon.get_balance>`), transactions
(:meth:`get_transaction <web3.platon.Platon.get_transaction>`), and block data
(:meth:`get_block <web3.platon.Platon.get_block>`) are some of the most common starting
points in platon.py.


API
^^^

- :meth:`web3.platon.get_balance() <web3.platon.Platon.get_balance>`
- :meth:`web3.platon.get_block() <web3.platon.Platon.get_block>`
- :meth:`web3.platon.get_block_transaction_count() <web3.platon.Platon.get_block_transaction_count>`
- :meth:`web3.platon.get_code() <web3.platon.Platon.get_code>`
- :meth:`web3.platon.get_proof() <web3.platon.Platon.get_proof>`
- :meth:`web3.platon.get_storage_at() <web3.platon.Platon.get_storage_at>`
- :meth:`web3.platon.get_transaction() <web3.platon.Platon.get_transaction>`
- :meth:`web3.platon.get_transaction_by_block() <web3.platon.Platon.get_transaction_by_block>`
- :meth:`web3.platon.get_transaction_count() <web3.platon.Platon.get_transaction_count>`


Making Transactions
-------------------

The most common use cases will be satisfied with
:meth:`send_transaction <web3.platon.Platon.send_transaction>` or the combination of
:meth:`sign_transaction <web3.platon.Platon.sign_transaction>` and
:meth:`send_raw_transaction <web3.platon.Platon.send_raw_transaction>`.

.. note::

   If interacting with a smart contract, a dedicated API exists. See the next
   section, :ref:`Contracts <overview_contracts>`.


API
^^^

- :meth:`web3.platon.send_transaction() <web3.platon.Platon.send_transaction>`
- :meth:`web3.platon.sign_transaction() <web3.platon.Platon.sign_transaction>`
- :meth:`web3.platon.send_raw_transaction() <web3.platon.Platon.send_raw_transaction>`
- :meth:`web3.platon.replace_transaction() <web3.platon.Platon.replace_transaction>`
- :meth:`web3.platon.modify_transaction() <web3.platon.Platon.modify_transaction>`
- :meth:`web3.platon.wait_for_transaction_receipt() <web3.platon.Platon.wait_for_transaction_receipt>`
- :meth:`web3.platon.get_transaction_receipt() <web3.platon.Platon.get_transaction_receipt>`
- :meth:`web3.platon.sign() <web3.platon.Platon.sign>`
- :meth:`web3.platon.sign_typed_data() <web3.platon.Platon.sign_typed_data>`
- :meth:`web3.platon.estimate_gas() <web3.platon.Platon.estimate_gas>`
- :meth:`web3.platon.generate_gas_price() <web3.platon.Platon.generate_gas_price>`
- :meth:`web3.platon.set_gas_price_strategy() <web3.platon.Platon.set_gas_price_strategy>`


.. _overview_contracts:

Contracts
---------

The two most common use cases involving smart contracts are deploying and executing
functions on a deployed contract.

Deployment requires that the contract already be compiled, with its bytecode and ABI
available. This compilation step can done within
`Remix <http://remix.platon.org/>`_ or one of the many contract development
frameworks, such as `Brownie <https://platon-brownie.readthedocs.io/>`_.

Once the contract object is instantiated, calling ``transact`` on the
:meth:`constructor <web3.contract.Contract.constructor>` method will deploy an
instance of the contract:

.. code-block:: python

   >>> ExampleContract = w3.platon.contract(abi=abi, bytecode=bytecode)
   >>> tx_hash = ExampleContract.constructor().transact()
   >>> tx_receipt = w3.platon.wait_for_transaction_receipt(tx_hash)
   >>> tx_receipt.contractAddress
   '0x8a22225eD7eD460D7ee3842bce2402B9deaD23D3'

Once loaded into a Contract object, the functions of a deployed contract are available
on the ``functions`` namespace:

.. code-block:: python

   >>> deployed_contract = w3.platon.contract(address=tx_receipt.contractAddress, abi=abi)
   >>> deployed_contract.functions.myFunction(42).transact()

If you want to read data from a contract (or see the result of transaction locally,
without executing it on the network), you can use the
:meth:`ContractFunction.call <web3.contract.ContractFunction.call>` method, or the
more concise :attr:`ContractCaller <web3.contract.ContractCaller>` syntax:

.. code-block:: python

   # Using ContractFunction.call
   >>> deployed_contract.functions.getMyValue().call()
   42

   # Using ContractCaller
   >>> deployed_contract.caller().getMyValue()
   42

For more, see the full :ref:`Contracts` documentation.


API
^^^

- :meth:`web3.platon.contract() <web3.platon.Platon.contract>`
- :attr:`Contract.address <web3.contract.Contract.address>`
- :attr:`Contract.abi <web3.contract.Contract.abi>`
- :attr:`Contract.bytecode <web3.contract.Contract.bytecode>`
- :attr:`Contract.bytecode_runtime <web3.contract.Contract.bytecode_runtime>`
- :attr:`Contract.functions <web3.contract.Contract.functions>`
- :attr:`Contract.events <web3.contract.Contract.events>`
- :attr:`Contract.fallback <web3.contract.Contract.fallback.call>`
- :meth:`Contract.constructor() <web3.contract.Contract.constructor>`
- :meth:`Contract.encodeABI() <web3.contract.Contract.encodeABI>`
- :attr:`web3.contract.ContractFunction <web3.contract.ContractFunction>`
- :attr:`web3.contract.ContractEvents <web3.contract.ContractEvents>`


Logs and Filters
----------------

If you want to react to new blocks being mined or specific events being emitted by
a contract, you can leverage platon.py filters.

.. code-block:: python

   # Use case: filter for new blocks
   >>> new_filter = web3.platon.filter('latest')

   # Use case: filter for contract event "MyEvent"
   >>> new_filter = deployed_contract.events.MyEvent.create_filter(fromBlock='latest')

   # retrieve filter results:
   >>> new_filter.get_all_entries()
   >>> new_filter.get_new_entries()

More complex patterns for creating filters and polling for logs can be found in the
:ref:`Filtering <filtering>` documentation.


API
^^^

- :meth:`web3.platon.filter() <web3.platon.Platon.filter>`
- :meth:`web3.platon.get_filter_changes() <web3.platon.Platon.get_filter_changes>`
- :meth:`web3.platon.get_filter_logs() <web3.platon.Platon.get_filter_logs>`
- :meth:`web3.platon.uninstall_filter() <web3.platon.Platon.uninstall_filter>`
- :meth:`web3.platon.get_logs() <web3.platon.Platon.get_logs>`
- :meth:`Contract.events.your_event_name.create_filter() <web3.contract.Contract.events.your_event_name.create_filter>`
- :meth:`Contract.events.your_event_name.build_filter() <web3.contract.Contract.events.your_event_name.build_filter>`
- :meth:`Filter.get_new_entries() <web3.utils.filters.Filter.get_new_entries>`
- :meth:`Filter.get_all_entries() <web3.utils.filters.Filter.get_all_entries>`
- :meth:`Filter.format_entry() <web3.utils.filters.Filter.format_entry>`
- :meth:`Filter.is_valid_entry() <web3.utils.filters.Filter.is_valid_entry>`


Net API
~~~~~~~

Some basic network properties are available on the ``web3.net`` object:

- :attr:`web3.net.listening`
- :attr:`web3.net.peer_count`
- :attr:`web3.net.version`


ethPM
~~~~~

ethPM allows you to package up your contracts for reuse or use contracts from
another trusted registry. See the full details :ref:`here <platonpm>`.


ENS
~~~

`Platon Name Service (ENS) <https://ens.domains/>`_ provides the infrastructure
for human-readable addresses. As an example, instead of
``0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359``, you can send funds to
``platonfoundation.platon``. platon.py has support for ENS, documented
:ref:`here <ens_overview>`.
