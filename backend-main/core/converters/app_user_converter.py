from core.dto.app_user_dto import AppUserDTO, AppUserUpsertDTO
from core.models import AppUser


def app_user_model_to_dto(obj: AppUser) -> AppUserDTO:
    return AppUserDTO(
        id=obj.id,
        nni=obj.nni,
        first_name=obj.first_name,
        last_name=obj.last_name,
        email=obj.email,
        role=obj.role,
        is_active=obj.is_active,
        last_login_at=obj.last_login_at,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
    )


def app_user_upsert_dto_to_fields(dto: AppUserUpsertDTO) -> dict:
    return {
        "nni": dto.nni,
        "first_name": dto.first_name,
        "last_name": dto.last_name,
        "email": dto.email,
        "role": dto.role,
        "is_active": dto.is_active,
        "last_login_at": dto.last_login_at,
    }
