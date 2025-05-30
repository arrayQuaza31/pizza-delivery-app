from fastapi import FastAPI
# from fastapi_jwt_auth import AuthJWT
from api.auth_routers.auth_routes import auth_router
from api.order_routers.order_routes import order_router
# from api.models import Settings

app = FastAPI()

# @AuthJWT.load_config()
# def get_config():
#     return Settings()

app.include_router(auth_router)
app.include_router(order_router)