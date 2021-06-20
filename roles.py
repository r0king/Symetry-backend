from enum import Enum


class Roles(Enum):
    """
    The role enum
    """
    ADMIN = "ADMIN"
    APP = "APP"
    USER = "USER"


hierarchy = {
    Roles.ADMIN: 2,
    Roles.APP: 1,
    Roles.USER: 0
}
