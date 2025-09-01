import pytest
from httpx import AsyncClient, ASGITransport
from main import app

required_keys = ["status", "title", "description", "uuid"]


@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.post("/tasks/", json={
            "title": "test_title",
            "description": "test_description",
            "status": "создано"
        })
        assert response.status_code == 200
        data = response.json()
        for key in required_keys:
            assert key in data, f"Ключ '{key}' отсутствует в ответе"


@pytest.mark.asyncio
async def test_create_task_error():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.post("/tasks/", json={
            "title": "test_title",
            "description": "test_description",
            "status": "не валидный статус"
        })
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_tasks_status():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/tasks/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_tasks():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/tasks/")

        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_task():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/tasks/")
        data = response.json()
        response_task = await ac.get(f"/task/{data[0]["uuid"]}")
        data_task = response_task.json()
        for key in required_keys:
            assert key in data_task, f"Ключ '{key}' отсутствует в ответе"


@pytest.mark.asyncio
async def test_get_task_error():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response_task = await ac.get(f"/task/bcf98280-5e44-423f-9986-a52")
        assert response_task.status_code == 404


@pytest.mark.asyncio
async def test_edit_task():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/tasks/")
        data = response.json()
        response_task = await ac.put(f"/task/{data[0]["uuid"]}", json={
            "title": "test_title_edit",
            "description": "test_description_edit",
            "status": "в работе"
        })
        data_task = response_task.json()
        for key in required_keys:
            assert key in data_task, f"Ключ '{key}' отсутствует в ответе"
        assert data_task["title"] == "test_title_edit"
        assert data_task["description"] == "test_description_edit"
        assert data_task["status"] == "в работе"


@pytest.mark.asyncio
async def test_edit_task_error():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/tasks/")
        data = response.json()
        response_task = await ac.put(f"/task/{data[0]["uuid"]}", json={
            "title": "test_title_edit",
            "description": "test_description_edit",
            "status": "не валидный статус"
        })
        assert response_task.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_error():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response_delete = await ac.delete(f"/task/bcf98280-5e44-423f-9986-a52")
        assert response_delete.status_code == 404


@pytest.mark.asyncio
async def test_delete_task():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/tasks/")
        data = response.json()
        response_delete = await ac.delete(f"/task/{data[0]['uuid']}")
        assert response_delete.status_code == 200
