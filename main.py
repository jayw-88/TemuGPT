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
if 'disclaimer_finish' not in st.session_state:
    st.session_state.disclaimer_finish = False

# Title
st.title("TemuGPT")

# DISCLAIMER SCREEN
st.text("DISCLAIMER: Please do not abuse this AI in any way. It is supposed to be an assistant—don't try to break school policy in any way.")
time.sleep(5)
# Console output
console_container = st.container()
with console_container:
    for line in st.session_state.console_output:
        st.text(line)

# Main input form - ONLY SHOWS HERE, AFTER DISCLAIMER
if len(st.session_state.chats) != 0:
    prompt_text = "What would you like to do? (Ask Something, New Chat (N), Delete Chat (X), Settings (S), Quit (Q))"
else:
    prompt_text = "Type here:"

# Main input form
with st.form(key="main_form", clear_on_submit=True):
    main_input = st.text_input(prompt_text, key="main_input")
    main_submit = st.form_submit_button("Submit", type="primary")

# Process main input
if main_submit and main_input:
    st.session_state.console_output.append(f"\n> {main_input}")
    
    # New Chat
    if main_input.lower() == "n":
        st.session_state.console_output.append("\nWhat would you like to name this chat?")
        
    # Delete Chat
    elif main_input.lower() == "x":
        if len(st.session_state.chats) != 0:
            st.session_state.console_output.append("\nWhich chat would you like to delete?\n")
            for i in range(len(st.session_state.chats)):
                st.session_state.console_output.append(str(i) + ". " + st.session_state.chats[i])
            st.session_state.console_output.append("\nInput the number of the chat.")
        else:
            st.session_state.console_output.append("\nYou have no chats to delete!")
    
    # Settings
    elif main_input.lower() == "s":
        st.session_state.console_output.append("\nWelcome to Settings!")
        st.session_state.console_output.append("Here you can give TemuGPT certain instructions for his responses. (e.g. Be more concise, be more thorough)")
        st.session_state.console_output.append("Input your settings or press 'X' to exit.")
    
    # Quit
    elif main_input.lower() == "q":
        st.session_state.console_output.append("\nThank you for using TemuGPT! Goodbye!")
    
    # Regular query
    else:
        if len(st.session_state.chats) == 0:
            st.session_state.console_output.append(f"\nNew chat automatically created! — {main_input}")
            st.session_state.chats.append(main_input)
        
        st.session_state.console_output.append("\nLoading... (Might take some time)")
        
        try:
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash-lite',
                system_instruction=st.session_state.system_instruction_change
            )
            response = model.generate_content(main_input)
            st.session_state.console_output.append(f"\nAnswer: \n{response.text}\n")
        except Exception as e:
            st.session_state.console_output.append(f"\nError: {str(e)}\n")
    
    st.rerun()
