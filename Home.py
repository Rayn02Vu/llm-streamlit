import streamlit as st
from streamlit import session_state as State
from langchain_openai.chat_models import ChatOpenAI

api_key = st.secrets["CONO_API_KEY"]
api_base = st.secrets["CONO_API_BASE"]

llm = ChatOpenAI(
    model_name="cono-3-exp",
    temperature=0, 
    api_key=api_key, 
    base_url=api_base
)

async def main():
    
    st.title("ArcanyBot")
    st.sidebar.success("Welcome to ArcanyBot")
    
    if "messages" not in State:
        State.messages = []
    
    prompt = st.chat_input("Prompt here...")
    
    if len(State.messages) > 5:
        State.messages = [State.messages[0]] + State.messages[-5:]
        
    for msg in State.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        State.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for response in llm.stream(State.messages):
                
                full_response += response.content
                message_placeholder.markdown(full_response + "▌")
                
            message_placeholder.markdown(full_response)
            
        State.messages.append({"role": "assistant", "content": response})
    else:
        st.markdown("### 📝 Type a prompt to get started!")  


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())