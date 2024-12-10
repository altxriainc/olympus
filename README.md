
# Olympus

![Latest Version](https://img.shields.io/pypi/v/olympus-framework)
![Downloads](https://img.shields.io/pypi/dm/olympus-framework)
![Status](https://img.shields.io/badge/status-alpha-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)

**Olympus** is a Python web framework foundation inspired by the rich routing, middleware, and exception handling systems found in Laravel. It provides a clean, extensible base that you can build upon for full-stack applications, whether you're serving HTML, JSON-based APIs, or file downloads. With Olympus, you can define routes using decorators, group them, apply middlewares globally or at the route level, and handle exceptions elegantly.

[Click here for the documentation](https://github.com/altxriainc/olympus/wiki)

---

## 🚀 Key Features

- **Expressive Routing System**: Define routes via decorators, including route groups, URL parameters, and multiple HTTP methods.
- **Advanced Middleware Support**: Apply middleware globally, per route, or per group. Handle pre- and post-request logic easily.
- **Exception Handling & Custom 404**: Gracefully handle errors and register custom exception handlers, including global 404 responses.
- **HTTPS Enforcement**: Force HTTPS globally or on specific routes/groups with a single middleware.
- **CORS Integration**: Easily add CORS headers to your responses, handle preflight requests.
- **JSON, File, and HTML Responses**: Return JSON APIs, serve files for download, or integrate a templating engine for HTML rendering.
- **Group Prefixes & Middleware Inheritance**: Organize routes into groups that share a prefix, middleware stack, or both.
- **Extensible & Composable**: Olympus is designed as a foundational layer. Plug in your own ORM, templating engine, or validation library.

---

## 🛠️ Getting Started

### Step 1: Install Olympus

Install Olympus via pip:

```bash
pip install olympus-framework
```

*(Ensure you have Python 3.8+ available.)*

### Step 2: Define Your First Route

Create a `main.py`:

```python
from src.server import run_server
from src.routing.decorators import route
from src.routing.response import Response
from src.routing.router import Router
from src.exceptions_manager import ExceptionsManager
from src.routing.exceptions import HttpNotFoundException

router = Router.get_instance()
exceptions_manager = ExceptionsManager()
router.set_exceptions_manager(exceptions_manager)

def handle_not_found(exc, request):
    return Response(status=404, body="Page not found!")
exceptions_manager.register_handler(HttpNotFoundException, handle_not_found)

@route("/hello", methods=["GET"])
def hello_route(request):
    return {"message": "Hello from Olympus!"}

if __name__ == "__main__":
    run_server("0.0.0.0", 8000)
```

Now, open [http://localhost:8000/hello](http://localhost:8000/hello) in your browser.

### Step 3: Use Middlewares

Add global or route-level middleware:

```python
from altxria.olympus.routing.middleware import Middleware

class LoggingMiddleware(Middleware):
    def handle_pre(self, request):
        print(f"Received request at {request.path}")
        return None

router.use_global_middleware(LoggingMiddleware())
```

All incoming requests are now logged before being handled.

### Step 4: Group Routes & Enforce HTTPS

```python
from altxria.olympus.routing.decorators import group
from altxria.olympus.routing.middleware import HTTPSMiddleware

@group(prefix="/admin", middlewares=[HTTPSMiddleware(enforce=True)])
class AdminGroup:
    @route("/dashboard", methods=["GET"])
    def dashboard(self, request):
        return {"admin": "This area is protected by HTTPS"}

    @route("/settings", methods=["GET"])
    def settings(self, request):
        return {"settings": "admin config"}
```

---

## 🔍 Project Status

![Issues Closed](https://img.shields.io/github/issues-closed/altxriainc/olympus)
![Bug Issues](https://img.shields.io/github/issues/altxriainc/olympus/bug)
![Enhancement Issues](https://img.shields.io/github/issues/altxriainc/olympus/enhancement)

Olympus is currently in **alpha**. Expect frequent changes and improvements as the framework matures.

---

## 📜 License and Usage

Olympus is licensed under the MIT License, making it free for personal and commercial use. See the [LICENSE](https://github.com/altxriainc/olympus/blob/main/LICENSE) file for more details.

---

## 🤝 Contributors

Developed and maintained by **Altxria Inc.** and the open-source community.

![Contributors](https://contrib.rocks/image?repo=altxriainc/olympus)

[See All Contributors](https://github.com/altxriainc/olympus/graphs/contributors)

---

## ❤️ Support Olympus

If you find Olympus useful, consider sponsoring us to support ongoing development and new features!

[![Sponsor Olympus](https://img.shields.io/badge/Sponsor-Olympus-blue?logo=github-sponsors)](https://github.com/sponsors/altxriainc)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/N4N516SMZ6)

---

**Ready to build your next web application with Olympus?** Jump right in by exploring the [documentation](https://github.com/altxriainc/olympus/wiki) or browsing the code.
