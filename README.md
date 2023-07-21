# Ethereum API

The Ethereum API project implements an interface in order to enable the request of data from the Ethereum Blockchain. The main focus is on the implementation of functions to interact with smart contracts. A container-based client-server architecture is used as architecture. Therefore, the project is about the development of a [Docker container](https://hub.docker.com/repository/docker/fabian253/ethereum_api/general).

An Ethereum Node is required to use the API, with both an execution and consensus client needed. [Geth](https://geth.ethereum.org) and [Lighthouse](https://lighthouse.sigmaprime.io) are suitable here, since the configuration of the project is set up for the corresponding endpoints and must otherwise be adjusted. Besides the two Ethereum clients, a [SQL database](https://www.mysql.com/de/) is required to use the API. This database is needed for indexing data from the Ethereum Blockchain. All required parts of the application can be run as a Docker container.

## Structure

The actual project is located in the app folder with the other files dealing with the creation of the Docker container. The app project folder contains the api_params, connectors, db_params, endpoints, and token_standards subfolders. It also contains a configuration file, dependencies and the main file. 

- **api_params**: includes all parameters belonging to the API, like decorators, metadata and a user database
- **connectors**: includes the connectors to both ethereum clients and the sql database as well as their initialization
- **db_params**: includes parameters for initializing the database
- **endpoints**: includes all endpoints of the API subdivided into groups depending on the functionality
- **token_standards**: includes the ABIs of selected [Ethereum token standards](https://eips.ethereum.org/erc)

The individual endpoint groups are divided into parameters, the router and schemas.

- **parameters**: includes query parameters that are used in the request
- **router**: includes the actual endpoints and thus part of the application logic
- **schemas**: includes schemas for the data passed and returned in requests

