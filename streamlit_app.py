import streamlit as st
from openai import OpenAI
from ui.layout import render_header, render_chat_area
from ui.chat_bubble import add_user_message, add_assistant_message
from ui.theme import apply_theme

def main():
    st.set_page_config(page_title="AI 챗봇", layout="wide")
    apply_theme()

    render_header()

    openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
    if not openai_api_key:
        st.warning("API Key가 필요합니다.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    render_chat_area()

    user_input = st.chat_input("메시지를 입력하세요")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        add_user_message(user_input)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=False
        )
        # 응답 포맷에 따라 다를 수 있으니 안전하게 추출
        try:
            reply = response.choices[0].message.content
        except Exception:
            # fallback: 응답이 다른 형식일 경우
            reply = getattr(response.choices[0], "text", "응답을 불러오지 못했습니다.")
        st.session_state.messages.append({"role": "assistant", "content": reply})
        add_assistant_message(reply)

if __name__ == "__main__":
    main()

import streamlit as st

def render_header():
    st.markdown("""
        <h1 style='text-align: center; color: #4B8BF4;'>💬 나의 10월 AI 챗봇</h1>
        <p style='text-align: center; color: gray;'>Streamlit + OpenAI 기반 고급형 챗봇</p>
        <hr>
    """, unsafe_allow_html=True)

def render_chat_area():
    # 채팅 컨테이너를 렌더링
    st.markdown("<div style='height: 400px; overflow-y: auto;'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])
    st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st

def add_user_message(content: str):
    with st.chat_message("user"):
        st.markdown(f"👤 **User:** {content}")

def add_assistant_message(content: str):
    with st.chat_message("assistant"):
        st.markdown(f"🤖 **AI:** {content}")

import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        body {
            background-color: #F7F9FC;
        }
        .stApp {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

