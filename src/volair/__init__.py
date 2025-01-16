import warnings

warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


from .client.base import VolairClient
from .client.tasks.task_response import ObjectResponse, StrResponse, IntResponse, FloatResponse, BoolResponse, StrInListResponse
from .client.tasks.tasks import Task
from .client.agent_configuration.agent_configuration import AgentConfiguration
from .client.knowledge_base.knowledge_base import KnowledgeBase



from pydantic import Field


def hello() -> str:
    return "Hello from volair!"


__all__ = ["hello", "VolairClient", "ObjectResponse", "StrResponse", "IntResponse", "FloatResponse", "BoolResponse", "Task", "StrInListResponse", "AgentConfiguration", "Field", "KnowledgeBase"]