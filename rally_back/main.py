"""
This file contains the fastapi main
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from database.db import engine, Base
from routes import (
    authent_routes,
    banned_users_routes,
    comment_routes,
    event_routes,
    like_routes,
    payment_routes,
    profile_routes,
    reason_routes,
    registration_routes,
    signaled_comment_routes,
    signaled_event_routes,
    signaled_user_routes,
    super_admin_routes,
    type_routes,
    user_routes,
    pictures_routes
)

load_dotenv()

FRONT_HOST = os.getenv("RALLY_FRONT_HOST", "http://localhost:3000")

Base.metadata.create_all(bind=engine)


## GET SQL SCRIPT
# from sqlalchemy.schema import CreateTable
# with open("create_schema.sql", "w") as f:
#     for table in Base.metadata.sorted_tables:
#         f.write(str(CreateTable(table).compile(engine)) + ";\n\n")

app = FastAPI()

origins = [
    FRONT_HOST
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],
)

app.include_router(authent_routes.router)
app.include_router(user_routes.router)
app.include_router(profile_routes.router)
app.include_router(reason_routes.router)
app.include_router(signaled_user_routes.router)
app.include_router(super_admin_routes.router)
app.include_router(event_routes.router)
app.include_router(type_routes.router)
app.include_router(like_routes.router)
app.include_router(comment_routes.router)
app.include_router(signaled_comment_routes.router)
app.include_router(signaled_event_routes.router)
app.include_router(registration_routes.router)
app.include_router(banned_users_routes.router)
app.include_router(payment_routes.router)
app.include_router(pictures_routes.router)

# Démarrage du serveur
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True,
                ssl_certfile="certs/127.0.0.1.pem",
                ssl_keyfile="certs/127.0.0.1-key.pem")
