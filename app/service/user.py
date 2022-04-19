from app.utils.db import get_db
import app.repositories.user as UserRepo


def delete_user(item_id: str):
    """for test purposes"""
    with get_db() as db:
        UserRepo.delete(db=db, user_id=item_id)


# def patch_user(item_id: str, user_patch: UserPatch):
#     with get_db() as db:
#         db_user = UserRepo.get(db=db, user_id=item_id)
#         if db_user:
#             if user_patch.name:
#                 db_user.name = user_patch.name
#             if user_patch.email:
#                 db_user.email = user_patch.email


# def add_admin_user(user: User, actor: User):
#     with get_db() as db:
#         db_user = UserRepo.get_or_create(db=db, user=user)
#         db_rule = CasbinRepo.create_grouping(
#             db=db, user_id=db_user.id, role_id=conf.ITEM_ADMIN_ROLE_ID, actor=actor
#         )
#         casbin_rule = CasbinGroup(user_id=db_user.id, group_id=db_rule.v1)
#     return casbin_rule


# def remove_admin_user(user_id: str):
#     with get_db() as db:
#         CasbinRepo.delete_grouping(
#             db=db, role_id=conf.ITEM_ADMIN_ROLE_ID, user_id=user_id
#         )


# def get_admin_user(user_id: str) -> CasbinGroup:
#     with get_db() as db:
#         # raises exc if the user is not admin
#         db_rule = CasbinRepo.get_grouping(
#             db=db, role_id=conf.ITEM_ADMIN_ROLE_ID, user_id=user_id
#         )
#         casbin_rule = CasbinGroup(user_id=user_id, group_id=db_rule.v1)
#     return casbin_rule


# def list_admin_user(query_pagination: QueryPagination) -> UserWithPaging:
#     with get_db() as db:
#         db_casbin_rules, paging = CasbinRepo.get_all_grouping(
#             db=db,
#             role_id=conf.ITEM_ADMIN_ROLE_ID,
#             query_pagination=query_pagination,
#         )
#         user_data_dict = UserRepo.get_user_data(
#             db=db, user_ids=[x.v0 for x in db_casbin_rules]
#         )
#         admin_users = [user_data_dict[x.v0] for x in db_casbin_rules]
#     return UserWithPaging(data=admin_users, paging=paging)
