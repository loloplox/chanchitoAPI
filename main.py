from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controllers import user_controller, transaction_controller, category_controller
from db.connection import init_db

origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    print("Shutting down database connection...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(user_controller.router, prefix="/api/v1", tags=["user"])
app.include_router(transaction_controller.router, prefix="/api/v1", tags=["transaction"])
app.include_router(category_controller.router, prefix="/api/v1", tags=["category"])
