# Website Analyzer

A Python utility that automatically analyzes websites and extracts structured information using BeautifulSoup4 and OpenAI's language models. The tool respects web standards by checking `robots.txt` before scraping.

## Features

- **Ethical Web Scraping:** Checks `robots.txt` before attempting to scrape any website
- **Clean HTML Processing:** Removes scripts and styles to focus on meaningful content
- **Intelligent Summarization:** Uses OpenAI API to categorize websites and extract key information
- **Structured Output:** Returns clean JSON following a consistent schema
- **Error Handling:** Gracefully handles blocked websites and invalid content

## Project Overview

This tool demonstrates:
- Web scraping with BeautifulSoup4
- Respecting web standards and `robots.txt`
- Integration with OpenAI API for content analysis
- Structured data extraction and JSON handling
- Professional Python project structure

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup

1. Clone the repository
```bash
git clone https://github.com/leonzalosny/structured-web-analyzer.git
cd structured-web-analyzer
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure API key
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the script to analyze a website:

```bash
python main.py
```

By default, it analyzes CNN's homepage. To analyze a different website, modify the `url` variable in the `if __name__ == "__main__"` block.

### Example Output

```json
{
  "category": "news",
  "summary": "CNN is a major news organization providing breaking news, analysis, and multimedia content across politics, business, technology, and world events.",
  "subjects": ["news", "politics", "business", "technology", "world events"],
  "contextual_analysis": {
    "audience": "general public",
    "tone": "formal",
    "purpose": "inform",
    "notable_features": ["breaking news", "video content", "live updates"]
  }
}
```

## Example Results

The tool successfully analyzes various website types:

| Website | Category | Status |
|---------|----------|--------|
| CNN | News | ✅ Success |
| Golang | Blog | ✅ Success |
| Rust Lang | Documentation | ✅ Success |
| Hacker News | Community | ✅ Success |
| Wikipedia | - | ⛔ Blocked by robots.txt |

## How It Works

1. **robots.txt Check:** Verifies scraping permissions before fetching any content
2. **HTML Cleaning:** Removes `<script>` and `<style>` tags to reduce noise
3. **Content Extraction:** Parses cleaned HTML and sends relevant content to OpenAI
4. **JSON Parsing:** Receives and parses structured JSON response from the model
5. **Error Handling:** Returns informative error messages for blocked or invalid sites

## JSON Schema

The tool returns data following this schema:

```json
{
  "category": "string",
  "summary": "string",
  "subjects": ["string"],
  "contextual_analysis": {
    "audience": "string | null",
    "tone": "string | null",
    "purpose": "string | null",
    "notable_features": ["string"]
  }
}
```

## Project Structure

```
structured-web-analyzer/
├── main.py                   # Main script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore file
├── README.md                 # This file
├── LICENSE                   # Standard MIT License
└── examples/                 # Example outputs
    ├── cnn.json
    ├── golang.json
    ├── rust-lang.json
    ├── ycombinator.json
    └── wikipedia.json
```

## Requirements

- `beautifulsoup4==4.14.2` - HTML parsing
- `openai==2.8.1` - OpenAI API client
- `requests==2.32.5` - HTTP requests
- `python-dotenv==1.2.1` - Environment variable management

## Notes

- The tool respects web standards and only scrapes sites that permit it via `robots.txt`
- Websites with heavy JavaScript rendering (e.g., Amazon, Etsy) may return insufficient content
- The OpenAI API key must be valid and have available credits
- Response time depends on website size and OpenAI API latency

## Future Improvements

- Support for JavaScript-rendered content using Selenium or Playwright
- Batch processing of multiple URLs
- Caching of results to reduce API calls
- Support for different output formats (CSV, XML)
- Custom categorization schemas

## License

MIT License - See LICENSE file for details

## Author

Created by Leon Zalosny as a portfolio project demonstrating web scraping, API integration, and Python best practices.

Connect with me:
- GitHub: [@leonzalosny](https://github.com/leonzalosny)
- LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/leon-zalosny)
