import sys
import os

# Ensure that we can import from src by adding project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.server import run_server
from src.routing.decorators import route, group
from src.routing.response import Response
from src.routing.router import Router
from src.routing.cors import CORSMiddleware
from src.routing.middleware import HTTPSMiddleware, Middleware
from src.exceptions_manager import ExceptionsManager
from src.routing.exceptions import HttpNotFoundException

# Initialize the main router and exceptions manager
router = Router.get_instance()
exceptions_manager = ExceptionsManager()
router.set_exceptions_manager(exceptions_manager)

# Custom 404 handler
def handle_not_found(exc, request):
    return Response(status=404, body="This page was not found!")
exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

# Logging Middleware for demonstration
class LoggingMiddleware(Middleware):
    def handle_pre(self, request):
        print(f"[LoggingMiddleware] Request for path: {request.path}")
        return None

# Global middleware setup
router.use_global_middleware(CORSMiddleware())  # CORS enabled for all routes
# Note: LoggingMiddleware could also be added globally if desired:
# router.use_global_middleware(LoggingMiddleware())

# Disable global HTTPS enforcement (we'll enforce HTTPS on some routes/groups)
router.force_https(False)

# ---------------------------------------
# Example Routes
# ---------------------------------------

@route("/json", methods=["GET"])
def json_route(request):
    # Simple JSON response route
    return {"message": "Hello JSON"}

@route("/json-logged", methods=["GET"], middlewares=[LoggingMiddleware()])
def json_logged_route(request):
    # Demonstrates route-level middleware logging in addition to global CORS
    return {"message": "Hello JSON with extra logging"}

@route("/file", methods=["GET"])
def file_route(request):
    # Returns the contents of README.md as a downloadable file named "README.txt"
    return Response.file("README.md", download_name="README.txt")

@route("/user/<int:id>", methods=["GET"])
def user_profile(request):
    user_id = request.param("id")
    return {"user_id": user_id, "name": "John Doe"}

@route("/secure-item", methods=["GET"], middlewares=[HTTPSMiddleware(enforce=True)])
def secure_item(request):
    # This route requires HTTPS; if accessed via HTTP, it will redirect
    return {"status": "secure", "message": "This route requires HTTPS"}

# ---------------------------------------
# Grouped Routes (with prefixes and middlewares)
# ---------------------------------------

@group(prefix="/api", middlewares=[])
class APIGroup:
    @route("/items", methods=["GET"])
    def list_items(self, request):
        return {"items": ["Item1", "Item2"]}

    @route("/items", methods=["POST"])
    def create_item(self, request):
        data = request.json()
        return {"status": "created", "item": data}

@group(prefix="/admin", middlewares=[HTTPSMiddleware(enforce=True)])
class AdminGroup:
    @route("/dashboard", methods=["GET"])
    def dashboard(self, request):
        # All routes in this group require HTTPS
        return {"admin": "secure area"}

    @route("/settings", methods=["GET"])
    def settings(self, request):
        return {"settings": "admin config"}

# ---------------------------------------
# Run the development server
# ---------------------------------------
if __name__ == "__main__":
    run_server("0.0.0.0", 8000)
