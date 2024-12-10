# example.py
from src.server import run_server
from src.routing.decorators import route, group
from src.routing.response import Response
from src.routing.router import Router
from src.routing.cors import CORSMiddleware
from src.routing.middleware import HTTPSMiddleware, Middleware
from src.exceptions_manager import ExceptionsManager
from src.routing.exceptions import HttpNotFoundException

router = Router.get_instance()
exceptions_manager = ExceptionsManager()
router.set_exceptions_manager(exceptions_manager)

# Custom 404 handler
def handle_not_found(exc, request):
    return Response(status=404, body="This page was not found!")
exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

class LoggingMiddleware(Middleware):
    def handle_pre(self, request):
        print(f"[LoggingMiddleware] Request for path: {request.path}")
        return None

# Global middlewares
# CORS for all routes
router.use_global_middleware(CORSMiddleware())
# Logging for all routes

# Force global HTTPS off
router.force_https(False)

@route("/json-logged", methods=["GET"], middlewares=[LoggingMiddleware()])
def json_logged_route(request):
    # This route uses LoggingMiddleware at the route level as well
    # (in addition to global) just as a demonstration.
    # This is redundant because LoggingMiddleware is global,
    # but shows how you'd add route-level middleware if global wasn't present.
    return {"message": "Hello JSON with extra logging"}

@route("/json", methods=["GET"])
def json_route(request):
    # Global middlewares (CORS, Logging) apply
    return {"message": "Hello JSON"}

@route("/file", methods=["GET"])
def file_route(request):
    # Provide a test file path
    return Response.file("README.md", download_name="README.txt")

@route("/user/<int:id>", methods=["GET"])
def user_profile(request):
    user_id = request.param("id")
    return {"user_id": user_id, "name": "John Doe"}

@route("/secure-item", methods=["GET"], middlewares=[HTTPSMiddleware(enforce=True)])
def secure_item(request):
    # This route enforces HTTPS at the route level
    return {"status": "secure", "message": "This route requires HTTPS"}

@group(prefix="/api", middlewares=[])
class APIGroup:
    @route("/items", methods=["GET"])
    def list_items(self, request):
        return {"items": ["Item1", "Item2"]}

    @route("/items", methods=["POST"])
    def create_item(self, request):
        data = request.json()
        return {"status": "created", "item": data}

# Another group that enforces HTTPS for all its routes
@group(prefix="/admin", middlewares=[HTTPSMiddleware(enforce=True)])
class AdminGroup:
    @route("/dashboard", methods=["GET"])
    def dashboard(self, request):
        # This route will only be accessible via HTTPS
        return {"admin": "secure area"}

    @route("/settings", methods=["GET"])
    def settings(self, request):
        return {"settings": "admin config"}

if __name__ == "__main__":
    run_server("0.0.0.0", 8000)
