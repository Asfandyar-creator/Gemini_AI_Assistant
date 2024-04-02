import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError


load_dotenv()


genai.configure(
    api_key=os.environ['GOOGLE_API_KEY']
)


class InternetConnectionError(Exception):
   pass
   
   def send_request(prompt):
        """
        Sends a request to the generative model, handling potential internet connection errors.

        Args:
            prompt: The user input to be processed by the model.

        Returns:
            The model's response as a string, or a user-friendly error message if unsuccessful.
        """

        try:
            model = genai.GenerativeModel(model_name='gemini-pro')
            chat = model.start_chat()
            response = chat.send_message(prompt)
            return response
        except RequestsConnectionError:
            raise InternetConnectionError("Internet connection is not available.")
        except requests.exceptions.Timeout:
            raise InternetConnectionError("Request timed out. Please check your internet connection.")
        except requests.exceptions.RequestException:
            raise InternetConnectionError("An error occurred while making the request. Please try again later.")

      
    


with st.sidebar:
    st.title('💬 LLM Chat App')
    st.markdown('''
    ## About
    
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [Gemini API](https://ai.google.dev/tutorials/get_started_web)
    - [Google Generative AI](https://pypi.org/project/google-generativeai/)
                 
 
    ''')
    st.write('Made with ❤️ by [Asfandyar](https://www.linkedin.com/in/asfand-yar-scientist/).')

def main():
    st.title("Chat with Gemini AI 🤖")

    # Initialize session state to store chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    text_area_content = ''
    input_prompt = st.text_area("hey! 👋🏼 ,How can I assist you today?", text_area_content, height=10, placeholder='Enter your prompt here...')


    col1, col2 = st.columns([1,1])
    
    # Your existing code here...

    with col1:
        if st.button("Search") and input_prompt.strip() != "":
            try:
                response = InternetConnectionError.send_request(input_prompt)
                st.session_state.chat_history.append({"user": input_prompt, "model": response.text})
            except:
                return st.error('Failed to connect to the internet. Please check your connection.')

    with col2:
    # Add a clear chat button 
        if st.button("Clear Chat"):
            st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.expander(f"Chat - {st.session_state.chat_history.index(chat) + 1}"):
            st.markdown(
                f"<div style='text-align: left; white-space: pre-wrap;'><b><i><u>You:</u></i></b>\n {chat['user']}</div>", 
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='text-align: left; white-space: pre-wrap;'><b><i><u>Model:</u></i></b>\n {chat['model']}</div>", 
                unsafe_allow_html=True
            )




# Footer text
footer_text = "Bot can make mistakes. Consider checking important information :)."

# Display footer using markdown
st.markdown(
f"""
<style>
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: black;
        padding: 10px 0;
        text-align: center;
        color: gray;
        opacity: 1;
    }}
</style>
<div class="footer">{footer_text}</div>
""",
unsafe_allow_html=True,
)

if __name__ == "__main__":
    main()

