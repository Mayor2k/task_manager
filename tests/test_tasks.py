from httpx import AsyncClient
    
async def test_error_add_task(ac: AsyncClient):
    response = await ac.post("/api/task/", json={
        "user_id": 1,
        "description": "test description"
    })
    assert response.status_code == 404
    
    
async def test_get_task_list(ac: AsyncClient):
    response = await ac.get("/api/tasks/")
    assert response.status_code == 200
