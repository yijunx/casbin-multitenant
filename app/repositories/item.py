from typing import List, Tuple, Union
from app.models.sqlalchemy.models import Item
from app.models.schemas.item import ItemCreate, ItemPatch, ItemQuery
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.pagination import ResponsePagination
from app.repositories.util import translate_query_pagination
import uuid


def create(db: Session, item_create: ItemCreate, actor: User) -> Item:
    """ """
    db_item = Item(
        id=str(uuid.uuid4()),
        name=item_create.name,
        desc=item_create.desc,
        content=item_create.content,
        created_by=actor.id,
    )
    db.add(db_item)
    # here we can try flush, and catch the integrity
    # error if there are unique contraints in the model
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise Exception("item already there")
    return db_item


def get(db: Session, item_id: str) -> Item:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise Exception("item not there")
    return db_item


def delete(db: Session, item_id: str) -> None:
    db_item = get(db=db, item_id=item_id)
    db.delete(db_item)


def get_by_name(db: Session, item_name: str) -> Union[Item, None]:
    db_item = db.query(Item).filter(Item.name == item_name).first()
    return db_item


def get_all(
    db: Session, query_pagination: ItemQuery, admin_access: bool, item_ids: List[str]
) -> Tuple[List[Item], ResponsePagination]:

    query = db.query(Item)

    if not admin_access:
        # if there is no admin access, this user can only see what
        # he created or shared to
        query = query.filter(Item.id.in_(item_ids))

    if query_pagination.name:
        query = query.filter(Item.name.contains(query_pagination.name))

    total = query.count()
    limit, offset, paging = translate_query_pagination(
        total=total, query_pagination=query_pagination
    )
    db_items = query.order_by(Item.name.desc()).limit(limit).offset(offset)
    return db_items, paging


def update(db: Session, item_id: str, item_patch: ItemPatch, actor: User) -> Item:
    """used for update item"""
    db_item = get(db=db, item_id=item_id)
    db_item.name = item_patch.name or db_item.name
    db_item.desc = item_patch.desc or db_item.desc
    db_item.content = item_patch.content or db_item.content
    # logs the action
    # db_item.modified_at = datetime.now(timezone.utc)
    # db_item.modified_by = actor.id
    return db_item
