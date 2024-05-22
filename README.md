# SimpleTor Project Technical Documentation

## Overview
The SimpleTor project is a Python-based application that simulates the functionality of the Tor network. It includes a client, multiple nodes (proxies), and a directory server. The client sends requests through multiple nodes to the final destination, and the response is sent back through the same nodes. This process ensures anonymity and security of the client's data.

## Components

### Client (`client/client.py`)
The client is responsible for initiating the connection and sending requests. It uses triple layer encryption to encrypt the data before sending it to the first node. The client also handles the decryption of the response data.

### Node (`node/node.py`)
Nodes are intermediaries in the network. They receive encrypted data from the client or a previous node, decrypt it to find out the next node in the path, and forward the data to the next node. Each node only knows about the previous and next node in the path, ensuring the anonymity of the client.

### Directory Server (`directory_server/directory_server.py`)
The directory server is responsible for managing the nodes in the network. It provides the client with the list of nodes that can be used to form a path for the data.

### Data Server (`data/main_data_server.py`)
The data server is the final destination of the client's request. It receives the request from the last node in the path, processes it, and sends the response back through the same path.

### RSA Encryption (`rsa/rsa.py`)
The RSA module provides functions for RSA encryption and decryption. It is used by the client and the nodes to encrypt and decrypt the data.

## Workflow
1. The client connects to the directory server to get a list of nodes.
2. The client selects a path through the nodes and encrypts the data using triple layer encryption.
3. The client sends the encrypted data to the first node in the path.
4. Each node decrypts the data to find out the next node in the path and forwards the data to the next node.
5. The last node in the path sends the data to the data server.
6. The data server processes the request and sends the response back through the same path.
7. Each node forwards the response to the previous node in the path.
8. The client receives the response from the first node in the path and decrypts it.

## Key Files
- `src/client.py`: Contains the Client class which is responsible for initiating the connection and sending requests.
- `node/node.py`: Contains the Node class which acts as an intermediary in the network.
- `src/directory_server.py`: Contains the Server class which manages the nodes in the network.
- `src/main_data_server.py`: Contains the DataServer class which is the final destination of the client's request.
- `rsa/rsa.py`: Provides functions for RSA encryption and decryption.
- `node/node_setup.py`: Contains the setup script for the Node.

## Dependencies
- Python 3.8 or higher
- `cryptography` Python library for RSA encryption and decryption
- `requests` Python library for making HTTP requests
- `json` Python library for handling JSON data
- `socket` Python library for creating socket connections
- `threading` Python library for creating threads
- `base64` Python library for encoding and decoding data in base64
- `random` Python library for generating random numbers

## Setup
1. Install Python 3.8 or higher.
2. Install the required Python libraries using pip:
3. Run the directory server, data server, and nodes.
4. Run the client to send a request.
