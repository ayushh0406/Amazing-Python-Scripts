from chatterbot import ChatBot
import os

# Naming the ChatBot calculator using mathematical evaluation logic.
# The calculator AI will not learn with the user input.
Bot = ChatBot(name='Calculator',
              read_only=True,
              logic_adapters=["chatterbot.logic.MathematicalEvaluation"],
              storage_adapter="chatterbot.storage.SQLStorageAdapter")

# Clear the screen and start the calculator.
os.system('cls' if os.name == 'nt' else 'clear')
print("Hello, I am a calculator. How may I help you?")

while True:
    # Take the input from the user.
    user_input = input("me: ")

    # Check if the user has typed quit to exit the program.
    if user_input.lower() == 'quit':
        print("Exiting")
        break

    # Otherwise, evaluate the user input.
    # Print invalid input if the AI is unable to comprehend the input.
    try:
        response = Bot.get_response(user_input)
        print("Calculator:", response)
    except:
        print("Calculator: Please enter valid input.")
