from app.casbin.role_definition import ResourceDomainEnum


def get_resource_prefix(domain: ResourceDomainEnum, tenant_id: str) -> str:
    return tenant_id + "/" + domain


def get_resource_id_from_item_id(
    item_id: str, domain: ResourceDomainEnum, tenant_id: str
) -> str:
    return get_resource_prefix(domain=domain, tenant_id=tenant_id) + item_id


def get_item_id_from_resource_id(
    resource_id: str, domain: ResourceDomainEnum, tenant_id: str
) -> str:
    prefix = get_resource_prefix(domain=domain, tenant_id=tenant_id)
    if resource_id.startswith(prefix):
        return resource_id[len(prefix) :]
    else:
        raise Exception(f"resource id {resource_id} not starting with prefix {prefix}")
