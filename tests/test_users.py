from httpx import AsyncClient
    
async def test_success_add_user(ac: AsyncClient):
    response = await ac.post("/api/users/", json={
        "email": "dsa@sca.com",
        "first_name": "test",
        "last_name": "bond",
        "gender": "male",
        "password": "lalalallaalla213",
    })
    assert response.status_code == 201
    
async def test_error_email_add_user(ac: AsyncClient):
    response = await ac.post("/api/users/", json={
        "email": "dsa@sca",
        "first_name": "test",
        "last_name": "bond",
        "gender": "male",
        "password": "lalalallaalla213",
    })
    assert response.status_code == 400
    
async def test_error_password_add_user(ac: AsyncClient):
    response = await ac.post("/api/users/", json={
        "email": "dsa@sca",
        "first_name": "test",
        "last_name": "bond",
        "gender": "male",
        "password": "ldld",
    })
    assert response.status_code == 400
    
async def test_get_user_list(ac: AsyncClient):
    response = await ac.get("/api/users/")
    assert response.status_code == 200
