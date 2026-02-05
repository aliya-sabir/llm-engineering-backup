from bs4 import BeautifulSoup
import requests


# Standard headers to fetch a website
# Many websites block bots or return different content to non-browsers.
# By setting a User-Agent, you pretend to be a real Chrome browser
# so the site is more likely to respond normally.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    # Return the title and contents of the website at the given url
    # Truncate to 2,000 characters as a sensible limit

    # Send an HTTP GET request to the URL using fake browser headers
    # response.content contains the raw HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # If <title> exists, grab its text
    # Otherwise, use a fallback string to avoid crashes
    title = soup.title.string if soup.title else "No title found"

    if soup.body:
        # Remove junk elements that are not useful for text analysis
        # <script>  → JavaScript
        # <style>   → CSS
        # <img>     → images
        # <input>   → forms
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()

        # Pull all remaining text from the body
        # separator="\n" puts newlines between elements
        # strip=True removes extra whitespace
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""

    # Combine title and body text
    # Truncate to 2,000 characters to avoid huge outputs
    # (especially useful when feeding text to LLMs)
    return (title + "\n\n" + text)[:2_000]


def fetch_website_links(url):
    # Return the links on the website at the given url
    # This re-parses the page and is intentionally simple for lab use

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all <a> (anchor) tags
    # Extract their href attribute
    # Results in a list like:
    # ["https://example.com", "/about", None, "#section"]
    links = [link.get("href") for link in soup.find_all("a")]

    # Remove empty or None links
    return [link for link in links if link]
