# -------------------------------------------------------------------------------------------------------------
# Copyright (c) UCARE.AI Pte Ltd. All rights reserved.
# -------------------------------------------------------------------------------------------------------------
from app.casbin.role_definition import ResourceActionsEnum, ResourceRightsEnum
from app.utils.db import get_db
from app.models.schemas.user import UserInJWT
import app.repositories.casbin as CasbinRepo
import uuid
from app.casbin.enforcer import create_casbin_enforcer
import time
from app.casbin.enforcer import Filter


# use click to do soemthing here
ADMIN_USER = UserInJWT(id="admin id", name="admin name", tenant_id="cool_tenant")


def add_policies():
    with get_db() as db:
        a_user_id = str(uuid.uuid4())
        for _ in range(3000):
            a_user_id = str(uuid.uuid4())
            CasbinRepo.create_policy(
                db=db,
                user_id=a_user_id,
                resource_id=f"cool_tenant/test_domain/{a_user_id}",
                right=ResourceRightsEnum.own,
                actor=ADMIN_USER,
            )
    return a_user_id  # return the last user id for test purpose


if __name__ == "__main__":
    user_id = add_policies()
    actor = UserInJWT(id=user_id, name="", tenant_id="cool_tenant")
    casbin_enforcer = create_casbin_enforcer()

    t1 = time.perf_counter()
    casbin_enforcer.load_filtered_policy(filter=Filter(v0=[actor.id]))
    t2 = time.perf_counter()
    print(f"enforcer.load_filter_policy() for a user takes {t2 - t1} seconds")
    casbin_enforcer.enforce(
        actor.id,
        actor.tenant_id,
        f"cool_tenant/test_domain/{actor.id}",
        ResourceActionsEnum.delete,
    )
