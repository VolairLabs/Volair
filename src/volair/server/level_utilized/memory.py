"""
Module for handling temporary memory storage of agent messages.
"""

import pickle
import base64
from ...storage.configuration import Configuration

def save_temporary_memory(messages: list, agent_id: str) -> None:
    """
    Save messages for a specific agent ID in temporary memory.

    Args:
        messages: List of messages to store.
        agent_id: Unique identifier for the agent.
    """
    # Serialize and encode messages for storage
    serialized_messages = base64.b64encode(pickle.dumps(messages)).decode("utf-8")
    Configuration.set(f"temp_memory_{agent_id}", serialized_messages)


def get_temporary_memory(agent_id: str) -> list:
    """
    Retrieve messages for a specific agent ID from temporary memory.

    Args:
        agent_id: Unique identifier for the agent.

    Returns:
        List of messages if found, or None if not found.
    """
    serialized_messages = Configuration.get(f"temp_memory_{agent_id}")
    if not serialized_messages:
        return None

    # Decode and deserialize messages
    return pickle.loads(base64.b64decode(serialized_messages))
