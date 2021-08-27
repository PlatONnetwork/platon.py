.. _Gas_Price:

Gas Price API
===============

.. warning::
    Gas price strategy is only supported for legacy transactions. The London fork
    introduced ``maxFeePerGas`` and ``maxPriorityFeePerGas`` transaction parameters
    which should be used over ``gasPrice`` whenever possible.

For Platon (legacy) transactions, gas price is a delicate property. For this reason,
Web3 includes an API for configuring it.

The Gas Price API allows you to define Web3's behaviour for populating the gas price.
This is done using a "Gas Price Strategy" - a method which takes the Web3 object and a
transaction dictionary and returns a gas price (denominated in von).

Retrieving gas price
--------------------

To retrieve the gas price using the selected strategy simply call
:meth:`~web3.platon.Platon.generate_gas_price`

.. code-block:: python

    >>> web3.platon.generate_gas_price()
    20000000000

Creating a gas price strategy
-------------------------------

A gas price strategy is implemented as a python method with the following
signature:

.. code-block:: python

    def gas_price_strategy(web3, transaction_params=None):
    ...

The method must return a positive integer representing the gas price in von.

To demonstrate, here is a rudimentary example of a gas price strategy that
returns a higher gas price when the value of the transaction is higher than
1 Ether.

.. code-block:: python

    from platon import Web3

    def value_based_gas_price_strategy(web3, transaction_params):
        if transaction_params['value'] > Web3.toVon(1, 'ether'):
            return Web3.toVon(20, 'gvon')
        else:
            return Web3.toVon(5, 'gvon')

Selecting the gas price strategy
--------------------------------

The gas price strategy can be set by calling :meth:`~web3.platon.Platon.set_gas_price_strategy`.

.. code-block:: python

    from platon import Web3

    def value_based_gas_price_strategy(web3, transaction_params):
        ...

    w3 = Web3(...)
    w3.platon.set_gas_price_strategy(value_based_gas_price_strategy)

Available gas price strategies
------------------------------

.. py:module:: web3.gas_strategies.rpc

.. py:method:: rpc_gas_price_strategy(web3, transaction_params=None)

    Makes a call to the `JSON-RPC platon_gasPrice
    method <https://github.com/platonnetwork/wiki/wiki/JSON-RPC#platon_gasprice>`_ which returns
    the gas price configured by the connected Platon node.

.. py:module:: web3.gas_strategies.time_based

.. py:method:: construct_time_based_gas_price_strategy(max_wait_seconds, sample_size=120, probability=98, weighted=False)

    Constructs a strategy which will compute a gas price such that the
    transaction will be mined within a number of seconds defined by
    ``max_wait_seconds`` with a probability defined by ``probability``.  The
    gas price is computed by sampling ``sample_size`` of the most recently
    mined blocks. If ``weighted=True``, the block time will be weighted towards
    more recently mined blocks.

    * ``max_wait_seconds`` The desired maxiumum number of seconds the
      transaction should take to mine.
    * ``sample_size`` The number of recent blocks to sample
    * ``probability`` An integer representation of the desired probability that
      the transaction will be mined within ``max_wait_seconds``.  0 means 0%
      and 100 means 100%.

    The following ready to use versions of this strategy are available.

    * ``web3.gas_strategies.time_based.fast_gas_price_strategy``: Transaction mined within 60 seconds.
    * ``web3.gas_strategies.time_based.medium_gas_price_strategy``: Transaction mined within 5 minutes.
    * ``web3.gas_strategies.time_based.slow_gas_price_strategy``: Transaction mined within 1 hour.
    * ``web3.gas_strategies.time_based.glacial_gas_price_strategy``: Transaction mined within 24 hours.

    .. warning:: Due to the overhead of sampling the recent blocks it is
      recommended that a caching solution be used to reduce the amount of chain
      data that needs to be re-fetched for each request.

    .. code-block:: python

        from platon import Web3, middleware
        from platon.gas_strategies.time_based import medium_gas_price_strategy

        w3 = Web3()
        w3.platon.set_gas_price_strategy(medium_gas_price_strategy)

        w3.middleware_onion.add(middleware.time_based_cache_middleware)
        w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        w3.middleware_onion.add(middleware.simple_cache_middleware)
