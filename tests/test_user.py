from httpx import AsyncClient
import pytest
from dataclasses import asdict
from app.model.request.register_user import RegisterUser


@pytest.mark.anyio
async def test_register_user_success(client: AsyncClient):
    json = asdict(
        RegisterUser(
            name="Vaibhav Goyal",
            about="",
            profile_image_url="",
            phone_number="+91 8847568693",
        )
    )

    response = await client.post("/api/v1/user/register", json=json)

    assert response.status_code == 200
