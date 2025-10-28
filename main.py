#Welcome to TemuGPT -_-
#Do not touch the code unless you know what you are doing!
#You were supposed to make a copy of this code if you want to edit it; do not edit the my original version.
#There are small pauses in the code to make the AI feel less rushed; if you want to get rid of this find all time.sleep() functions and delete them.
#I am working on a TemuGPT version that uses Tkinter to have an actual application with GUI instead of just a console. Mkae sure to check that out when I am finished with it.

import google.generativeai as genai
import time

genai.configure(
    api_key="AIzaSyDAm1jtwFCjZhkiDtG4SmwQXwikfdDQLpE")  #type: ignore

system_instruction_change = "You are a generalized helpful assistant that helps with users' tasks."

chats = []
chat_end = False
while not chat_end:
    model = genai.GenerativeModel(  #type: ignore
        model_name='gemini-2.5-flash-lite',
        system_instruction=system_instruction_change)
    if len(chats) != 0:
        user_input = input(
            "What would you like to do? (Ask, New Chat (N), Delete Chat (X), Settings (S), Quit (Q))\n\nType here: "
        )
    else:
        user_input = input(
            "-----------------------Welcome to TemuGPT! Press 'N' to start a new chat, 'X' to delete a chat, 'S' for settings, and 'Q' to quit. How may TemuGPT help you today?-----------------------\n\nType here: "
        )
    if user_input == "N" or user_input == "n":
        chat_name = input("What would you like to name this chat?\n\n")
        chats.append(chat_name)
    elif user_input == "X" or user_input == "x":
        if len(chats) != 0:
            print("Which chat would you like to delete?\n\n")
            for i in range(len(chats)):
                print(str(i) + ". " + chats[i])
            chat_to_del = int(input("Input the number of the chat.\n\n"))
            chats.remove(chats[(chat_to_del - 1)])
            if len(chats) != 0:
                print("Chat deleted! Here are you current chats:")
                print(f"{str(chats)}\n\n")

            elif len(chats) == 0:
                print("Chat deleted! You have no more chats.")
        elif len(chats) == 0:
            print("You have no chats to delete!")
    elif user_input == "S" or user_input == "s":
        print(
            "Welcome to Settings!\nHere you can give TemuGPT certain instructions for his reponses. (e.g. Be more concise, be more thorough) "
        )
        system_in = str(input("Input your settings or press 'X' to exit.\n"))
        if system_in == "X":
            next
        else:
            print("Settings changed!")
            system_instruction_change = system_in
            time.sleep(.5)
            next

    else:
        if len(chats) == 0:
            print(f"\nNew chat automatically created! — {user_input}")
            chats.append(user_input)
        time.sleep(.5)
        print("Loading... (Might take some time)")
        response = model.generate_content(user_input)
        print(f"\nAnswer: \n{response.text}\n")
    time.sleep(.5)
