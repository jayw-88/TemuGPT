import streamlit as st
import google.generativeai as genai
import time

# API
genai.configure(api_key="AIzaSyC7LgIAL1HSccNkkFNTQi0VgjFH2VWQjF8")

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

# Console output area
console_container = st.container()
with console_container:
    if not st.session_state.console_output:
        st.text("DISCLAIMER: Please do not abuse this AI in any way. It is supposed to be used as an assistant—don't let it do everything for you.)
        time.sleep(5)
        st.text("Welcome to TemuGPT! \nPress 'N' to start a new chat, 'X' to delete a chat, 'S' for settings, and 'Q' to quit. \n\nHow may TemuGPT help you today?")
    else:
        for line in st.session_state.console_output:
            st.text(line)

# Input area
if len(st.session_state.chats) != 0:
    prompt_text = "What would you like to do? \n(Ask Something, New Chat (N), Delete Chat (X), Settings (S), Quit (Q))"
else:
    prompt_text = "Type here:"
with st.form(key="input_form", clear_on_submit=True):  
    user_input = st.text_input(prompt_text, key="user_input")    
    submit_button = st.form_submit_button("Submit", type="primary")

if submit_button and user_input:
    if user_input:
        st.session_state.console_output.append(f"\n> {user_input}")
        
        # New Chat
        if user_input == "N" or user_input == "n":
            time.sleep(.5)
            st.session_state.console_output.append("\nWhat would you like to name this chat?")
            
        # Delete Chat
        elif user_input == "X" or user_input == "x":
            time.sleep(.5)
            if len(st.session_state.chats) != 0:
                st.session_state.console_output.append("\nWhich chat would you like to delete?\n")
                for i in range(len(st.session_state.chats)):
                    st.session_state.console_output.append(str(i) + ". " + st.session_state.chats[i])
                time.sleep(.5)
                st.session_state.console_output.append("\nInput the number of the chat.")
            else:
                time.sleep(.5)
                st.session_state.console_output.append("\nYou have no chats to delete!")
        
        # Settings
        elif user_input == "S" or user_input == "s":
            time.sleep(.5)
            st.session_state.console_output.append("\nWelcome to Settings!")
            st.session_state.console_output.append("Here you can give TemuGPT certain instructions for his responses. (e.g. Be more concise, be more thorough)")
            st.session_state.console_output.append("Input your settings or press 'X' to exit.")
        
        # Regular query
        else:
            if len(st.session_state.chats) == 0:
                st.session_state.console_output.append(f"\nNew chat automatically created! — {user_input}")
                st.session_state.chats.append(user_input)
            
            try:
                model = genai.GenerativeModel(
                    model_name='gemini-2.5-flash-lite',
                    system_instruction=st.session_state.system_instruction_change
                )
                st.session_state.console_output.append("\nLoading... (Might take some time)")
                time.sleep(.5)
                response = model.generate_content(user_input)
                st.session_state.console_output.append(f"\nAnswer: \n{response.text}\n")
            except Exception as e:
                st.session_state.console_output.append(f"\nError: {str(e)}\n")
        
    st.rerun()

