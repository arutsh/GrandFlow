"""
Tests for UserRole enum validation (P5).

The DB check constraint (users_role_check) enforces this at the DB level.
These tests verify the schema layer rejects invalid roles before they reach the DB.
"""
import pytest
from pydantic import ValidationError

from shared.schemas.user_schema import UserRole, UserCreate, UserStatus


def _valid_payload(**overrides) -> dict:
    base = {
        "email": "test@example.com",
        "role": UserRole.user,
        "status": UserStatus.pending,
    }
    base.update(overrides)
    return base


class TestUserRoleEnum:
    def test_user_role_is_valid(self):
        assert UserRole("user") == UserRole.user

    def test_superuser_role_is_valid(self):
        assert UserRole("superuser") == UserRole.superuser

    def test_invalid_role_raises(self):
        with pytest.raises(ValueError):
            UserRole("admin")

    def test_invalid_role_uppercase_raises(self):
        with pytest.raises(ValueError):
            UserRole("Superuser")


class TestUserCreateRoleValidation:
    def test_valid_user_role_accepted(self):
        user = UserCreate(**_valid_payload(role="user"))
        assert user.role == UserRole.user

    def test_valid_superuser_role_accepted(self):
        user = UserCreate(**_valid_payload(role="superuser"))
        assert user.role == UserRole.superuser

    def test_invalid_role_rejected_by_schema(self):
        with pytest.raises(ValidationError):
            UserCreate(**_valid_payload(role="admin"))

    def test_invalid_role_empty_string_rejected(self):
        with pytest.raises(ValidationError):
            UserCreate(**_valid_payload(role=""))
