import argparse
import json
import os
from dotenv import load_dotenv

from scraper import scrape_instagram_post
from extractor import extract_recipe_from_text

def main():
    parser = argparse.ArgumentParser(description="NutriPlan Agent: Scrape Instagram and extract recipe.")
    parser.add_argument("url", help="The URL of the Instagram post to scrape.")
    parser.add_argument("--output", "-o", default="recipe_output.json", help="Path to save the output JSON.")
    args = parser.parse_args()

    # Load environment variables (e.g., GEMINI_API_KEY)
    load_dotenv()
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is missing.")
        print("Please create a .env file with your API key or set it in your environment.")
        return

    print(f"--- Starting NutriPlan Agent ---")
    
    # 1. Scrape the URL
    raw_text = scrape_instagram_post(args.url)
    if not raw_text or len(raw_text.strip()) == 0:
        print("Failed to extract any text from the URL.")
        return
    
    print(f"Successfully scraped {len(raw_text)} characters of text.")
    
    # 2. Extract structured data using Gemini
    try:
        recipe_data = extract_recipe_from_text(raw_text)
    except Exception as e:
        print(f"Error during extraction: {e}")
        return
    
    # 3. Output the result
    print("\n--- Extraction Successful ---")
    
    # Convert Pydantic model to dict, then JSON
    recipe_dict = recipe_data.model_dump()
    json_output = json.dumps(recipe_dict, indent=2)
    
    print(json_output)
    
    # Save to file
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(json_output)
        
    print(f"\nSaved structured recipe to: {args.output}")

if __name__ == "__main__":
    main()
