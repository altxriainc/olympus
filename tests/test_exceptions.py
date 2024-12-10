import unittest
from src.routing.router import Router
from src.exceptions_manager import ExceptionsManager
from src.routing.request import Request
from src.routing.response import Response

class CustomException(Exception):
    pass

class TestExceptions(unittest.TestCase):
    def setUp(self):
        Router._instance = None
        self.router = Router.get_instance()
        self.exceptions_manager = ExceptionsManager()
        self.router.set_exceptions_manager(self.exceptions_manager)

    def test_custom_exception_handler(self):
        def handler(req):
            raise CustomException("Something went wrong")

        def custom_handler(exc, request):
            return Response(status=500, body="Custom Error")

        self.exceptions_manager.register_handler(CustomException, custom_handler)
        self.router.add_route(["GET"], "/error", handler)

        req = Request("GET", "/error", {}, {}, b"", "http", {})
        res = self.router.handle_request(req)
        self.assertEqual(res.status, 500)
        self.assertEqual(res.body, b"Custom Error")
