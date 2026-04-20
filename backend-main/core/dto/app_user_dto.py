from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class AppUserDTO:
  id: int
  nni: str
  first_name: str
  last_name: str
  email: str
  role: str
  is_active: bool
  last_login_at: Optional[datetime]
  created_at: datetime
  updated_at: datetime


@dataclass(frozen=True)
class AppUserUpsertDTO:
  nni: str = ""
  first_name: str = ""
  last_name: str = ""
  email: str = ""
  role: str = ""
  is_active: bool = True
  last_login_at: Optional[datetime] = None