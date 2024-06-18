import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *


float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "CHÀO! Tôi có thể hỗ trợ gì cho bạn hôm nay?"}
        ]

initialize_session_state()

st.title("OpenAI Chatbot ")


chat_input_container = st.container()
with chat_input_container:
    user_input = st.text_input("Nhập câu hỏi của bạn...")
    send_button = st.button("Gửi")  


footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()



if send_button: 
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
elif audio_bytes:
    with st.spinner("Phiên âm..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            os.remove(webm_file_path)
else:
   
    pass  


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant" and (user_input or audio_bytes):
    with st.chat_message("assistant"):
        with st.spinner("Suy nghĩ..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Tạo phản hồi âm thanh..."):
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)


footer_container.float("bottom: 0rem;")
