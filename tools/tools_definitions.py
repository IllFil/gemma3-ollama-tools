def get_tools_definitions() -> list:
    """
    Return the JSON tool definitions for the available functions.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_info_chroma",
                "description": "Access the Chroma database containing user documents and perform a similarity search based on the query.",
                "parameters": {
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "A search query string to perform a similarity search."
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_text_from_url",
                "description": "Retrieves page content from a URL. Ensure the URL exactly matches the one provided by the user.",
                "parameters": {
                    "type": "object",
                    "required": ["url"],
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The exact URL from which to extract text."
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_web_results",
                "description": "Searches the web using multiple queries. Useful when the requested info is not available internally or when the user asks for a web search.",
                "parameters": {
                    "type": "object",
                    "required": ["queries", "user_input"],
                    "properties": {
                        "queries": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A search query string for one aspect of the topic."
                            },
                            "description": "An array of search query strings covering different aspects of the topic."
                        },
                        "user_input": {
                            "type": "string",
                            "description": "The exact user input."
                        }
                    }
                }
            }
        },
    {
        "type": "function",
        "function": {
            "name": "add_two_numbers",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "The first number"
                    },
                    "b": {
                        "type": "integer",
                        "description": "The second number"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtract_two_numbers",
            "description": "Subtract two numbers",
            "parameters": {
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "The number from which to subtract"
                    },
                    "b": {
                        "type": "integer",
                        "description": "The number to subtract"
                    }
                }
            }
        }
    }
    ]