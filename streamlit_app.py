import streamlit as st
import openai
import time

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set OpenAI API key
    openai.api_key = openai_api_key

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for user prompt
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Define a function to retry on 429 errors
        def openai_call_with_retries(messages, retries=5):
            for attempt in range(retries):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        stream=False,  # Disable streaming to avoid excessive API calls
                    )
                    return response
                except openai.error.RateLimitError:
                    if attempt < retries - 1:
                        st.warning(f"Rate limit exceeded. Retrying in {2 ** attempt} seconds...")
                        time.sleep(2 ** attempt)
                    else:
                        st.error("Rate limit exceeded. Please try again later.")
                        return None

        # Prepare the messages for the API call.
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # Make the API call with retry mechanism.
        response = openai_call_with_retries(messages)
        if response:
            assistant_message = response['choices'][0]['message']['content']

            # Display and store the assistant's response.
            with st.chat_message("assistant"):
                st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
