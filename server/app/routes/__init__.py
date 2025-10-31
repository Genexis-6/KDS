from .auth.auth import auth
from .class_available.class_endpoint import room

def register_all_routes(app):
    app.include_router(auth)
    
    app.include_router(room)