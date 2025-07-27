from .user_handlers import register_user
from .admin_handlers import register_admin

def register_handlers(dp):
    register_user(dp)
    register_admin(dp)
