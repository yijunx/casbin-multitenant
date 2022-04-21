# -------------------------------------------------------------------------------------------------------------
# Copyright (c) UCARE.AI Pte Ltd. All rights reserved.
# -------------------------------------------------------------------------------------------------------------
from app.casbin.role_definition import ResourceRightsEnum
from app.utils.db import get_db
from app.models.schemas.user import UserInJWT
import app.repositories.casbin as CasbinRepo
import uuid
from app.casbin.enforcer import create_casbin_enforcer
import time
from app.casbin.enforcer import Filter


# use click to do soemthing here


def add_policies():
    with get_db() as db:
        a_user_id = str(uuid.uuid4())
        for _ in range(3000):
            a_user_id = str(uuid.uuid4())
            CasbinRepo.create_policy(
                db=db,
                user_id="non exist user",
                resource_id=f"test_domain/{a_user_id}",
                right=ResourceRightsEnum.own,
                actor=admin_user,
            )
    return a_user_id  # return the last user id for test purpose


if __name__ == "__main__":
    add_policies()
    
    t1 = time.perf_counter()
    casbin_enforcer = create_casbin_enforcer(actor=UserInJWT(), preload_policies=False)
    a_user_id = casbin_enforcer.load_policy()
    t2 = time.perf_counter()
    print(f"enforcer.load_policy() takes {t2 - t1} seconds")

    t1 = time.perf_counter()
    casbin_enforcer = create_casbin_enforcer(actor=UserInJWT(), preload_policies=False)
    casbin_enforcer.load_filtered_policy(
        filter=Filter(v0=[conf.ITEM_ADMIN_ROLE_ID, a_user_id])
    )
    t2 = time.perf_counter()
    print(f"enforcer.load_filter_policy() for a user takes {t2 - t1} seconds")