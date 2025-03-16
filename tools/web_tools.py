import json
import re
import html
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from ollama import chat
from pydantic import BaseModel
from typing import List

from utils.helper_func import random_delay


class PageSummary(BaseModel):
    """
    Schema for summarizing a webpage with a title and a concise content summary.

    Attributes:
        title (str): The title or name of the webpage.
        content (str): A concise summary capturing key information from the webpage.
    """
    title: str
    content: str


def get_prompt(user_input: str, text: str) -> object:
    """
    Generate prompt messages for the AI assistant to analyze a webpage.

    This function returns a list of system message dictionaries which instruct the AI
    assistant to analyze the provided webpage text according to the user input question.
    The response is expected to adhere to a specific JSON schema containing a title and content.

    Args:
        user_input (str): The user question that guides the analysis.
        text (str): The raw text content of the webpage.

    Returns:
        list: A list of dictionaries formatted as system messages for the AI model.
    """
    return [
        {
            "role": "system",
            "content": (
                f"You are a helpful AI assistant. Your task is to analyze a webpage and provide an output focus on this user question {user_input}"
                "that follows the schema below:\n\n"
                "  title: str\n"
                "  content: str\n\n"
                "Where:\n"
                "- 'title' is the name of the page,\n"
                "- 'content' is a concise summary of the webpage that captures all key information.\n\n"
                "Ensure accuracy, clarity, and conciseness in your analysis."
                "Return a list in JSON format"
            ),
        },
        {
            "role": "system",
            "content": f"Web page: {text}"
        }
    ]


def search(query):
    """
    Perform a search query on Bing using Playwright and retrieve search result links.

    This function launches a headless Chromium browser, navigates to Bing, and executes
    the provided search query. It mimics human behavior by introducing random delays, checks
    for unusual traffic warnings, and finally extracts the URLs of the first two search results.

    Args:
        query (str): The search query string.

    Returns:
        list: A list of URLs (strings) from the first two search results.
              If an error occurs or unusual traffic is detected, the function may return None.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/95.0.4638.54 Safari/537.36"
            )
        )
        page = context.new_page()

        page.goto("https://bing.com")
        random_delay(2, 4)

        page_content = page.content()
        if "Our systems have detected unusual traffic" in page_content:
            print("Unusual traffic detected. Pausing to mimic human behavior.")
            random_delay(10, 20)
            browser.close()
            return

        search_selector = "textarea[name='q']"
        try:
            page.wait_for_selector(search_selector, timeout=10000)
        except Exception as e:
            print("Search input did not appear:", e)
            browser.close()
            return

        page.fill(search_selector, query)
        random_delay(0.5, 1)
        page.keyboard.press("Enter")

        try:
            page.wait_for_selector("h3", timeout=10000)
            random_delay(1, 2)
        except Exception as e:
            print("Search results not found:", e)

        results = page.query_selector_all("li.b_algo h2 a")
        first_five_links = [result.get_attribute("href") for result in results[:2]]
        print(first_five_links)

        browser.close()
        return first_five_links


def get_text_from_url(url):
    """
    Retrieve and clean the text content from a given URL.

    This function uses Playwright to navigate to the specified URL, retrieves the page's HTML content,
    and then processes it with BeautifulSoup to extract and clean the textual information.
    The cleaning process includes normalizing whitespace, unescaping HTML entities,
    replacing fancy quotes, and removing non-ASCII and control characters.

    Args:
        url (str): The URL of the webpage to fetch and process.

    Returns:
        str: The cleaned text content from the webpage.
             If an error occurs during retrieval, returns an error message including the URL.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            try:
                page.goto(url)
            except Exception as e:
                browser.close()
                raise RuntimeError(f"Failed to load the page: {e}")

            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            text_content = soup.get_text()
            text_content = re.sub(r'\s+', ' ', text_content)
            text_content = html.unescape(text_content)
            # Replace fancy quotes and apostrophes with standard ones
            text_content = text_content.replace("“", '"').replace("”", '"').replace("’", "'")
            # Remove control characters (0x00-0x1F and 0x7F)
            text_content = re.sub(r'[\x00-\x1F\x7F]', '', text_content)
            # Remove non-ASCII characters (keeps only characters from space (0x20) to tilde (0x7E))
            text_content = re.sub(r'[^\x20-\x7E]', '', text_content)
            # Normalize whitespace to a single space
            text_content = re.sub(r'\s+', ' ', text_content)
            browser.close()
            return text_content
    except Exception as e:
        return f"During link search error occurred check the link check the link {url} try again"


def get_text_from_links(links: List[str], user_input: str) -> str:
    """
    Process multiple webpage links to generate summarized outputs.

    For each link provided, this function retrieves the webpage's text, constructs a prompt
    for the AI assistant based on the user's input, and calls an AI model to obtain a summary.
    The resulting summaries are aggregated and returned as a JSON-formatted string.

    Args:
        links (List[str]): A list of webpage URLs.
        user_input (str): The user's question that guides the summarization process.

    Returns:
        str: A JSON-formatted string containing a list of summarized webpage data.
    """
    combined_results = []
    for link in links:
        text = get_text_from_url(link)
        messages = get_prompt(user_input, text)
        model_response = chat(
            model="gemma3-4b-tools",
            messages=messages,
            format=PageSummary.model_json_schema(),
            options={'temperature': 0},
        )
        response = PageSummary.model_validate_json(model_response.message.content)
        combined_results.append(response)
    return json.dumps([result.model_dump() for result in combined_results])


def get_web_results(queries: List[str], user_input: str) -> str:
    """
    Perform web searches for multiple queries and compile summarized results.

    For each query, this function retrieves relevant webpage links using the search function,
    processes each link to extract and summarize the content, and aggregates all the summaries
    into a JSON-formatted string.

    Args:
        queries (List[str]): A list of search query strings.
        user_input (str): The user's question to guide the summarization process.

    Returns:
        str: A JSON-formatted string containing summarized results for each query.
    """
    combined_results = []
    for query in queries:
        links = search(query)
        response = get_text_from_links(links, user_input=user_input)
        combined_results.append(response)
    return json.dumps(combined_results)
