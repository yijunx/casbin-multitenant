from app.models.schemas.user import UserInJWT


def get_user_info_from_user_management(user_id: str, tenant_id: str) -> UserInJWT:
    """well this is definitely a mock"""
    return UserInJWT(
        id=user_id, name=f"name for {user_id}", email="", tenant_id=tenant_id
    )
