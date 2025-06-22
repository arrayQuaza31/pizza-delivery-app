from fastapi import FastAPI
from contextlib import asynccontextmanager

# from fastapi_jwt_auth import AuthJWT
from api.user_routes import user_router
from api.order_routes import order_router

# from api.models import Settings
from database.init_db import init_db_models
from database.redis import test_redis_connection, close_redis_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    await init_db_models()
    await test_redis_connection()
    yield
    await close_redis_connection()
    print("Server has been stopped")


app = FastAPI(
    title="Pizza Delivery App",
    description="A simple REST API app for pizza delivery service",
    version="0.1.0",
    lifespan=lifespan,
)


# @app.get("/")
# def test():
#     return {"message": "working"}


# @AuthJWT.load_config()
# def get_config():
#     return Settings()


version = "v1"
app.include_router(
    router=user_router,
    prefix=f"/api/{version}/auth",
    tags=["auth"],
)
app.include_router(
    router=order_router,
    prefix=f"/api/{version}/orders",
    tags=["orders"],
)
