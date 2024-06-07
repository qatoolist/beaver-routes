# tests/test_beaver_routes.py
import httpx
import pytest
from beaver_routes.core.base_route import BaseRoute
from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta

BASE_URL = "https://reqres.in/api"


class GetUsersRoute(BaseRoute):
    def __init__(self):
        super().__init__(f"{BASE_URL}/users")


class CreateUserRoute(BaseRoute):
    def __init__(self):
        super().__init__(f"{BASE_URL}/users")

    def __post__(self, meta: Meta, hooks: Hook) -> None:
        meta.data = {"name": "morpheus", "job": "leader"}


class UpdateUserRoute(BaseRoute):
    def __init__(self, user_id: int):
        super().__init__(f"{BASE_URL}/users/{user_id}")

    def __put__(self, meta: Meta, hooks: Hook) -> None:
        meta.data = {"name": "morpheus", "job": "zion resident"}


class DeleteUserRoute(BaseRoute):
    def __init__(self, user_id: int):
        super().__init__(f"{BASE_URL}/users/{user_id}")


@pytest.mark.asyncio
async def test_get_users():
    route = GetUsersRoute()
    response = await route.async_get()
    assert response.status_code == 200
    assert "data" in response.json()


@pytest.mark.asyncio
async def test_create_user():
    route = CreateUserRoute()
    response = await route.async_post()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["name"] == "morpheus"
    assert json_response["job"] == "leader"


@pytest.mark.asyncio
async def test_update_user():
    route = UpdateUserRoute(user_id=2)
    response = await route.async_put()
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == "morpheus"
    assert json_response["job"] == "zion resident"


@pytest.mark.asyncio
async def test_delete_user():
    route = DeleteUserRoute(user_id=2)
    response = await route.async_delete()
    assert response.status_code == 204


# For synchronous tests
def test_sync_get_users():
    route = GetUsersRoute()
    response = route.get()
    assert response.status_code == 200
    assert "data" in response.json()


def test_sync_create_user():
    route = CreateUserRoute()
    response = route.post()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["name"] == "morpheus"
    assert json_response["job"] == "leader"


def test_sync_update_user():
    route = UpdateUserRoute(user_id=2)
    response = route.put()
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == "morpheus"
    assert json_response["job"] == "zion resident"


def test_sync_delete_user():
    route = DeleteUserRoute(user_id=2)
    response = route.delete()
    assert response.status_code == 204
