# AI Sports Writer

> Automated sports content generation pipeline powered by AI - scrape, summarize, translate, and publish sports news articles with GPT-4.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

AI Sports Writer is an intelligent content automation tool designed for sports media publishers. It streamlines the entire content creation workflow by automatically scraping sports news from international sources, summarizing articles, translating them into multiple languages, refining the content, and publishing to your database—all with minimal human intervention.

Perfect for sports portals, news aggregators, and content teams looking to scale their multilingual content production efficiently.

## Key Features

- **Automated Web Scraping** - Extracts sports news articles from Eurosport and other sources
- **AI-Powered Summarization** - Condenses lengthy articles into concise 200-word summaries using GPT-4
- **Smart Translation** - Translates content from English to Russian with sports-specific terminology awareness
- **Content Refinement** - Rewrites articles for clarity, readability, and grammatical accuracy
- **Database Integration** - Automatically publishes finished articles to MySQL database
- **Continuous Pipeline** - Runs autonomously on a configurable schedule
- **Duplicate Prevention** - Smart tracking prevents reprocessing of already published content

## How It Works

The pipeline operates in five sequential stages:

```
┌─────────┐    ┌───────────┐    ┌───────────┐    ┌─────────┐    ┌──────────┐
│ Scrape  │ -> │ Summarize │ -> │ Translate │ -> │ Rewrite │ -> │ Publish  │
└─────────┘    └───────────┘    └───────────┘    └─────────┘    └──────────┘
   Raw            Concise          Russian         Refined         Database
  Articles        Summaries        Version         Content         Storage
```

1. **Scrape** - Fetches latest sports articles from configured sources
2. **Summarize** - Reduces articles to essential information using GPT-4
3. **Translate** - Converts content to target language (Russian by default)
4. **Rewrite** - Polishes translated content for publication quality
5. **Publish** - Stores final articles in MySQL database and cleans up temporary files

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL database
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/stukenov/ai-sports-writer.git
cd ai-sports-writer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```ini
[DEFAULT]
OPENAI_API_KEY=your_openai_api_key_here

[MYSQL]
USER=your_mysql_username
PASSWORD=your_mysql_password
HOST=127.0.0.1
DATABASE=your_database_name
RAISE_ON_WARNINGS=True
```

4. Set up your MySQL database:
```sql
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ru_title VARCHAR(255) NOT NULL,
    ru_fulltxt TEXT NOT NULL,
    ru_pubdate DATETIME NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

5. Create content directories:
```bash
mkdir -p content/{scraped,summarized,translated,rewrited,completed}
```

## Usage

### Run the Complete Pipeline

Execute the main orchestrator to run all stages continuously:

```bash
python main.py
```

The pipeline will run every 2 minutes, processing new articles automatically.

### Run Individual Stages

You can also run each stage independently for testing or custom workflows:

```bash
# Scrape articles only
python scrape.py

# Summarize scraped content
python summarize.py

# Translate summaries
python translate.py

# Rewrite translated content
python rewrite.py

# Publish to database
python write.py
```

## Project Structure

```
ai-sports-writer/
├── main.py              # Pipeline orchestrator
├── scrape.py           # Web scraping module
├── summarize.py        # AI summarization module
├── translate.py        # Translation module
├── rewrite.py          # Content refinement module
├── write.py            # Database publishing module
├── utils.py            # Configuration utilities
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── content/           # Processing directories
    ├── scraped/       # Raw scraped articles
    ├── summarized/    # AI summaries (JSON)
    ├── translated/    # Translated content (JSON)
    ├── rewrited/      # Refined articles (JSON)
    └── completed/     # Published articles archive
```

## Configuration

### Customizing the Pipeline

**Change the scraping source:**
Edit `scrape.py` to modify the target URL or add new sources.

**Adjust summary length:**
Modify the prompt in `summarize.py` to change the target word count.

**Change target language:**
Update the translation prompt in `translate.py` for different languages.

**Modify cycle interval:**
Change the `time.sleep(120)` value in `main.py` (default: 2 minutes).

## API Usage & Costs

This tool uses OpenAI's GPT-4 API, which incurs costs based on token usage:
- Summarization: ~1-2 requests per article
- Translation: ~1 request per article
- Rewriting: ~1 request per article

**Estimated cost:** $0.03-0.10 per article (varies by article length)

Monitor your usage at [OpenAI Platform](https://platform.openai.com/usage).

## Requirements

All dependencies are listed in `requirements.txt`:

- **openai** - GPT-4 API integration
- **beautifulsoup4** - HTML parsing for web scraping
- **requests** - HTTP client for web requests
- **mysql-connector-python** - MySQL database connectivity
- Other supporting libraries (see requirements.txt)

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [ ] Support for additional sports news sources
- [ ] Multi-language support beyond Russian
- [ ] Web dashboard for monitoring pipeline
- [ ] PostgreSQL and MongoDB support
- [ ] Docker containerization
- [ ] Cloud deployment guides (AWS, GCP, Azure)
- [ ] RSS feed generation
- [ ] WordPress integration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is designed for legitimate content aggregation and translation purposes. Users are responsible for:
- Complying with the terms of service of scraped websites
- Respecting copyright and attribution requirements
- Following local laws regarding automated web scraping
- Properly attributing original sources in published content

## Support

For questions, issues, or feature requests:
- Open an issue on [GitHub Issues](https://github.com/stukenov/ai-sports-writer/issues)
- Contact: [your contact method]

## Acknowledgments

- Powered by [OpenAI GPT-4](https://openai.com/)
- Sports news sourced from Eurosport
- Built with Python and open-source libraries

---

**Made with AI by Saken Tukenov** | [GitHub](https://github.com/stukenov)
