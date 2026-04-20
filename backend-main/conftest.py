import pytest
from core.models import AppUser


@pytest.fixture
def app_user(db):
    return AppUser.objects.create(
        nni="a30481",
        first_name="Test",
        last_name="User",
        email="test@edf.fr",
        role="READ_ONLY",
        is_active=True,
    )


@pytest.fixture
def admin_user(db):
    return AppUser.objects.create(
        nni="admin01",
        first_name="Admin",
        last_name="User",
        email="admin@edf.fr",
        role="ADMIN",
        is_active=True,
    )