import streamlit as st
from app_and_bot.bot import GPTBot
from app_and_bot.config import settings

def create_bot(api_key: str, model_name: str):
    """
    Creates an instance of GPTBot using the provided API key and model name.
    Then this instance is cached.
    """
    return GPTBot(api_key, model_name)

class Application():
    def __init__(
            self,
            api_key: str
        ) -> None:
        """
        Initializes the Application class, which sets up the interface,
        creates a GPTBot instance, and updates the conversation.
        
        Parameters:
        api_key (str): The API key for accessing the GPT model.
        
        Returns:
        GPTBot: An instance of GPTBot configured with the given API key and model name.
        """
        model_name = self.__initialize_interface()
        
        # Check if a bot instance exists in the session state and if the model has been changed.
        if "bot" not in st.session_state or st.session_state.bot.get_model_name() != model_name:
            st.session_state.bot = create_bot(api_key, model_name)
        
        self.__bot = st.session_state.bot
        self.__update_conversation()
            
    def __initialize_interface(self) -> str:
        """
        Sets up the Streamlit interface.

        Returns:
        str: The name of the selected GPT model.
        """
        options = ["gpt-4.1", "gpt-4o-mini"]
        selected_model = st.selectbox("Choose a model", options)
        col1, col2 = st.columns([3, 1], vertical_alignment="center")
        with col1:
            st.title("**Your personal** AI **assistant**")
        with col2:
            st.button("Clear chat", on_click=self.clear_conversation)
        st.markdown("---")
        return selected_model
            
    def clear_conversation(self) -> None:
        """
        Clears the conversation history stored in the GPTBot instance.
        """
        self.__bot.clear_history()
        
    @property
    def bot_instance(self) -> GPTBot:
        """
        Property to access the GPTBot instance.
        
        Returns:
        GPTBot: The current instance of GPTBot.
        """
        return self.__bot
        
    def __update_conversation(self) -> None:
        """
        Handles user input from the chat input field and sends it to the GPTBot,
        then updates the chat interface with the conversation history.
        """
        user_message = st.chat_input("Type your message here...")
        if user_message:
            self.__bot.ask_bot(user_message)
        st.markdown("  \n".join(self.__bot.get_formatted_history()))
                   
def main():
    """
    The main function of the application. Retrieves the API key from the environment variables
    and initializes the Application class to start the Streamlit interface.
    """
    app = Application(settings.openai_api_key)

if __name__ == "__main__":
     main()
