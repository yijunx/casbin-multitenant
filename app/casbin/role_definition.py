from enum import Enum


class PolicyTypeEnum(str, Enum):
    """p for policy, g for grouping"""

    p = "p"
    g = "g"


class ResourceDomainEnum(str, Enum):
    """There could be more domains and different kind of admins"""

    datasets = "datasets/"


class RoleEnum(str, Enum):
    """the name of admin to store in casbin table"""

    dataset_admin = "dataset_admin"


class ResourceRightsEnum(str, Enum):
    """one user of one resource can only be one of the below"""

    own = "own"  # user is owner of the user resource
    edit = "edit"
    view = "view"
    admin = "admin_right"  # user is admin


class ResourceActionsEnum(str, Enum):
    """these are the actions"""

    get = "get"
    delete = "delete"
    update = "update"
    share = "share"


resource_right_action_mapping: dict = {
    ResourceRightsEnum.own: {
        ResourceActionsEnum.share,
        ResourceActionsEnum.update,
        ResourceActionsEnum.get,
        ResourceActionsEnum.delete,
    },
    ResourceRightsEnum.edit: {
        ResourceActionsEnum.update,
        ResourceActionsEnum.get,
    },
    ResourceRightsEnum.view: {
        ResourceActionsEnum.get,
    },
    ResourceRightsEnum.admin: {
        # the enforcer custom logic
        # make sures admin can perform action
        # on a group of resources
        ResourceActionsEnum.share,
        ResourceActionsEnum.update,
        ResourceActionsEnum.get,
    },
}
