import os
from dotenv import load_dotenv
import pickledb
from .folder import BASE_PATH


class ConfigManager:
    def __init__(self, db_name="config.db"):
        """
        Initializes the ConfigManager with a database file.
        """
        self.db_path = os.path.join(BASE_PATH, db_name)
        self.db = pickledb.load(self.db_path, auto_dump=False)

    def initialize_keys(self, keys):
        """
        Load environment variables for the specified keys and store them in the database.

        Args:
            keys (list): A list of environment variable keys to initialize.
        """
        load_dotenv()
        for key in keys:
            value = os.getenv(key)
            if value:
                self.set(key, value)

    def get(self, key, default=None):
        """
        Retrieves the value associated with the given key from the database.

        Args:
            key (str): The key to retrieve the value for.
            default: The default value to return if the key is not found.

        Returns:
            The value from the database or the default value.
        """
        return self.db.get(key) if self.db.get(key) is not False else default

    def set(self, key, value):
        """
        Sets a key-value pair in the database and saves it.

        Args:
            key (str): The key to set.
            value: The value to associate with the key.
        """
        self.db.set(key, value)
        self.db.dump()


# Utility function to create and initialize a ConfigManager

def create_initialized_config(db_name, keys):
    """
    Creates a ConfigManager instance and initializes it with specified keys.

    Args:
        db_name (str): Name of the database file.
        keys (list): A list of environment variable keys to initialize.

    Returns:
        ConfigManager: The initialized ConfigManager instance.
    """
    config = ConfigManager(db_name)
    config.initialize_keys(keys)
    return config

# Initialize Configurations
ENV_KEYS = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_OPENAI_API_KEY",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_REGION",
    "DEEPSEEK_API_KEY",
]

Configuration = create_initialized_config("config.db", ENV_KEYS)
ClientConfiguration = create_initialized_config("client_config.db", [])
