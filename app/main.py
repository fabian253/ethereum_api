from fastapi import FastAPI, HTTPException, status, Request
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

import app.api_params.api_metadata as api_metadata
from app.endpoints import AuthRouter, MainnetStateRouter, MainnetHistoryRouter, SmartContractRouter, BeaconChainRouter, NodeStateRouter, EvaluationRouter

# init FastAPI
app = FastAPI(
    title=api_metadata.API_TITLE,
    description=api_metadata.API_DESCIPTION,
    version=api_metadata.API_VERSION,
    contact={
        "name": api_metadata.API_CONTACT_NAME,
        "email": api_metadata.API_CONTACT_EMAIL
    },
    openapi_tags=api_metadata.API_TAGS_METADATA,
    docs_url=None,
    redoc_url=None
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# include routers
app.include_router(AuthRouter.router)
app.include_router(MainnetStateRouter.router)
app.include_router(MainnetHistoryRouter.router)
app.include_router(SmartContractRouter.router)
app.include_router(BeaconChainRouter.router)
NodeStateRouter.router.include_router(NodeStateRouter.execution_client_router)
NodeStateRouter.router.include_router(NodeStateRouter.consensus_client_router)
app.include_router(NodeStateRouter.router)
app.include_router(EvaluationRouter.router)


# root

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# docs

@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(req: Request) -> HTMLResponse:
    root_path = req.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + app.openapi_url
    oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
    if oauth2_redirect_url:
        oauth2_redirect_url = root_path + oauth2_redirect_url

    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=api_metadata.API_TITLE,
        oauth2_redirect_url=oauth2_redirect_url,
        init_oauth=app.swagger_ui_init_oauth,
        swagger_favicon_url="/static/favicon.ico",
        swagger_ui_parameters=api_metadata.API_SWAGGER_UI_PARAMETERS
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_ui_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=api_metadata.API_TITLE,
        redoc_favicon_url="/static/favicon.ico"
    )


# catch all unknown routes

@ app.route("/{full_path:path}")
async def catch_all_unknown_routes(full_path: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found",
    )
