class OIDCError(Exception):
    pass

class OIDCStateError(OIDCError):
    pass

class OIDCTokenError(OIDCError):
    pass

class OIDCUserinfoError(OIDCError):
    pass
