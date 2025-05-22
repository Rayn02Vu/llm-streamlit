import json
import streamlit as st
from streamlit import session_state as state
import streamlit_shadcn_ui as ui
import requests


api_base = st.secrets["FLOW_API_BASE"]
api_key = st.secrets["FLOWISE_API_KEY"]


def query(payload):
    response = requests.post(api_base, headers={
        "Authorization": "Bearer " + api_key
    }, json=payload)
    return response.json()



async def main():
    
    if "messages" not in state:
        state.messages = []
    if "running" not in state:
        state.running = False
    if "prompt" not in state:
        state.prompt = ""
    
    st.title("AcanyBot 🤖")
    ui.badges(
        badge_list=[
            ("QA Chat", "secondary"), ("RAG", "destructive")
        ],
        class_name="flex gap-4"
    )
    
    st.sidebar.success("### History Data")
    st.sidebar.markdown("#### 📕 Lich_su_Dang.txt")
    
    state.messages.append({"role": "assistant", "content": "Chào bạn! Tôi có thể giúp gì?"})
    
    for item in state.messages:
        with st.chat_message(item["role"]):
            st.write(item["content"])
    
    
    if not state.running:
        if new_prompt := st.chat_input("Send a message...", disabled=state.running):
            state.prompt = new_prompt
            state.messages.append({"role": "user", "content": new_prompt})
            state.running = True
            with st.chat_message("user"):
                st.write(new_prompt)
            st.rerun()

    if state.running:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query({"question": state.prompt})
                with open("res.json", "w") as f:
                    f.write(json.dumps(response, indent=4))
                
                state.running = False
                state.messages.append({"role": "assistant", "content": response["text"]})
                state.prompt = ""
                st.rerun()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
