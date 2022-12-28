from execution_client_connector import ExecutionClientConnector
import config
import json

execution_client = ExecutionClientConnector(
    config.EXECUTION_CLIENT_IP, config.EXECUTION_CLIENT_PORT)

if __name__ == "__main__":
    response = execution_client.get_transaction("0x09253105dd507588b6648b7dd07f0f97c532fc4de1817c9d943a81395f2ac892")

    json_object = json.dumps(response, indent=4)

    with open("app/execution_client_connector_test.json", "w") as outfile:
        outfile.write(json_object)
