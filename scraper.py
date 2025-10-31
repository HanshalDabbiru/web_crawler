import re
import tokenizer
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urldefrag, urljoin

valid_urls = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu"]
visited_urls = set()
subdomains = {}
total_freq = {}
longest_page = ("", 0)

def stats():
    return visited_urls, total_freq, subdomains, longest_page

def unique_subdomains(url):
    parsed = urlparse(url).netloc
    subdomains[parsed] = subdomains.get(parsed, 0) + 1

def scraper(url, resp):
    if resp.status < 200 or resp.status > 299:
        return []
    
    content_string = resp.raw_response.content.decode("utf-8", errors="replace")
    soup = BeautifulSoup(content_string, "lxml")

    links = extract_next_links(url, resp, soup)
    update_token_counts(url, soup)
    return [link for link in links if is_valid(link)]

def update_token_counts(url, soup):
    global longest_page

    text = soup.get_text(separator=' ', strip=True)
    tokens = tokenizer.tokenize(text)
    freqs = tokenizer.computeWordFrequencies(tokens)
    for word, f in freqs.items():
        total_freq[word] = total_freq.get(word, 0) + f

    if len(tokens) > longest_page[1]:
        longest_page = (url, len(tokens))


def extract_next_links(url, resp, soup):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    links = []
    for link in soup.find_all("a", href=True):
        url_defrag, _ = urldefrag(link["href"])
        absolute_url = urljoin(resp.url, url_defrag)
        links.append(absolute_url)
    return links



def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        if url in visited_urls:
            return False
        else:
            visited_urls.add(url)
        if re.search(r"(ical|login|events/)", url, re.IGNORECASE): 
            return False

        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        # Makes sure the url is in one of the allowed domains
        pattern = "(" + "|".join(re.escape(url) for url in valid_urls) + ")" 
        if not re.search(pattern, parsed.netloc):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
    except ValueError:
        return False
