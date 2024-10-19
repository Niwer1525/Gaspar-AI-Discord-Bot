import json
import os

# Get system prompt from json
with open('config.json', 'r') as f:
    json_content = json.load(f)
    system_prompt = json_content.get('system_prompt')
    model_small = json_content.get('model_small')
    model_medium = json_content.get('model_medium')
    model_large = json_content.get('model_large')

def get_chat_history_objects():
    # Check if the history file exists and is not empty
    if os.path.exists('history.json') and os.path.getsize('history.json') > 0:
        # Read the existing data
        with open('history.json', 'r') as history_file:
            try:
                existing_data = json.load(history_file)
            except json.JSONDecodeError:
                existing_data = {"history": []}  # If the file is corrupt, start fresh
    else:
        existing_data = {"history": []}  # Start fresh if the file doesn't exist or is empty

    return existing_data["history"]

def write_to_history(received_data, cleaned_output_text):
    """ Add the assistant's response & user prompt to the history.
        {
            {
                "role": "user"
                "content": "User's prompt"
            }
            {
                "role": "asistant"
                "content": "Assistant's response"
            }
        }
    """

    # Create history entry
    history_entry = [{"role": "user","content": received_data},{"role": "assistant","content": cleaned_output_text}]
    
    # Check if the history file exists and is not empty
    if os.path.exists('history.json') and os.path.getsize('history.json') > 0:
        # Read the existing data
        with open('history.json', 'r') as history_file:
            try:
                existing_data = json.load(history_file)
            except json.JSONDecodeError:
                existing_data = {"history": []}  # If the file is corrupt, start fresh
    else:
        existing_data = {"history": []}  # Start fresh if the file doesn't exist or is empty
    
    # Append new entries to the existing "history"
    existing_data["history"].extend(history_entry)
    
    # Write the updated history back to the file
    with open('history.json', 'w') as history_file:
        json.dump(existing_data, history_file, ensure_ascii=False)