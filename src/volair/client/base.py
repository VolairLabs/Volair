from pydantic import BaseModel
from typing import Dict, Any
import httpx
import atexit
from .level_one.call import Call
from .level_two.agent import Agent
from .storage.storage import Storage
from .tools.tools import Tools
from .markdown.markdown import Markdown
from .others.others import Others
from .printing import connected_to_server

class ServerStatusException(Exception):
    """Custom exception for server status check failures."""
    pass

class TimeoutException(Exception):
    """Custom exception for request timeout."""
    pass

class VolairClient(Call, Storage, Tools, Agent, Markdown, Others):
    def __init__(self, url: str, debug: bool = False):
        self.debug = debug
        self.url = self._initialize_url(url, debug)
        self.default_llm_model = "openai/gpt-4o"

        if not self.check_server_status():
            connected_to_server(self.server_type, "Failed")
            raise ServerStatusException("Failed to connect to the server at initialization.")

        connected_to_server(self.server_type, "Established")

    def _initialize_url(self, url: str, debug: bool) -> str:
        """Initializes the server URL and handles server setup for local development."""
        if "0.0.0.0" in url or "localhost" in url:
            self.server_type = "Local(Docker)"
        elif "valorlabs.com" in url:
            self.server_type = "Cloud(Volair)"
        elif "devserver" in url or "localserver" in url:
            self.server_type = "Local(LocalServer)"
            url = "http://localhost:7541"
            self._setup_dev_server(debug)
        else:
            self.server_type = "Cloud(Unknown)"

        return url

    def _setup_dev_server(self, debug: bool):
        """Sets up the development server and registers cleanup handlers."""
        from ..server import run_dev_server, stop_dev_server, is_tools_server_running, is_main_server_running

        run_dev_server(redirect_output=not debug)

        def exit_handler():
            if is_tools_server_running() or is_main_server_running():
                stop_dev_server()

        atexit.register(exit_handler)

    def set_default_llm_model(self, llm_model: str):
        """Sets the default LLM model for the client."""
        self.default_llm_model = llm_model

    def check_server_status(self) -> bool:
        """Checks if the server is reachable and operational."""
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.url}/status")
                return response.status_code == 200
        except httpx.RequestError:
            return False

    def send_request(self, endpoint: str, data: Dict[str, Any], files: Dict[str, Any] = None, method: str = "POST", return_raw: bool = False) -> Any:
        """
        Sends an HTTP request to the server.

        Args:
            endpoint: The API endpoint.
            data: Data to include in the request.
            files: Optional files to upload.
            method: HTTP method (GET or POST).
            return_raw: Whether to return raw response content.

        Returns:
            Response from the API, either as JSON or raw content.
        """
        with httpx.Client() as client:
            url = f"{self.url}{endpoint}"

            try:
                if method.upper() == "GET":
                    response = client.get(url, params=data, timeout=600.0)
                else:
                    response = client.post(url, data=data if files else None, files=files, json=None if files else data, timeout=600.0)

                if response.status_code == 408:
                    raise TimeoutException("Request timed out")

                response.raise_for_status()
                return response.content if return_raw else response.json()

            except httpx.RequestError as e:
                raise TimeoutException(f"HTTP request failed: {str(e)}")