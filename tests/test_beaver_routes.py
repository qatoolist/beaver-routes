from http import HTTPStatus

import pytest

from beaver_routes.core.base_route import BaseRoute
from beaver_routes.core.hook import Hook
from beaver_routes.core.meta import Meta

BASE_URL = "https://reqres.in/api"


class GetUsersRoute(BaseRoute):
    """Route class for getting users.

    This class demonstrates how to customize a GET route.

    Methods:
        __get__(meta: Meta, hooks: Hook) -> None:
            Customize the GET-specific meta and hooks.
    """

    def __init__(self) -> None:
        """Initialize the GetUsersRoute with the users endpoint."""
        super().__init__(f"{BASE_URL}/users")

    def __get__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the GET-specific meta and hooks for this route.

        Args:
            meta (Meta): The GET request metadata.
            hooks (Hook): The GET request hooks.

        Example:
            >>> route = GetUsersRoute()
            >>> route.__get__(Meta(), Hook())
        """
        pass


class CreateUserRoute(BaseRoute):
    """Route class for creating a user.

    This class demonstrates how to customize a POST route.

    Methods:
        __post__(meta: Meta, hooks: Hook) -> None:
            Customize the POST-specific meta and hooks.
    """

    def __init__(self) -> None:
        """Initialize the CreateUserRoute with the users endpoint."""
        super().__init__(f"{BASE_URL}/users")

    def __post__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the POST-specific meta and hooks for this route.

        Args:
            meta (Meta): The POST request metadata.
            hooks (Hook): The POST request hooks.

        Example:
            >>> route = CreateUserRoute()
            >>> route.__post__(Meta(), Hook())
        """
        meta.json = {"name": "morpheus", "job": "leader"}


class UpdateUserRoute(BaseRoute):
    """Route class for updating a user.

    This class demonstrates how to customize a PUT route.

    Methods:
        __put__(meta: Meta, hooks: Hook) -> None:
            Customize the PUT-specific meta and hooks.
    """

    def __init__(self, user_id: int) -> None:
        """Initialize the UpdateUserRoute with the user-specific endpoint.

        Args:
            user_id (int): The ID of the user to update.
        """
        super().__init__(f"{BASE_URL}/users/{user_id}")

    def __put__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the PUT-specific meta and hooks for this route.

        Args:
            meta (Meta): The PUT request metadata.
            hooks (Hook): The PUT request hooks.

        Example:
            >>> route = UpdateUserRoute(2)
            >>> route.__put__(Meta(), Hook())
        """
        meta.json = {"name": "morpheus", "job": "zion resident"}


class DeleteUserRoute(BaseRoute):
    """Route class for deleting a user.

    This class demonstrates how to customize a DELETE route.

    Methods:
        __delete__(meta: Meta, hooks: Hook) -> None:
            Customize the DELETE-specific meta and hooks.
    """

    def __init__(self, user_id: int) -> None:
        """Initialize the DeleteUserRoute with the user-specific endpoint.

        Args:
            user_id (int): The ID of the user to delete.
        """
        super().__init__(f"{BASE_URL}/users/{user_id}")

    def __delete__(self, meta: Meta, hooks: Hook) -> None:
        """Customize the DELETE-specific meta and hooks for this route.

        Args:
            meta (Meta): The DELETE request metadata.
            hooks (Hook): The DELETE request hooks.

        Example:
            >>> route = DeleteUserRoute(2)
            >>> route.__delete__(Meta(), Hook())
        """
        pass


@pytest.mark.asyncio  # type: ignore
async def test_get_users() -> None:
    """Test the GetUsersRoute async GET request.

    This test verifies that the GET request to the GetUsersRoute returns a 200 status code
    and contains the expected data.

    Example:
        >>> await test_get_users()
    """
    route = GetUsersRoute()
    response = await route.async_get()
    assert response.status_code == HTTPStatus.OK
    assert "data" in response.json_content


@pytest.mark.asyncio  # type: ignore
async def test_create_user() -> None:
    """Test the CreateUserRoute async POST request.

    This test verifies that the POST request to the CreateUserRoute returns a 201 status code
    and contains the expected data.

    Example:
        >>> await test_create_user()
    """
    route = CreateUserRoute()
    response = await route.async_post()
    assert response.status_code == HTTPStatus.CREATED
    json_response = response.json_content
    assert "id" in json_response
    assert "createdAt" in json_response


@pytest.mark.asyncio  # type: ignore
async def test_update_user() -> None:
    """Test the UpdateUserRoute async PUT request.

    This test verifies that the PUT request to the UpdateUserRoute returns a 200 status code
    and contains the expected data.

    Example:
        >>> await test_update_user()
    """
    route = UpdateUserRoute(user_id=2)
    response = await route.async_put()
    assert response.status_code == HTTPStatus.OK
    json_response = response.json_content
    assert "updatedAt" in json_response


@pytest.mark.asyncio  # type: ignore
async def test_delete_user() -> None:
    """Test the DeleteUserRoute async DELETE request.

    This test verifies that the DELETE request to the DeleteUserRoute returns a 204 status code.

    Example:
        >>> await test_delete_user()
    """
    route = DeleteUserRoute(user_id=2)
    response = await route.async_delete()
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_sync_get_users() -> None:
    """Test the GetUsersRoute sync GET request.

    This test verifies that the GET request to the GetUsersRoute returns a 200 status code
    and contains the expected data.

    Example:
        >>> test_sync_get_users()
    """
    route = GetUsersRoute()
    response = route.get()
    assert response.status_code == HTTPStatus.OK
    assert "data" in response.json_content


def test_sync_create_user() -> None:
    """Test the CreateUserRoute sync POST request.

    This test verifies that the POST request to the CreateUserRoute returns a 201 status code
    and contains the expected data.

    Example:
        >>> test_sync_create_user()
    """
    route = CreateUserRoute()
    response = route.post()
    assert response.status_code == HTTPStatus.CREATED
    json_response = response.json_content
    assert "id" in json_response
    assert "createdAt" in json_response


def test_sync_update_user() -> None:
    """Test the UpdateUserRoute sync PUT request.

    This test verifies that the PUT request to the UpdateUserRoute returns a 200 status code
    and contains the expected data.

    Example:
        >>> test_sync_update_user()
    """
    route = UpdateUserRoute(user_id=2)
    response = route.put()
    assert response.status_code == HTTPStatus.OK
    json_response = response.json_content
    assert "updatedAt" in json_response


def test_sync_delete_user() -> None:
    """Test the DeleteUserRoute sync DELETE request.

    This test verifies that the DELETE request to the DeleteUserRoute returns a 204 status code.

    Example:
        >>> test_sync_delete_user()
    """
    route = DeleteUserRoute(user_id=2)
    response = route.delete()
    assert response.status_code == HTTPStatus.NO_CONTENT
