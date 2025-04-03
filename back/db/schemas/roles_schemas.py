from .schemas import RoleBase as Role


class RoleCreate(Role):
    name: str


class RoleUpdate(Role):
    id: int
    name: str


class RoleResponse(Role):
    id: int
    name: str
