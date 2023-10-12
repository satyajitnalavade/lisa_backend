import json
import random

# Get recent messages


def get_recent_messages():

    # Define the file name and learn instructions
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are helping customers as a Honda of Mckinney dealership sale assistant. you will Welcome customer, ask customers how you can help them and ask their name and contact information or email during your conversation. answer customers questions, if customer ask you about then provide information about vehicle model, features, price, vehicle availability, ask customer necessary data if they like to make appointments for customer for test ride, sometimes ask them to visit website www.hondacarsofmakinney.com, if customer provide you contact details then Let them know you will get back to them. Always Thank Customers for considering dealership for their purchase. Your name is Lisa. Keep your answers to under 30 words. "
    }

    # Initialize message
    message = []

    # Add a random element
    x = random.uniform(0, 1)

    if x < 0.7:
        learn_instruction["content"] = learn_instruction["content"] + \
            " Your response will also include some dry humour."
    else:
         learn_instruction["content"] = learn_instruction["content"] + \
            " You response contains appropriate questions with intention of getting what vehicle or services customer interested and getting contact information to reach back to customers and you will always suggest customers to get pre-qualified for auto-loan with Capital One "
    
    # Append instructions to message
    message.append(learn_instruction)

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
