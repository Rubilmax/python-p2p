User manual
===========

General introduction
********************

A :code:`Peer` is an instance of a listening device, which is able to connect to another listening :code:`Peer`.
A :code:`Connection` represents a link between 2 :code:`Peer` on a local network. It allows the serialization and the exchange of data over TCP.

.. note::
   Every address is an IPv4 address.

.. note::
   Every connection has 2 fixed peers, 1 fixed data type and possibly 1 fixed data size in case of a streaming connection (a connection over which we only exchange data of fixed size).

.. note::
   Data type is one of:

   * :code:`"raw"` (any object pickle-serialized to bytes)
   * :code:`"json"` (any json-serializable object)
   * :code:`"bytes"` (explicit)

Protocols
*********

Connection protocol
-------------------

In the following scenario, Alice knows the address and listening port of Bob:

* Alice sends a *HELLO* header to Bob, containing her address and port and information about the desired connection: **HELLO|address_name=127.0.0.1:51515&data_type=json**
* Bob receives the *HELLO* header and answers with a *ACCEPT* or *DENY* header, depending on his choice.
* Alice waits for an answer from Bob within a given timeout, before giving up. If she receives a *ACCEPT* header from Bob, both acknowledge they have established a connection.

.. note::
   For the underlying python's :code:`socket`, a connection is established from the first step of this protocol. As we only listen for utf-8 encoded bytes headers until the end of the previous protocol, this doesn't present security issues.

Data protocol
-------------

In the following scenario, Alice and Bob already established a connection and thus have come to an agreement on data types for this connection (and possible data size, in case of a streaming connection). Alice wants to send Bob some data:

* Alice sends a *DATA* header to Bob, containing information about the following data: **DATA|data_size=2048&data_type=raw**
* Bob receives the header and reads it: he sees that the following data_type is :code:`raw`. If they previously agreed on a :code:`strict` connection, Bob shuts down the connection with Alice, as Alice violated their agreement. Otherwise, he proceeds with receiving data.
* As TCP is a reliable data exchange protocol, no further acknowledgment packet is exchanged and the data transmission is considered completed.

Discovery protocol
------------------

Peerpy comes with a builtin discovery protocol built over UDP. In the following scenario, Alice wants to discover people on her local network:

* Alice sends a *PING* packet to her router's UDP broadcasting IPv4 address, containing her address and listening port: **PING 192.168.0.2:51515**.
* Bob listens for packets on his router's UDP broadcasting IPv4 address, waiting for *PING* packets. He receives Alice's packet and sends her a *PONG* packet, containing his address and listening port: **PING 192.168.0.3:62626**.
* Alice receives Bob's *PONG* packet and thus knows that Bob is reachable over the address he shared.

Events & Handlers
*****************

:code:`Peer` and :code:`Connection` classes both inherits from the :code:`EventHandler` superclass, which allows one to pass event handlers (python callables) which will respectively be called by the peer's listening thread and the connection's main thread upon the corresponding event.

Let's say for example that you want to print your :code:`Peer` object's address and listening port (which is the default behavior). Then you just have to register your handler at your :code:`Peer` instanciation::

   with Peer(handlers={
      "listen": lambda peer: print(peer.address, peer.address_name)
   }) as peer:

Here is a table showing every events and handlers possible:

.. versionchanged:: 1.2.0
   Whenever a handler is called, the first argument is now the event emitter.

+--------------------+--------------------+------------------------------------------------------------------------------------+----------------------------------+
| Emitter            | Event              | Description                                                                        | Additional arguments             |
+====================+====================+====================================================================================+==================================+
|                    | :code:`listen`     | Triggered when peer is listening for connections                                   |                                  |
+                    +--------------------+------------------------------------------------------------------------------------+----------------------------------+
|                    | :code:`offer`      | Triggered when peer has received a connection offer.                               | The connection to accept or deny |
|                    |                    | This handler must return a boolean indicating whether to accept or deny the offer. |                                  |
+ :code:`Peer`       +--------------------+------------------------------------------------------------------------------------+----------------------------------+
|                    | :code:`connection` | Triggered when peer has established a new connection                               | The connection established       |
+                    +--------------------+------------------------------------------------------------------------------------+----------------------------------+
|                    | :code:`stop`       | Triggered when peer has stopped listening for connections                          |                                  |
+--------------------+--------------------+------------------------------------------------------------------------------------+----------------------------------+
|                    | :code:`data`       | Triggered when connection has received some data                                   | The data received                |
+ :code:`Connection` +--------------------+------------------------------------------------------------------------------------+----------------------------------+
|                    | :code:`close`      | Triggered when connection has been terminated                                      |                                  |
+--------------------+--------------------+------------------------------------------------------------------------------------+----------------------------------+