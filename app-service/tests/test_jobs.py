from httpx import AsyncClient
from unittest.mock import patch

async def test_get_job(client: AsyncClient, auth_token: str):
    response = await client.get(
        "/jobs/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {auth_token}"})
    
    assert response.status_code == 404
    
async def test_create_job(client: AsyncClient, auth_token: str):
    with patch("service.job.celery_app.send_task") as mock_send_task:
        response = await client.post(
            "/jobs/",
            json={"language": "python", "code": "print(1)"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
    assert response.status_code == 200
    mock_send_task.assert_called_once()
    