import unittest
from src.routing.router import Router
from src.routing.request import Request
from src.routing.response import Response

class TestRouting(unittest.TestCase):
    def setUp(self):
        # Reset router instance
        Router._instance = None
        self.router = Router.get_instance()

    def test_simple_route(self):
        def sample_handler(req):
            return Response(body="Hello World")
        self.router.add_route(["GET"], "/hello", sample_handler)
        req = Request("GET", "/hello", {}, {}, b"", "http", {})
        res = self.router.handle_request(req)
        self.assertEqual(res.body, b"Hello World")
        self.assertEqual(res.status, 200)

    def test_not_found(self):
        req = Request("GET", "/not-exist", {}, {}, b"", "http", {})
        res = self.router.handle_request(req)
        self.assertEqual(res.status, 404)
        self.assertIn("Not Found", res.body.decode('utf-8'))
