import pytest
import os
from app_and_bot.bot import GPTBot
from dotenv import load_dotenv

@pytest.fixture(scope="module")
def api_key() -> str:
    """
    Fixture to get the API key from environment variables.

    Returns: The API key for accessing the GPT model.
    """
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

@pytest.fixture(scope="module")
def bot(api_key: str) -> GPTBot:
    """
    Fixture to create an instance of GPTBot using the provided API key.

    Parameters:
    api_key (str): The API key for accessing the GPT model.

    Returns: An instance of GPTBot configured with the given API key.
    """
    bot = GPTBot(api_key)
    return bot

def test_bot_answer_length(bot: GPTBot) -> None:
    """
    Test to verify that the bot provides a non-empty response.

    Parameters:
    bot (GPTBot): An instance of GPTBot.

    Asserts:
    The length of the bot's response content is greater than 0.
    """
    reply = bot.ask_bot("What is your name?")
    assert len(reply.content) > 0

def test_bot_memory_length(bot: GPTBot) -> None:
    """
    Test to verify that the bot correctly remembers the conversation history
    and that the history contains the expected number of messages.

    Parameters:
    bot (GPTBot): An instance of GPTBot.

    Asserts:
    The length of the formatted conversation history is equal to 4.
    """
    bot.ask_bot("What did I ask you last time?")
    history_messages_length = len(bot.get_formatted_history())
    assert history_messages_length == 4