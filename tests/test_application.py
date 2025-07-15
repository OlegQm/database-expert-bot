import pytest
from app_and_bot.application import Application
from app_and_bot.config import settings

@pytest.fixture(scope="module")
def api_key():
    """
    Fixture to get the API key from environment variables.

    Returns: The API key for accessing the GPT model.
    """
    return settings.openai_api_key
    
@pytest.fixture(scope="module")
def application(api_key):
    """
    Fixture to create an instance of the Application
    class using the provided API key.

    Parameters:
    api_key (str): The API key for accessing the GPT model.

    Returns: An instance of the Application class.
    """
    return Application(api_key)

def test_initial_state(application):
    """
    Test to verify that the initial state of the application has an empty conversation history.

    Parameters:
    application (Application): An instance of the Application class.

    Asserts:
    The initial length of the formatted conversation history is 0.
    """
    assert len(application.bot_instance.get_formatted_history()) == 0
    
def test_history_cleaned(application):
    """
    Test to verify that the conversation history is correctly filled and
    cleaned after being filled.

    Parameters:
    application (Application): An instance of the Application class.

    Asserts:
    - The length of the formatted conversation history is 2 after sending a message to the bot.
    - The length of the formatted conversation history is 0 after clearing the conversation.
    """
    application.bot_instance.ask_bot("Hello!")
    assert len(application.bot_instance.get_formatted_history()) == 2
    application.clear_conversation()
    assert len(application.bot_instance.get_formatted_history()) == 0
