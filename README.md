# Article Scraper

A professional web scraping tool built with Python 3.12 and Selenium WebDriver for extracting article data from Brewin Dolphin's insights page.

## Features

- **Automated Web Scraping**: Automatically navigates and scrapes article links from target websites
- **Dynamic Content Loading**: Handles "Load More" buttons to collect all available articles
- **Article Content Extraction**: Extracts titles, descriptions, and full content from individual articles
- **CSV Export**: Saves scraped data in CSV format for easy analysis
- **Error Handling**: Robust exception handling for reliable scraping operations
- **Chrome WebDriver Integration**: Uses Chrome browser automation with automatic driver management

## Prerequisites

- Python 3.12 or higher
- Google Chrome browser
- Internet connection
- Sufficient disk space for CSV output files

## Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Alternative for some systems
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create Requirements File (if not exists)

```bash
pip install selenium webdriver-manager
pip freeze > requirements.txt
```
## How It Works

### 1. Link Collection Phase
- Opens the target website using Chrome WebDriver
- Automatically clicks "Discover More" buttons to load all available articles
- Extracts article links from the page
- Saves links to `post_links.csv`

### 2. Content Extraction Phase
- Reads the collected links from CSV
- Visits each article page individually
- Extracts:
  - Article title
  - Article description
  - Full article content (paragraphs, headings, lists)
- Saves detailed data to `article_details.csv`

## Output Files

### post_links.csv
Contains all collected article URLs, one per row.

### article_details.csv
Contains detailed article information with columns:
- **Link**: Article URL
- **Title**: Article headline
- **Description**: Article summary/description
- **Content**: Full article text content

## Configuration

### Customizing Target URL

```python
# Change the target URL in the main section
url = "https://your-target-website.com/articles"
scraper = ArticleScraper(url)
```

### Modifying Output Paths

```python
# Update CSV paths in the ArticleScraper class
self.csv_path = "/path/to/your/post_links.csv"
output_csv_path = "/path/to/your/article_details.csv"
```


## Project Structure

```
article-scraper/
├── article_scraper.py      # Main scraper class
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore            # Git ignore rules
├── venv/                 # Virtual environment (not tracked)
├── post_links.csv        # Generated link collection
└── article_details.csv   # Generated article data
```
