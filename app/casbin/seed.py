from typing import Union
from app.models.user import User
from datetime import datetime, timezone
from app.utils.db import get_db
import app.repositories.user as userRepo
import os


def seed_or_get_admin_user() -> User:

    name = os.getenv("ADMIN_USER_NAME", "initial-user")
    email = os.getenv("ADMIN_USER_EMAIL", "initial-user-email")
    id = os.getenv("ADMIN_USER_ID", "initial-iser-id")
    if not id:
        raise Exception("initial admin id not provided")
    actor = User(id=id, name=name, email=email)
    with get_db() as db:
        db_user = userRepo.get_or_create(db=db, user=actor)
        initial_admin_user = User.from_orm(db_user)
    return initial_admin_user
