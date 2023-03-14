from app.execution_client_connector import ExecutionClientConnector
import numpy as np
from datetime import datetime


def evaluate_request_time_get_block(execution_client: ExecutionClientConnector, block_sample: list, full_transactions: bool = False):
    request_time_list = []

    for block_identifier in block_sample:
        # measure time
        start_time = datetime.now()
        execution_client.get_block(block_identifier, full_transactions)
        request_time_list.append((datetime.now() - start_time).total_seconds())

    return __evaluate_request_time(request_time_list, "get_block")


def evaluate_request_time_get_transaction(execution_client: ExecutionClientConnector, transaction_sample: list):
    request_time_list = []

    for transaction_hash in transaction_sample:
        # measure time
        start_time = datetime.now()
        execution_client.get_transaction(transaction_hash)
        request_time_list.append((datetime.now() - start_time).total_seconds())

    return __evaluate_request_time(request_time_list, "get_transaction")


def __evaluate_request_time(request_time_list: list, method: str):
    min_request_time = 1000
    max_request_time = 0

    for request_time in request_time_list:
        # set min request time
        if request_time < min_request_time:
            min_request_time = request_time
        # set max request time
        if request_time > max_request_time:
            max_request_time = request_time

    average_request_time = np.average(request_time_list)

    percentile_95 = np.percentile(request_time_list, 95)

    percentile_99 = np.percentile(request_time_list, 99)

    return {
        "method": method,
        "min_request_time": min_request_time,
        "max_request_time": max_request_time,
        "average_request_time": average_request_time,
        "95th_percentile": percentile_95,
        "99th_percentile": percentile_99
    }
