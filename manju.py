
import streamlit as st
from google import genai
import google.generativeai as genai
from google.genai import types
from PIL import Image
import os



st.title('ABC chatbot')
#input_chat = st.selectbox('Ask your question here)
# file uploader for adding image file
input_image = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
# Text area for user input
input_text = st.text_area('Please paste the text here', height = 100).lower()

# google gemini api using streamlit secrets
genai.configure(api_key=st.secrets.get("gemini_api_key"))

chat = genai.chats.create(model="gemini-2.0-flash")


# Process inputs on button click (chatgpt)
if st.button("Analyze"):
  try:
    response_text = ""

    if input_image and input_text:
      try:
        image =  Image.open(input_image)

        # response from chatbot
        response = client.models.generate_content_stream(
        model="gemini-2.5-flash", contents=[image, input_text],
        config=types.GenerateContentConfig(
            temperature=0.1
          ),
        )

        # Handle streaming or non-streaming response
        if hasattr(response, '__iter__') and not hasattr(response, 'text'):
          response_text = "".join([part.text for part in response if hasattr(part, 'text')])
        else:
          response_text = response.text if hasattr(response, 'text') else ""
          st.markdown(response_text, unsafe_allow_html=True)
        # Saving to chat history
        chat.send_message(response_text)
      except Exception as e:
        st.error(f"Error processing image: {e}")

    else:
      if input_text != 'stop':
        response = chat.send_message_stream(input_text)
        response_text = "".join([part.text for part in response if hasattr(part, 'text')])
        st.markdown(response_text, unsafe_allow_html=True)
      else:
        print('Thank you for your conversation. Have a nice day!')

  except Exception as e:
      st.write(f"Error: {e}")


for message in chat.get_history():
      st.write(f'role - {message.role}',end=": ")
      st.write(message.parts[0].text)
