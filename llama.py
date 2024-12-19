import streamlit as st
from langchain_community.llms import Ollama

# App title
st.set_page_config(page_title="🦙💬 Llama 3.1 Chatbot")

# App sidebar
with st.sidebar:
    st.title('🦙💬 Llama 3.3 Chatbot')
    st.write('This chatbot is created using the open-source Llama 3.3 LLM model.')
    
    st.subheader('Models and parameters')
    temperature = st.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('max_length', min_value=32, max_value=128, value=120, step=8)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA3.1 response
def generate_llama3_response(prompt_input):
    llm = Ollama(model='llama3.3')
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    response = llm.invoke(f"{string_dialogue} {prompt_input} Assistant: ")
    return response

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama3_response(prompt)
            placeholder = st.empty()
            placeholder.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
