import pytest
from app.models.exceptions.casbin import CasbinNotAuthorised
from app.models.pagination import QueryPagination
from app.models.schemas.item import ItemCreate, ItemQuery
import app.service.item as ItemService
from app.models.schemas.user import UserInJWT, UserShare
from app.casbin.role_definition import ResourceRightsEnum


TENANT1 = "ORG 1"
TENANT2 = "ORG 2"

ORG_1_USER_1 = UserInJWT(
    id="org 1 user 1", name="org 1 user 1", tenant_id=TENANT1, roles=[]
)

ORG_1_USER_2 = UserInJWT(
    id="org 1 user 2", name="org 1 user 2", tenant_id=TENANT1, roles=[]
)

ORG_1_ADMIN = UserInJWT(
    id="org 1 admin", name="org 1 admin", tenant_id=TENANT1, roles=["algobox-admin"]
)

ORG_2_USER_1 = UserInJWT(
    id="org 2 user 1", name="org 2 user 1", tenant_id=TENANT2, roles=[]
)

ORG_2_USER_2 = UserInJWT(
    id="org 2 user 2", name="org 2 user 2", tenant_id=TENANT2, roles=[]
)

ORG_2_ADMIN = UserInJWT(
    id="org 2 admin", name="org 2 admin", tenant_id=TENANT2, roles=["algobox-admin"]
)

ITEM_CREATE = ItemCreate(
    name="name of item", desc="desc of item", content="content of item"
)

ITEM_ID_USER1_TENANT1 = ""
ITEM_ID_USER2_TENANT1 = ""
ITEM_ID_USER1_TENANT2 = ""


def test_user1_tenant1_create():
    item = ItemService.create_item(item_create=ITEM_CREATE, actor=ORG_1_USER_1)
    global ITEM_ID_USER1_TENANT1
    ITEM_ID_USER1_TENANT1 = item.id


def test_user1_tenant2_create():
    item = ItemService.create_item(item_create=ITEM_CREATE, actor=ORG_2_USER_1)
    global ITEM_ID_USER1_TENANT2
    ITEM_ID_USER1_TENANT2 = item.id


def test_user1_tenant1_can_get():
    item = ItemService.get_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_USER_1)
    assert item.name == ITEM_CREATE.name


def test_admin_tenant1_can_get():
    item = ItemService.get_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_ADMIN)
    assert item.name == ITEM_CREATE.name


def test_admin_tenant1_cannot_patch():
    with pytest.raises(CasbinNotAuthorised):
        ItemService.patch_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_ADMIN)


def test_user2_tenant1_cannot_get():
    with pytest.raises(CasbinNotAuthorised):
        ItemService.get_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_USER_2)
    with pytest.raises(CasbinNotAuthorised):
        ItemService.get_item(item_id=ITEM_ID_USER2_TENANT1, actor=ORG_1_USER_2)


def test_share_to_user2_tenant1_as_view():
    ItemService.share_item(
        item_id=ITEM_ID_USER1_TENANT1,
        user_share=UserShare(id=ORG_1_USER_2.id, role=ResourceRightsEnum.view),
        actor=ORG_1_USER_1,
    )


def test_user2_tenant1_can_get_after_share_as_view():
    item = ItemService.get_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_USER_2)
    assert item.name == ITEM_CREATE.name


def test_user2_tenant1_cannot_patch():
    with pytest.raises(CasbinNotAuthorised):
        ItemService.patch_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_USER_2)


def test_user2_tenant_create():
    item = ItemService.create_item(item_create=ITEM_CREATE, actor=ORG_1_USER_2)
    global ITEM_ID_USER2_TENANT1
    ITEM_ID_USER2_TENANT1 = item.id


def test_admin_tenant1_list():
    items_with_paging = ItemService.list_items(
        item_query=ItemQuery(), actor=ORG_1_ADMIN
    )
    assert len(items_with_paging.data) == 2


def test_user2_tenant1_list_after_share():
    items_with_paging = ItemService.list_items(
        item_query=ItemQuery(), actor=ORG_1_USER_2
    )
    assert len(items_with_paging.data) == 2


def test_user2_tenant1_list_users_of_item1():
    user_id_to_resource_right_mapping = ItemService.list_sharee_of_item(
        item_id=ITEM_ID_USER1_TENANT1,
        query_pagination=QueryPagination(),
        actor=ORG_1_USER_2,
    )
    # please note that admin is not there...
    # assert user_id_to_resource_right_mapping[ORG_1_ADMIN.id] == ResourceRightsEnum.admin
    assert user_id_to_resource_right_mapping[ORG_1_USER_1.id] == ResourceRightsEnum.own
    assert user_id_to_resource_right_mapping[ORG_1_USER_2.id] == ResourceRightsEnum.view
    assert len(user_id_to_resource_right_mapping) == 2


def test_admin_tenant2_cannot_get():
    with pytest.raises(CasbinNotAuthorised):
        ItemService.get_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_2_ADMIN)


def test_unshare_to_user2():
    ItemService.unshare_item(
        item_id=ITEM_ID_USER1_TENANT1, user_id=ORG_1_USER_2.id, actor=ORG_1_USER_1
    )


def test_user2_tenant1_cannot_get_after_unshare():
    with pytest.raises(CasbinNotAuthorised):
        ItemService.get_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_USER_2)


def test_user1_tenant1_delete():
    ItemService.delete_item(item_id=ITEM_ID_USER1_TENANT1, actor=ORG_1_USER_1)


def test_user2_tenant1_delete():
    ItemService.delete_item(item_id=ITEM_ID_USER2_TENANT1, actor=ORG_1_USER_2)


def test_user1_tenant2_delete():
    ItemService.delete_item(item_id=ITEM_ID_USER1_TENANT2, actor=ORG_2_USER_1)
