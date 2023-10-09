from fastapi import HTTPException
from dataclasses import dataclass
from app.api import HTTPStatus
from app.domain.models import Permission

@dataclass
class PermissionService:
    async def find_all(self) -> list[Permission]:
        all_permissions: list[Permission] = Permission.objects.all()

        if len(all_permissions) == 0:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT)

        return all_permissions

    async def my_permissions(self, user_id: int):
        permissions = await self.find_all_user_permissions(user_id)

        if len(permissions) == 0:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT)

        return permissions

    async def find_all_user_permissions(self, user_id: int) -> list[Permission]:
        return await Permission.objects.select_related('users').all(users__id=user_id)
    
    async def verify_user_permission(self, user_id: int, role: str) -> None:
        permissions: list[Permission] = await self.find_all_user_permissions(user_id)
        user_roles: list[str] = [permission.role for permission in permissions]

        if role not in user_roles:
            raise HTTPException(detail='Você não tem permissão para acessar esse recurso.', status_code=HTTPStatus.FORBIDDEN)
        