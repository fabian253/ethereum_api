import app.config as config
from app.connectors import ExecutionClientConnector, ConsensusClientConnector, SqlDatabaseConnector, TokenStandard
import app.db_params.sql_tables as tables

# init sql database connector
sql_db_connector = SqlDatabaseConnector(
    config.SQL_DATABASE_HOST,
    config.SQL_DATABASE_PORT,
    config.SQL_DATABASE_USER,
    config.SQL_DATABASE_PASSWORD,
    config.SQL_DATABASE_NAME,
    [tables.CONTRACT_TABLE, tables.TRANSACTION_TABLE]
)

# init execution client
execution_client_url = f"http://{config.EXECUTION_CLIENT_IP}:{config.EXECUTION_CLIENT_PORT}"
execution_client = ExecutionClientConnector(
    execution_client_url, config.ETHERSCAN_URL, config.ETHERSCAN_API_KEY, sql_db_connector, config.SQL_DATABASE_TABLE_CONTRACT)

# TODO: remove when node is fully synced -> currently used for contract endpoints only
# init infura execution client
infura_execution_client_url = f"{config.INFURA_URL}/{config.INFURA_API_KEY}"
infura_execution_client = ExecutionClientConnector(
    infura_execution_client_url, config.ETHERSCAN_URL, config.ETHERSCAN_API_KEY, sql_db_connector, config.SQL_DATABASE_TABLE_CONTRACT)

# init conensus client
consensus_client = ConsensusClientConnector(
    config.CONSENCUS_CLIENT_IP, config.CONSENSUS_CLIENT_PORT)