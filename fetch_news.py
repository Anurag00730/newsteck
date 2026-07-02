import urllib.request
import xml.etree.ElementTree as ET
import json
import email.utils
from datetime import datetime, timezone
import os

FEEDS = {
    "world": "https://news.google.com/rss/search?q=world+news+when:1d&hl=en-US&gl=US&ceid=US:en",
    "ai": "https://news.google.com/rss/search?q=Artificial+Intelligence+LLM+ChatGPT+when:1d&hl=en-US&gl=US&ceid=US:en",
    "markets": "https://news.google.com/rss/search?q=stock+market+finance+economy+when:1d&hl=en-US&gl=US&ceid=US:en"
}

def fetch_feed(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_rss(xml_data, max_items=8):
    if not xml_data:
        return []
    
    try:
        root = ET.fromstring(xml_data)
        items = []
        now = datetime.now(timezone.utc)
        
        for item in root.findall('.//item'):
            title = item.find('title')
            link = item.find('link')
            pub_date = item.find('pubDate')
            source = item.find('source')
            
            pub_date_str = pub_date.text if pub_date is not None else ""
            if not pub_date_str:
                continue
                
            try:
                dt = email.utils.parsedate_to_datetime(pub_date_str)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                diff = now - dt
                if diff.total_seconds() > 24 * 3600:
                    continue  # Skip items older than 24 hours
            except Exception as e:
                print(f"Error parsing date {pub_date_str}: {e}")
                continue
                
            # Clean up title (Google News appends " - Source")
            title_text = title.text if title is not None else "No Title"
            source_text = source.text if source is not None else "Unknown Source"
            
            if title_text.endswith(f" - {source_text}"):
                title_text = title_text[:-len(source_text) - 3].strip()
                
            items.append({
                "title": title_text,
                "link": link.text if link is not None else "",
                "pubDate": pub_date_str,
                "source": source_text
            })
            
            if len(items) >= max_items:
                break
        return items
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return []

def main():
    print("Starting news fetch...")
    result = {
        "date": datetime.now().strftime("%B %d, %Y"),
        "timestamp": datetime.now().strftime("%I:%M %p"),
        "sections": {}
    }
    
    for section, url in FEEDS.items():
        print(f"Fetching {section} news...")
        xml_data = fetch_feed(url)
        articles = parse_rss(xml_data)
        result["sections"][section] = articles
        print(f"Found {len(articles)} articles for {section}.")
        
    # Write to raw_news.json
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_news.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully wrote raw news to {output_path}")

if __name__ == "__main__":
    main()
