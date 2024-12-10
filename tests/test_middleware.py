import unittest
from src.routing.router import Router
from src.routing.middleware import Middleware
from src.routing.response import Response
from src.routing.request import Request

class TestMiddleware(unittest.TestCase):
    def setUp(self):
        Router._instance = None
        self.router = Router.get_instance()

    def test_global_middleware(self):
        class TestPreMiddleware(Middleware):
            def handle_pre(self, request):
                if request.path == "/blocked":
                    return Response(status=403, body="Forbidden")
                return None

        self.router.use_global_middleware(TestPreMiddleware())
        
        def handler(req):
            return Response(body="OK")

        self.router.add_route(["GET"], "/allowed", handler)

        req_blocked = Request("GET", "/blocked", {}, {}, b"", "http", {})
        res_blocked = self.router.handle_request(req_blocked)
        self.assertEqual(res_blocked.status, 403)

        req_allowed = Request("GET", "/allowed", {}, {}, b"", "http", {})
        res_allowed = self.router.handle_request(req_allowed)
        self.assertEqual(res_allowed.status, 200)
        self.assertEqual(res_allowed.body, b"OK")
