from execution_client_connector import ExecutionClientConnector
import config
import json

execution_client = ExecutionClientConnector(
    config.EXECUTION_CLIENT_IP, config.EXECUTION_CLIENT_PORT)

if __name__ == "__main__":
    response = execution_client.get_syncing()

    json_object = json.dumps(response, indent=4)

    with open("app/execution_client_connector_test.json", "w") as outfile:
        outfile.write(json_object)
