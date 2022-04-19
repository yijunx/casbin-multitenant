import casbin_sqlalchemy_adapter
import casbin
from app.utils.config import configurations as conf
from app.casbin.role_definition import (
    ResourceRightsEnum,
    ResourceDomainEnum,
    resource_right_action_mapping,
)
from app.models.exceptions.casbin import CasbinRuleDoesNotExist
import app.repositories.casbin as CasbinRepo

# from app.casbin.seed import seed_or_get_admin_user
from app.utils.db import get_db

# from app.utils.app_logging import getLogger
from app.casbin.seed import seed_or_get_admin_user


# logger = getLogger(__name__)


def create_casbin_enforcer():
    adapter = casbin_sqlalchemy_adapter.Adapter(conf.DATABASE_URI)
    casbin_enforcer = casbin.Enforcer("app/casbin/model.conf", adapter)

    def actions_mapping(
        action_from_request: str, resource_right_from_policy: str
    ) -> bool:
        """
        actions are get download patch share...
        resource_right are own / edit / view
        """
        if resource_right_from_policy in resource_right_action_mapping:
            if (
                action_from_request
                in resource_right_action_mapping[resource_right_from_policy]
            ):
                return True
        return False

    def objects_mapping(object_from_request: str, object_from_policy: str) -> bool:
        """
        admin users will have * in obj in the admin role policy, so admin user can
        do things on any resource
        """
        # shall we use startswith? what is the complexity here
        # ????
        if object_from_request.startswith(object_from_policy):
            return True
        else:
            return object_from_request == object_from_policy

    casbin_enforcer.add_function("actions_mapping", actions_mapping)
    casbin_enforcer.add_function("objects_mapping", objects_mapping)
    # this makes admin can perform all actions on item domain resources
    # here the item admin role is defined

    # well there will be no initial admin user now...
    initial_admin_user = seed_or_get_admin_user()
    # well its also good to do it..
    # the initial admin...
    with get_db() as db:

        try:
            CasbinRepo.get_grouping(
                db=db, role_id=conf.ITEM_ADMIN_ROLE_ID, user_id=initial_admin_user.id
            )
        except CasbinRuleDoesNotExist:
            try:
                print("Trying adding initial admin to item admin role")
                CasbinRepo.create_grouping(
                    db=db,
                    user_id=initial_admin_user.id,
                    role_id=conf.ITEM_ADMIN_ROLE_ID,
                    actor=initial_admin_user,
                )
                print("Done")
            except Exception:
                print("Initial user already added to item admin role")

        try:
            # check for this tenant, is there a admin already
            # if not, add his permission
            CasbinRepo.get_policy(
                db=db,
                resource_id=ResourceDomainEnum.items,
                user_id=conf.ITEM_ADMIN_ROLE_ID,
            )
        except CasbinRuleDoesNotExist:
            try:
                print("Trying adding permission of items to item admin role")
                CasbinRepo.create_policy(
                    db=db,
                    resource_id=ResourceDomainEnum.items,
                    user_id=conf.ITEM_ADMIN_ROLE_ID,
                    right=ResourceRightsEnum.admin,
                    actor=initial_admin_user,  # no su
                )
                print("Done")
            except Exception:
                print("Permission already added")
    return casbin_enforcer


casbin_enforcer = create_casbin_enforcer()
