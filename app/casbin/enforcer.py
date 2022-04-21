import casbin_sqlalchemy_adapter
import casbin
from app.casbin.resource_id_converter import get_resource_id_from_item_id
from app.models.schemas.user import UserInJWT
from app.utils.config import configurations as conf
from app.casbin.role_definition import (
    ResourceRightsEnum,
    ResourceDomainEnum,
    resource_right_action_mapping,
    RoleEnum,
)
from app.models.exceptions.casbin import CasbinNotAuthorised
import app.repositories.casbin as CasbinRepo
from app.utils.db import get_db
from typing import List


def create_casbin_enforcer(actor: UserInJWT):
    """this enforcer preloads the policies for the actor"""
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
        if object_from_request.startswith(object_from_policy):
            return True
        else:
            return object_from_request == object_from_policy

    casbin_enforcer.add_function("actions_mapping", actions_mapping)
    casbin_enforcer.add_function("objects_mapping", objects_mapping)
    casbin_enforcer.load_filtered_policy(filter=Filter(v0=[actor.id]))
    return casbin_enforcer


def make_sure_policy_is_there(admin_actor: UserInJWT):
    """This function make sure the admin actor has the access to a domain of his
    tenancy
    """
    with get_db() as db:
        # try:
        #     print(
        #         f"Trying adding policy for the admin for tenant {admin_actor.tenant_id}"
        #     )
        #     CasbinRepo.create_policy(
        #         db=db,
        #         resource_id=admin_actor.tenant_id + "/",
        #         user_id=RoleEnum.admin,
        #         right=ResourceRightsEnum.admin,
        #         actor=admin_actor,  # no su
        #     )
        #     print("Done")
        # except Exception:
        #     print("Permission already added")

        try:
            print(
                f"Trying adding grouping for admin user {admin_actor.id} to admin group"
            )
            CasbinRepo.create_grouping(
                db=db,
                user_id=admin_actor.id,
                role_name=RoleEnum.admin,
                actor=admin_actor,
            )
            print("Done")
        except Exception:
            print("Permission already added")


def resource_exits(resource_id: str) -> bool:
    """This function make sure the admin actor has the access to a domain of his
    tenancy
    """
    with get_db() as db:
        print("checking if the resource is valid...")
        policies = CasbinRepo.get_all_policies_of_resource(
            db=db, resource_id=resource_id
        )
    return bool(policies)


class Filter:
    def __init__(self, v0: List[str], v1: List[str] = None) -> None:
        self.ptype = []
        self.v0 = v0  # the only setup
        self.v1 = v1 if v1 is not None else []
        self.v2 = []
        self.v3 = []
        self.v4 = []
        self.v5 = []


def enforce(
    actor: UserInJWT, action: str, item_id: str, domain: ResourceDomainEnum
) -> None:
    """just raise error if not ok, does not return anything"""
    resource_id = get_resource_id_from_item_id(
        item_id=item_id, domain=domain, tenant_id=actor.tenant_id
    )

    # everytime a new enforcer needs to be created
    casbin_enforcer = create_casbin_enforcer(actor=actor)

    if actor.is_admin:
        print("now we have an admin..")
        # check if policy for admin of the tenant has been created...
        # make_sure_policy_is_there(admin_actor=actor)

        # ORG 2/items/f35a7b4d-8e22-4d05-b2ba-afa959de080f
        # items/ORG-1/ffff <- upon creation..
        # items/
        # also need to make sure if the resource is there
        if not resource_exits(resource_id=resource_id):
            raise CasbinNotAuthorised(
                actor=actor, resource_id=resource_id, action=action
            )
        # and check if the action is ok
        if action not in resource_right_action_mapping[ResourceRightsEnum.admin]:
            raise CasbinNotAuthorised(
                actor=actor, resource_id=resource_id, action=action
            )
    #     sub = RoleEnum.admin
    # else:
    #     sub = actor.id
    else:  # the actor is not admin
        casbin_enforcer.load_filtered_policy(filter=Filter(v0=[actor.id]))

        print("REQUEST: ", actor.id, actor.tenant_id, resource_id, action)
        verdict = casbin_enforcer.enforce(
            actor.id, actor.tenant_id, resource_id, action
        )

        if verdict is False:
            raise CasbinNotAuthorised(
                actor=actor, resource_id=resource_id, action=action
            )
