from httpx import AsyncClient

async def test_register_user(client: AsyncClient, user_data: dict):
    response = await client.post(
        "/auth/register", 
        json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@gmail.com"
    assert "hashed_password" not in data
    

async def test_dublicate_email(client: AsyncClient, user_data: dict):
    response = await client.post(
        "/auth/register", 
        json=user_data)
    
    dublicate = await client.post(
        "/auth/register", 
        json=user_data)
    
    assert response.status_code == 200
    assert dublicate.status_code == 409
    
async def test_log_in(client: AsyncClient, user_data: dict):
    response = await client.post(
        "/auth/register", 
        json=user_data) 
    
    assert response.status_code == 200
    
    user = await client.post(
        "/auth/login",
        json={
            "email": response.json()["email"],
            "password": "passwordtest"
        }
    )
    
    assert user.status_code == 200
    data = user.json()
    assert "access_token" in data and "refresh_token" in data
    

async def test_log_in_not_true_password(client: AsyncClient, user_data: dict):
    response = await client.post(
        "/auth/register", 
        json=user_data) 
    
    assert response.status_code == 200
    
    user = await client.post(
        "/auth/login",
        json={
            "email": response.json()["email"],
            "password": "falsepassword"
        }
    )
    
    assert user.status_code == 401
    