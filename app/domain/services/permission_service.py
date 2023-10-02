from fastapi import HTTPException
from dataclasses import dataclass
from app.api import HTTPStatus
from app.domain.models import Permission

@dataclass
class PermissionService:
    async def my_permissions(self, user_id: int):
        permissions = await self.find_all_user_permissions(user_id)

        if len(permissions) == 0:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT)

        return permissions

    async def find_all_user_permissions(self, user_id: int) -> list[Permission]:
        return await Permission.objects.select_related('users').all(users__id=user_id)