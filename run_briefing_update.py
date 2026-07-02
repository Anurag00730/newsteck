import subprocess
import json
import os
import sys

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fetch_path = os.path.join(base_dir, "fetch_news.py")
    update_path = os.path.join(base_dir, "update_briefing.py")
    
    print("--- Starting Full Briefing Update Flow ---")
    
    # 1. Fetch news
    print("Executing fetch_news.py...")
    res = subprocess.run([sys.executable, fetch_path], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("Error during news fetching:", res.stderr)
        sys.exit(1)
        
    # 2. Compile briefing
    print("Executing update_briefing.py...")
    res = subprocess.run([sys.executable, update_path], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("Error during briefing compilation:", res.stderr)
        sys.exit(1)
        
    print("--- Briefing Update Completed Successfully ---")

if __name__ == "__main__":
    main()
