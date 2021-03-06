from sqlalchemy import (
    Column,
    String,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.sql.sqltypes import BigInteger
from app.models.sqlalchemy.base import Base


class CasbinRule(Base):
    __tablename__ = "casbin_rule"
    __table_args__ = (UniqueConstraint("v0", "v1", "v2", name="_v0_v1_uc"),)
    id = Column(BigInteger, autoincrement=True, primary_key=True, index=True)
    ptype = Column(String, nullable=False)
    v0 = Column(
        String, nullable=True, index=True
    )  # user id or role name, the sub, index for faster obtain the wanted policies
    v1 = Column(String, nullable=True)  # role name if g, tenant id if p
    v2 = Column(String, nullable=True, index=True)  # tenant id if g, resource id if p
    v3 = Column(String, nullable=True)  # empty if g, resource right if p
    v4 = Column(String, nullable=True)  # empty
    v5 = Column(String, nullable=True)  # empty

    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_by = Column(String, nullable=True)
    modified_at = Column(DateTime, nullable=True)


class Item(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, index=True)
    # here we index it so that we can faster find all the resources of that tenant..

    name = Column(String, nullable=False)
    desc = Column(String, nullable=True)
    content = Column(String, nullable=False)
    created_by = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tenant_id = Column(String, nullable=False)

    # and email etc.. not going to add here...
