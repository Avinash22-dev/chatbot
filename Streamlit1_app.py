import streamlit as st
import requests  # For making API requests to Llama

# Show title and description.
st.title(" Chatbot (Powered by Llama)")
st.write(
    "This is a simple chatbot that uses Meta's open-source Llama model to generate responses. "
    "To use this app, you'll need a Llama API key (available through providers like Replicate)."
)

# Ask user for their Llama API endpoint and key.
llama_endpoint = st.text_input("Llama API Endpoint (URL)")
llama_api_key = st.text_input("Llama API Key", type="password")

# Show informative messages based on input status.
if not llama_endpoint:
    st.info("Please enter the Llama API endpoint URL.")
elif not llama_api_key:
    st.info("Please enter your Llama API key.")
else:

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Function to format and display messages
    def display_message(message, role):
        with st.chat_message(role):
            st.markdown(message)

    # Display the existing chat messages.
    for message in st.session_state.messages:
        display_message(message["content"], message["role"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.text_input("What can I help you with today?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message(prompt, "user")

        # Prepare the request body containing the prompt and past messages.
        request_body = {
            "messages": [{"role": message["role"], "content": message["content"]} for message in st.session_state.messages]
        }

        # Set headers with the API key for authentication.
        headers = {"Authorization": f"Bearer {llama_api_key}"}

        # Send the request to the Llama API endpoint (replace with your provider's endpoint).
        response = requests.post(f"{llama_endpoint}/completions", json=request_body, headers=headers)

        # Check for successful response.
        if response.status_code == 200:
            generated_response = response.json()["choices"][0]["text"]
            st.session_state.messages.append({"role": "assistant", "content": generated_response})
            display_message(generated_response, "assistant")
        else:
            st.error("An error occurred while communicating with the Llama API.")
