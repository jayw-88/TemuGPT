import streamlit as st
import google.generativeai as genai

# API
genai.configure(api_key="AIzaSyDAm1jtwFCjZhkiDtG4SmwQXwikfdDQLpE")

# page config
st.set_page_config(page_title="TemuGPT")

if 'chats' not in st.session_state:
    st.session_state.chats = []
if 'system_instruction_change' not in st.session_state:
    st.session_state.system_instruction_change = "You are a generalized helpful assistant that helps with users' tasks."
if 'console_output' not in st.session_state:
    st.session_state.console_output = []

# Title
st.title("TemuGPT")
st.markdown("---")

# Console output area
st.subheader("")
console_container = st.container()
with console_container:
    if not st.session_state.console_output:
        st.text("Welcome to TemuGPT! Press 'N' to start a new chat, 'X' to delete a chat, 'S' for settings, and 'Q' to quit. How may TemuGPT help you today?")
    else:
        for line in st.session_state.console_output:
            st.text(line)

st.markdown("---")

# Input area
if len(st.session_state.chats) != 0:
    prompt_text = "What would you like to do? (Ask, New Chat (N), Delete Chat (X), Settings (S), Quit (Q))"
else:
    prompt_text = "Type here:"

user_input = st.text_input(prompt_text, key="user_input")

if st.button("Enter", type="primary"):
    if user_input:
        st.session_state.console_output.append(f"\n> {user_input}")
        
        # New Chat
        if user_input == "N" or user_input == "n":
            st.session_state.console_output.append("\nWhat would you like to name this chat?")
            # This will need another input cycle
            
        # Delete Chat
        elif user_input == "X" or user_input == "x":
            if len(st.session_state.chats) != 0:
                st.session_state.console_output.append("\nWhich chat would you like to delete?\n")
                for i in range(len(st.session_state.chats)):
                    st.session_state.console_output.append(str(i) + ". " + st.session_state.chats[i])
                st.session_state.console_output.append("\nInput the number of the chat.")
            else:
                st.session_state.console_output.append("\nYou have no chats to delete!")
        
        # Settings
        elif user_input == "S" or user_input == "s":
            st.session_state.console_output.append("\nWelcome to Settings!")
            st.session_state.console_output.append("Here you can give TemuGPT certain instructions for his responses. (e.g. Be more concise, be more thorough)")
            st.session_state.console_output.append("Input your settings or press 'X' to exit.")
        
        # Regular query
        else:
            if len(st.session_state.chats) == 0:
                st.session_state.console_output.append(f"\nNew chat automatically created! — {user_input}")
                st.session_state.chats.append(user_input)
            
            st.session_state.console_output.append("\nLoading... (Might take some time)")
            
            try:
                model = genai.GenerativeModel(
                    model_name='gemini-2.5-flash-lite',
                    system_instruction=st.session_state.system_instruction_change
                )
                response = model.generate_content(user_input)
                st.session_state.console_output.append(f"\nAnswer: \n{response.text}\n")
            except Exception as e:
                st.session_state.console_output.append(f"\nError: {str(e)}\n")
        
        st.rerun()

