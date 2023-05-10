# __init__.py
from .auth import router as AuthRouter
from .mainnet_state import router as MainnetStateRouter
from .mainnet_history import router as MainnetHistoryRouter
from .smart_contract import router as SmartContractRouter
from .beacon_chain import router as BeaconChainRouter
from .node_state import router as NodeStateRouter
from .evaluation import router as EvaluationRouter
