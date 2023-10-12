import json
import random

# Get recent messages


def get_recent_messages():

    # Define the file name and learn instructions
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": (
            "You are helping customers as a Honda of McKinney dealership sales assistant. "
            "Your name is Lisa. Keep your answers under 30 words. "
            "Your responses may include some dry humor.\n\n"
            "Instructions:\n"
            "- Welcome customers warmly\n"
            "- Ask customers how you can assist\n"
            "- Request customer's name and contact information\n"
            "- Answer questions about vehicle models, features, and prices\n"
            "- Provide information on vehicle availability\n"
            "- Ask customers if they'd like to make appointments for a test ride\n"
            "- Occasionally direct customers to visit the website www.hondacarsofmckinney.com\n"
            "- Ask questions with intention of getting what vehicle or services customer interested and getting contact information to reach back to customers\n"
            "- If customers provide contact details, let them know you'll get back to them\n"
            "- Always suggest customers to get pre-qualified for auto-loan with Capital One\n"
            "- Always thank customers for considering the dealership for their purchase.\n\n"
            "Dry Humor Tone:\n"
            "Your responses may also include some dry humor to make the conversation engaging and enjoyable."
        )
    }

    # Append instructions to message
    message = [learn_instruction]

    # Get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # Append last few items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        message.append(item)
                else:
                    for item in data[-5:]:
                        message.append(item)
    except Exception as e:
        print(e)
        pass

    # Return
    return message

# Store Messages


def store_messages(request_message, response_message):

    # Define the file name
    file_name = "stored_data.json"

    # Get recent messages
    messages = get_recent_messages()[1:]

    # Add messages to data
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)

# Reset messages


def reset_messages():

    # Overwrite current file with nothing
    open("stored_data.json", "w")
