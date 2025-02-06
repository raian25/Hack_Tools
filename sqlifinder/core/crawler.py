from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # Force HTTPS protocol in the URLs
                    if newUrl.startswith("http://"):
                        newUrl = newUrl.replace("http://", "https://")
                    self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        print(f"Opening URL: {url}")  # Verbose output for the URL being opened
        try:
            response = urlopen(url)
            # Check for valid HTML content type
            if response.getheader('Content-Type') == 'text/html':
                htmlBytes = response.read()
                try:
                    # Try decoding with UTF-8 first, fallback to ISO-8859-1
                    htmlString = htmlBytes.decode("utf-8")
                except UnicodeDecodeError:
                    print(f"Error decoding with UTF-8, trying ISO-8859-1")
                    htmlString = htmlBytes.decode("ISO-8859-1")
                self.feed(htmlString)
                print(f"Found {len(self.links)} links on {url}")  # Verbose output for the number of links found
                return htmlString, self.links
            else:
                print(f"Skipping non-HTML content from {url}")  # Verbose output for non-HTML content
                return "", []
        except Exception as e:
            print(f"Error opening URL {url}: {e}")
            return "", []

def spider(url, maxPages):
    links = [] 
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited += 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        print(f"\nVisiting page {numberVisited}: {url}")  # Verbose output for page being visited
        
        try:
            parser = LinkParser()
            data, links = parser.getLinks(url)
            # Add found links to pagesToVisit
            for link in links:
                if link not in pagesToVisit:
                    pagesToVisit.append(link)
                    print(f"Adding link to visit: {link}")  # Verbose output for new links found
        except Exception as e:
            print(f"Error with {url}: {e}")  # Verbose output for errors during processing
            pass
    print(f"\nTotal links found: {len(links)}")  # Verbose output for the final count of found links
    return links

# Test the spider function with HTTPS
print(spider("https://www.estgv.ipv.pt/estgv/", 10))
