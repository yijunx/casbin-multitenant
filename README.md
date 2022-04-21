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
- This app works statelessly. Everytime a service function is triggered, the casbin enforcer reloads policies.
- When the service sees an admin user, it wont go through the normal casbin, but allow him to access all resources in his domain, just check his action only.


### To finish as a full flask app
- Need apis layer
- Need auth layer and add this casbin enforcer
- Need to save the user info into the user tables


### Set up and test

```bash
# open in devcontainer first
make test
```

- The test will record time for top a few slowest operations to check performance
- All tests are in tests/test_service/test_service.py, they will trigger the repo layer thus the coverage is quite high.
- The test covers the situation of 2 tenants, with admin, and see if all operations have intended result. All stuff created in the tests will be deleted at last.

### Load test

```bash
# open in devcontainer first
python load_policy_test.py
```

Each time adds 3000 policies, and see the time spent in load policy for the user. We can also add like 12000 policies then run `make test` to see the performance of other stuff when there are a lot of policies in db.