import streamlit as st
import time
  
async def main():
    st.title("ArcanyBot")
    
    st.sidebar.success("Welcome to ArcanyBot")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    prompt = st.chat_input("Prompt here...")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            async for response in stream_response(prompt):
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.markdown("### 📝 Type a prompt to get started!")  


async def stream_response(prompt):
    chunks = [
        "Hello world! ",
        "I am AcanyBot. ",
        "I am ",
        "in offline mode.",
        " Echo: ",
        prompt,
    ]
    for chunk in chunks:
        time.sleep(0.25)
        yield chunk


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())