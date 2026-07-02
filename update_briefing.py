import json
import os
import sys

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, "raw_news.json")
    output_path = os.path.join(base_dir, "briefing.json")
    
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found. Please run fetch_news.py first.")
        sys.exit(1)
        
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Briefing compiled successfully at {output_path}")

if __name__ == "__main__":
    main()
