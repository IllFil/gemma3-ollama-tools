import json
import logging

from ollama import chat, ChatResponse

from tools.chroma_tools import get_info_chroma
from tools.other_tools import add_two_numbers, subtract_two_numbers
from tools.tools_definitions import get_tools_definitions
from tools.web_tools import get_text_from_url, get_web_results


def get_initial_messages() -> list:
    """
    Return the initial conversation history.
    """
    messages = [
        {'role': 'system', 'content': 'You are helpful AI assistant.'},
        {'role': 'user', 'content': 'What are the best practices in modern AI research?Search the web'},
    ]
    logging.info("Initial conversation history: %s", json.dumps(messages, indent=2))
    return messages


def get_available_functions() -> dict:
    """
    Return a mapping of tool names to their function implementations.
    """
    return {
        'get_text_from_url': get_text_from_url,
        'get_info_chroma': get_info_chroma,
        'get_web_results': get_web_results,
        'add_two_numbers': add_two_numbers,
        'subtract_two_numbers': subtract_two_numbers,
    }


def process_tool_call(tool, available_functions: dict, messages: list) -> list:
    """
    Process a single tool call from the chat response.
    Calls the corresponding function and updates the conversation history.
    """
    tool_name = tool.function.name
    tool_args = tool.function.arguments
    logging.info("Processing tool call: %s with arguments: %s", tool_name, tool_args)

    function_to_call = available_functions.get(tool_name)
    if function_to_call:
        output = function_to_call(**tool_args)
        logging.info("Output from %s: %s", tool_name, output)
    else:
        logging.error("Function %s not found", tool_name)
        output = None
    tool_data = {
        "name": tool.function.name,
        "arguments": tool.function.arguments
    }

    messages.append({
        'role': 'system',
        'content': json.dumps(tool_data)
    })
    messages.append({
        'role': 'tool',
        'content': str(output),
        'name': tool_name,
    })
    return messages


def run_chat():
    """
    Main loop for sending messages to the chat API and processing tool calls.
    """
    messages = get_initial_messages()
    tools_definitions = get_tools_definitions()
    available_functions = get_available_functions()

    while True:
        logging.info("Calling chat API with model 'gemma3-12b-tools'...")
        response: ChatResponse = chat(
            'gemma3-12b-tools', messages=messages, tools=tools_definitions, options={'temperature': 0})
        logging.info("Raw response from model: %s",
                     json.dumps(response.message.__dict__, default=lambda o: o.__dict__, indent=2))

        if response.message.tool_calls:
            for tool in response.message.tool_calls:
                messages = process_tool_call(tool, available_functions, messages)
            logging.info("Updated conversation history: %s",
                         json.dumps(messages, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o),
                                    indent=2))
            continue
        else:
            final_response = response.message.content
            logging.info("Final response from model: %s", final_response)
            break