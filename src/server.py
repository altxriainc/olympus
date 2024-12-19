from wsgiref.simple_server import make_server, WSGIRequestHandler
from .routing.router import Router
from .routing.request import Request
from .routing.response import Response
from .exceptions_manager import ExceptionsManager
from .routing.exceptions import HttpNotFoundException, HttpMethodNotAllowedException
from .routing.middleware import HTTPSMiddleware
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("OlympusServer")

class CustomRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        request_line = format % args
        client_ip = self.client_address[0]
        timestamp = self.log_date_time_string()

        try:
            status_code = int(args[1].split(' ')[0])  # Extract the status code
            if 200 <= status_code < 300:
                status_color = '\033[92m'  # Green
                emoji = "🟢"
            elif 300 <= status_code < 400:
                status_color = '\033[93m'  # Yellow
                emoji = "🟡"
            elif 400 <= status_code < 500:
                status_color = '\033[91m'  # Red
                emoji = "🔴"
            else:
                status_color = '\033[95m'  # Magenta
                emoji = "🔥"
        except (IndexError, ValueError):
            status_color = '\033[90m'  # Grey for unknown cases
            emoji = "❓"

        logger.info(
            "%s%s Client: %s | Time: %s | Request: %s%s",
            status_color,
            emoji,
            client_ip,
            timestamp,
            request_line,
            '\033[0m'  # Reset color
        )

def application(environ, start_response):
    request = Request.from_environ(environ)
    router = Router.get_instance()

    # If global HTTPS is enforced
    if router.enforce_https_global:
        https_mw = HTTPSMiddleware(enforce=True)
        redirect_res = https_mw.handle_pre(request)
        if redirect_res:
            start_response(redirect_res.status_line, list(redirect_res.headers.items()))
            return [redirect_res.body]

    # Handle request in a try/except so that all exceptions go through ExceptionsManager
    try:
        response = router.handle_request(request)
    except Exception as e:
        if router.exceptions_manager:
            response = router.exceptions_manager.handle_exception(e, request)
        else:
            response = Response(status=500, body="Internal Server Error")

    start_response(response.status_line, list(response.headers.items()))
    return [response.body]

def run_server(host="127.0.0.1", port=8000):
    banner = f"""
    \033[94m======================================
       Olympus Server is Running 🚀
    --------------------------------------
       \033[92mURL: http://{host}:{port}\033[0m
    \033[94m======================================\033[0m
    """
    print(banner)
    logger.info("\033[92mServer started at http://%s:%s\033[0m", host, port)

    with make_server(host, port, application, handler_class=CustomRequestHandler) as httpd:
        httpd.serve_forever()
