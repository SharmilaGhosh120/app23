import streamlit as st
from openai import OpenAI, AuthenticationError
import os

st.set_page_config(page_title="AI Companion", page_icon="🤖")
st.title("World’s First AI Companion powered by Large Behavioral Model (LBM)")

st.subheader("Privacy Policy")
policy_text = """use your website or services, collect basic details like your name, email, phone number, and any other information you choose to provide. collect technical info like your IP address and browser type to help improve our platform.use this data to create your account, process payments, respond to queries, and keep you informed. Your information stays safe with us—we don't sell or share it with anyone except trusted services like payment processors.We use cookies to understand how people use our site and make improvements. You can always block cookies in your browser settings. If you want to update or delete your information, just email us and we'll take care of it."""
st.markdown(policy_text)

st.subheader("Create Account")
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

with st.form(key="user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    submit = st.form_submit_button("Create Account")
    if submit:
        st.session_state.user_info = {"name": name, "email": email, "phone": phone}
        st.success("Account created successfully! Now you can chat with the AI Companion.")

st.subheader("Chat with AI Companion")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are an AI Companion powered by the Large Behavioral Model (LBM), trained on complete human metadata for domain-agnostic interactions. Build intelligent responses using LLMs and agentic frameworks, personalize based on user behavior."}]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_info := st.session_state.get("user_info"):
    st.info(f"Welcome, {user_info['name']}! Your details are stored securely for personalization.")

if prompt := st.chat_input("Ask the AI Companion anything..."):
    api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    if not api_key:
        st.error("Please set your OpenAI API key in Streamlit secrets (.streamlit/secrets.toml) or environment variable.")
    else:
        try:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except AuthenticationError as e:
            st.error(f"Authentication failed: Invalid API key. Please check your key at https://platform.openai.com/account/api-keys. Error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")