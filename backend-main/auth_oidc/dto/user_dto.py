from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class OIDCUserDTO:
    sub: Optional[str]
    uid: Optional[str]
    name: Optional[str]
    givenName: Optional[str]
    sn: Optional[str]
    mail: Optional[str]

    @staticmethod
    def from_userinfo(userinfo: Dict[str, Any]):
        return OIDCUserDTO(
            sub=userinfo.get("sub"),
            uid=userinfo.get("uid"),
            name=userinfo.get("name"),
            givenName=userinfo.get("givenName"),
            sn=userinfo.get("sn"),
            mail=userinfo.get("mail"),
        )
