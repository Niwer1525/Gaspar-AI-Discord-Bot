import torch
from transformers import pipeline
import sys
import tools
import re
import history
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# pipe = pipeline("text-generation", model=model_name, device_map='cuda' if torch.cuda.is_available() else 'cpu').to(device)
pipe = pipeline("text-generation", model=history.model_large, torch_dtype=torch.bfloat16, device_map='cuda')
pipe.model.to(device)

# Disable safetensors to speed up generation (And because we don't need it for this use case)
pipe.model.config.update({"use_safetensors": False})

def generate_text(input_text):
    with torch.no_grad():
        # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
        messages = [{"role": "system","content": history.system_prompt}]

        # Add history to the messages
        for obj in history.get_chat_history_objects():
            messages.append(obj)

        # Add the user's input to the messages
        messages.append({"role": "user", "content": input_text})

        # Generate the response
        prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False, return_tensors="pt") # tools=tools.tools_list,
        outputs = pipe(prompt, max_new_tokens=64, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        return outputs[0]["generated_text"]

def clean_text(text):
    start_marker = "assistant"
    start_index = text.lower().rfind(start_marker)
    if start_index != -1:
        return text[start_index + len(start_marker):].strip()
    return text.strip()

def get_message_id(text):
    match = re.search(r'<(\d+)>', text)
    if match:
        return f'<{match.group(1)}>'
    return ""

def remove_message_id(text):
    return re.sub(r'<\d+>', '', text)

# Loop to continuously receive data
for line in sys.stdin:
    received_data = line.strip() # Remove blank lines
    message_id = get_message_id(received_data) # Extract message ID
    received_data = remove_message_id(received_data) # Remove message ID from the text

    output_text = generate_text(received_data) # Generate text
    cleaned_output_text = clean_text(output_text) # Clean the text (Get only the assistant's response)
    sys.stdout.buffer.write((message_id+cleaned_output_text+"\n").encode('utf-8')) # Echo back the received data

    history.write_to_history(received_data, cleaned_output_text) # Write to history

    # sys.stdout.buffer.write((message_id+received_data).encode('utf-8')) # Echo back the received data
    sys.stdout.flush() # Empty the output buffer to ensure immediate sending