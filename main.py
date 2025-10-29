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
if 'disclaimer_finish' not in st.session_state:  # Fixed typo here
    st.session_state.disclaimer_finish = False

# Title
st.title("TemuGPT")

# DISCLAIMER SCREEN
if not st.session_state.disclaimer_finish:
    st.text("DISCLAIMER: Please do not abuse this AI in any way. It is supposed to be an assistant—don't try to break school policy in any way.")
    dis_text = "Type 'I solemnly swear that I will abide by these rules' if you agree to these rules."
    
    with st.form(key="input_dis", clear_on_submit=True):  
        user_input_dis = st.text_input(dis_text, key="user_input_dis")    
        submit_button_dis = st.form_submit_button("Submit", type="primary")
    
    if submit_button_dis and user_input_dis:
        if user_input_dis == "I solemnly swear that I will abide by these rules":  # Fixed variable name
            st.session_state.disclaimer_finish = True  # Fixed typo
            st.session_state.console_output = [  # Initialize console output
                "Accepted! Starting TemuGPT...",
                "Welcome to TemuGPT!", 
                "Press 'N' to start a new chat, 'X' to delete a chat, 'S' for settings, and 'Q' to quit.", 
                "\nHow may TemuGPT help you today?"
            ]
            st.rerun()
            time.sleep(.5)
        else:
            st.error("Please type the exact statement: 'I solemnly swear that I will abide by these rules'")
            time.sleep(.5)

# MAIN SCREEN (only shows after disclaimer accepted)
else:
    # Console output
    console_container = st.container()
    with console_container:
        for line in st.session_state.console_output:
            st.text(line)
    
    # Input area - ONLY SHOW AFTER DISCLAIMER
    if len(st.session_state.chats) != 0:
        prompt_text = "What would you like to do? \n(Ask Something, New Chat (N), Delete Chat (X), Settings (S), Quit (Q))"
    else:
        prompt_text = "Type here:"
    
    with st.form(key="input_form", clear_on_submit=True):  
        user_input = st.text_input(prompt_text, key="user_input")    
        submit_button = st.form_submit_button("Submit", type="primary")

    if submit_button and user_input:
        st.session_state.console_output.append(f"\n> {user_input}")

        # New Chat
        if user_input.lower() == "n":
            time.sleep(.5)
            st.session_state.console_output.append("\nWhat would you like to name this chat?")

        # Delete Chat
        elif user_input.lower() == "x":
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
        elif user_input.lower() == "s":
            time.sleep(.5)
            st.session_state.console_output.append("\nWelcome to Settings!")
            st.session_state.console_output.append("Here you can give TemuGPT certain instructions for his responses. (e.g. Be more concise, be more thorough)")
            st.session_state.console_output.append("Input your settings or press 'X' to exit.")

        # Quit command (added missing)
        elif user_input.lower() == "q":
            time.sleep(.5)
            st.session_state.console_output.append("\nThank you for using TemuGPT! Goodbye!")

        # Regular query
        else:
            if len(st.session_state.chats) == 0:
                st.session_state.console_output.append(f"\nNew chat automatically created! — {user_input}")
                st.session_state.chats.append(user_input)

            try:
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',  # Changed to more common model
                    system_instruction=st.session_state.system_instruction_change
                )
                time.sleep(.5)
                st.session_state.console_output.append("\nLoading... (Might take some time)")
                response = model.generate_content(user_input)
                time.sleep(.5)
                st.session_state.console_output.append(f"\nAnswer: \n{response.text}\n")
            except Exception as e:
                st.session_state.console_output.append(f"\nError: {str(e)}\n")

        st.rerun()
