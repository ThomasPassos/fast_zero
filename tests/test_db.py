from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    user = User(username="test", email="test@test.com", password="secret")

    with mock_db_time(model=User) as time:
        session.add(user)
        await session.commit()
        user = await session.scalar(
            select(User).where(User.username == "test")
        )

    assert asdict(user) == {
        "id": 1,
        "username": "test",
        "email": "test@test.com",
        "password": "secret",
        "created_at": time,
        "updated_at": time,
    }
