from rag_scraper.scraper import Scraper
from rag_scraper.converter import Converter

# Fetch HTML content
url = "https://docs.astral.sh/uv/"
html_content = Scraper.fetch_html(url)

# Convert to Markdown
markdown_content = Converter.html_to_markdown(
    html=html_content,
    base_url='https:// docs.astral.sh',
    parser_features='html.parser',
    ignore_links=True
)
print(markdown_content)
