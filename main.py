"""
main.py

Utility to fetch a website's HTML (respecting robots.txt), strip scripts/styles,
and ask the OpenAI API to produce a concise JSON summary following a fixed schema.

Usage:
    Set OPENAI_API_KEY in the environment or a .env file, then run this module.
    The script will attempt to scrape the example URL in the __main__ block
    and print the resulting JSON.

Notes:
    - The scraper checks robots.txt before requesting a page.
    - The OpenAI client is used to produce a single JSON object; the prompt
      enforces strict JSON-only output.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
from urllib.robotparser import RobotFileParser
import json

def can_scrape_url(url):
    """
    Check robots.txt for the given site to determine whether scraping is allowed.

    Args:
        url (str): Base URL of the site to check. Example: "https://example.com"

    Returns:
        bool: True if the user-agent "*" is allowed to fetch the given URL, False otherwise.
    """
    rp = RobotFileParser()
    # Point the parser at the site's robots.txt
    rp.set_url(url + "/robots.txt")
    rp.read()
    return rp.can_fetch("*", url)

def fetch_website_contents(url):
    """
    Retrieve a website's HTML and remove <script> and <style> elements.

    This function first checks robots.txt via can_scrape_url. If scraping is disallowed,
    it returns None.

    Args:
        url (str): Full page URL to fetch.

    Returns:
        str | None: Prettified HTML/text content with scripts/styles removed,
                    or None if scraping is disallowed.
    """
    if can_scrape_url(url) is False:
        return None

    # Perform a simple GET request to fetch the page content
    response = requests.get(url)

    # Parse the HTML and remove script/style blocks to reduce noise
    soup = BeautifulSoup(response.text, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()

    # Return a readable string representation of the cleaned HTML
    return soup.prettify()

def openai_prompt_builder(website_text):
    """
    Build the system and user messages for the OpenAI chat completion API.

    The user message contains a strict instruction to return ONLY a single valid JSON
    object that matches a provided schema. The messages returned are compatible with
    the OpenAI chat API client used in get_website_summary_in_json.

    Args:
        website_text (str): The cleaned website text to be summarized.

    Returns:
        list[dict]: Messages array containing system and user message dictionaries.
    """
    system_message = {
        "role": "system",
        "content": "You are a helpful assistant that summarizes website content in the form of a json."
    }
    user_message = {
        "role": "user",
        "content": f"""Summarize the following website content and return ONLY a single valid JSON object that exactly matches the schema below. Do not include any explanations, notes, or markdown — only the JSON object.

Website content:
{website_text}

Required JSON schema (provide this exact structure; use null or [] when unknown):
{{
  "category": "string, primary category of the website (e.g., \"news\", \"e-commerce\", \"blog\", \"documentation\", \"education\")",
  "summary": "string, concise summary (2-4 sentences)",
  "subjects": ["array of strings, main subjects/topics"],
  "contextual_analysis": {{
    "audience": "string or null, intended audience (e.g., \"developers\", \"general public\")",
    "tone": "string or null (e.g., \"formal\", \"informal\", \"promotional\")",
    "purpose": "string or null (e.g., \"inform\", \"sell\", \"entertain\", \"instruct\")",
    "notable_features": ["array of strings, notable features or elements"]
  }}
}}

Rules:
- Output must be valid JSON parsable by a JSON parser.
- Use null for unknown string fields and [] for unknown lists.
- Keep values concise.
- Do not output any additional keys or metadata.
"""
    }
    messages = [system_message, user_message]
    return messages

# send api request to openai
def get_website_summary_in_json(url):
    """
    Fetch a website, build a prompt, call the OpenAI chat completion API, and parse the JSON.

    The function:
      - Loads environment variables (overrides with .env if present).
      - Initializes the OpenAI client.
      - Verifies OPENAI_API_KEY exists.
      - Fetches website contents (respecting robots.txt).
      - Sends a chat completion request and parses the result as JSON.

    Args:
        url (str): The website URL to summarize.

    Returns:
        dict: Parsed JSON object returned by the model.

    Raises:
        ValueError: If OPENAI_API_KEY is not found in environment variables.
    """
    # Load environment variables (allow .env to override existing values)
    load_dotenv(override=True)

    # Create the OpenAI client; assumes the library picks up the API key from env
    client = OpenAI()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    
    # Retrieve cleaned website contents; respect robots.txt
    website_contents = fetch_website_contents(url)
    if website_contents is None:
        return {
            "error": "Scraping not allowed",
            "url": url,
            "message": "The website's robots.txt disallows scraping."
            }

    # Build messages for the chat completion
    prompt_messages = openai_prompt_builder(website_contents)
    
    # Call the OpenAI chat completion endpoint
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=prompt_messages, 
        temperature=0,
        max_tokens=1000
    )
    
    # Parse the model's textual response as JSON and return it
    try:
        summary_json = json.loads(response.choices[0].message.content)
        return summary_json
    except json.JSONDecodeError as e:
        return {
            "error": "Invalid JSON response",
            "url": url,
            "message": str(e)
        }

if __name__ == "__main__":
    # Example usage: summarize CNN's homepage and print the JSON result
    url = "https://cnn.com"
    result = get_website_summary_in_json(url)
    print(json.dumps(result, indent=2))