from typing import Dict, Tuple, List
from app.models.sqlalchemy.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.pagination import QueryPagination, ResponsePagination
from app.models.schemas.user import UserInJWT
from app.repositories.util import translate_query_pagination


def create(db: Session, user: UserInJWT) -> User:
    """
    here the user already create himself
    with data from cookie
    there is no way other people create user for him/her
    """

    # now = datetime.now(timezone.utc)

    db_item = User(
        id=user.id,
        name=user.name,
        tenant_id=user.tenant_id,
    )
    db.add(db_item)
    # db.flush()
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise Exception("user already there")
    return db_item


def delete_all(db: Session) -> None:
    db.query(User).delete()


def delete(db: Session, user_id: str) -> None:
    db_item = db.query(User).filter(User.id == user_id).first()
    if not db_item:
        raise Exception("user does not exist")
    db.delete(db_item)


def get(db: Session, user_id: str) -> User:
    db_item = db.query(User).filter(User.id == user_id).first()
    if not db_item:
        raise Exception("user does not exist")
    return db_item


def get_user_data(db: Session, user_ids: str) -> List[User]:
    db_items = db.query(User).filter(User.id.in_(user_ids))
    return db_items


def get_or_create(db: Session, user: UserInJWT) -> User:
    try:
        db_item = create(db=db, user=user)
    except Exception:
        db_item = db.query(User).filter(User.id == user.id).first()
    return db_item


def get_all(
    db: Session, query_pagination: QueryPagination, user_ids: List[str]
) -> Tuple[List[User], ResponsePagination]:
    """used for get sharees"""
    query = db.query(User)
    query = query.filter(User.id.in_(user_ids))

    total = query.count()
    limit, offset, paging = translate_query_pagination(
        total=total, query_pagination=query_pagination
    )

    db_items = query.order_by(User.name).limit(limit).offset(offset)
    return db_items, paging
