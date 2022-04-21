# casbin-multitenant
This repo shows how to manage RBAC with casbin

### Objective
- User can create an item and share to another user in the same tenant
- There needs to be multiple level of resource right to an item, a user will have one right to an item.
- User will not have access to resources created by any other users, if not shared to.
- Admin user of a tenant has admin-right to all items belonging to this tenant. What can admin-right do can be updated without changing the database.
- no information sharing across tenants

### Details

- The resource rights to actions relation in this example is specified like this in `app/casbin/role_definition.py`

    ```python
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
            ResourceActionsEnum.get,
            # it shows that admin cannot patch or delete, they can only see and share, in this example..
        },
    }

    ```
- In above example, we can see that there are 4 resource rights, they are
    - own, can perform actions like share/update/get/delete
    - edit, can perform actions like update/get
    - view, can perform actions like get
    - admin, can perform actions like share/get
- The setup of casbin can tell from `app/casbin/model.conf`
- This app works statelessly. Everytime a service function is triggered, a new casbin enforcer will need to load policies.


### To finish as a full flask app
- Need apis layer
- Need auth layer and add this casbin enforcer
- Need to save the user info into the user tables


### Set up and test

```bash
# open in devcontainer first
make test
```

- Can add more tests to tests/test_service/test_service.py