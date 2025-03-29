import os
import json
from dotenv import load_dotenv
import google.generativeai as genai 
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def post_to_card(x_post: dict, prioritization_rule: dict, product_description: str):
    """
    Use Gemini to classify an X post.
    
    Parameters:
      x_post (dict): Contains keys "text", "likes", "retweets", and "source".
      gemini_rules (dict): Dynamic priority rules (e.g., as a JSON dict).
      
    Returns:
      dict: Structured output with the following keys:
            {
              "add": bool,
              "card_name": str,
              "priority": "High" | "Medium" | "Low",
              "card_description": str
            }
    """
    # Construct a prompt that gives Gemini the rules and the X post details.
    prompt = f"""
You are an intelligent assistant that determines if an X post (tweet) should be added as a Trello card for a product development.
Here are the dynamic priority rules: (If not set, use your own judgement)
    Prioritization Rule: {json.dumps(prioritization_rule, indent=2)}
Product description: {product_description}

The X post has these properties:
- text: {x_post.get("text", "")}
- likes: {x_post.get("likes", 0)}
- retweets: {x_post.get("retweets", 0)}

Based on the above, generate a structured JSON output that meets the following:
1. "add": A boolean indicating whether to add the post as a Trello card. The post must be relevant to the product and must be one of the defined request types below.
        If it is not one of the following [Bug/Problem Report, Feature Request, or Suggestions to the product], this should be set to false.
2. "card_name": A title determined solely by the content. It must be prefixed by one of:
   "[Bug Report]", "[Feature Request]", "[Improvement Suggestion]", with a concise title for the product development team to understand.
3. "priority": A string "High", "Medium", or "Low" based on the engagement metrics and the given rules.
4. "card_description": A concise yet detailed task description. It should understand what should be done to address what's on the post.
   be written in a clear tone for the team, and end with the source URL if available.

Return only a valid JSON object without any additional text or code wrappers.

Example Output: When add is False

{{
  'add': false,
  'reason': ''
}}

---

Another Example: When add is True

{{
   'add': true,
   'card_name': '[Bug Report] App crashes on startup',
   'priority': 'High',
   'card_description': 'The app crashes immediately on startup. Investigate the issue and provide a fix. Source: x.com/post/12345'
}}
"""

    # Call the Gemini API using the genai client.
    response =  model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "top_p": 0.95,
                }
            )
    response_text = response.text.strip().replace("```json", "").replace('```', '')

    try:
        result = json.loads(response_text)
        return {"success": True, "result": result}
    except Exception as e:
        print(response_text)
        return {"success": False, "error": str(e)}

# Example usage (for testing purposes):
if __name__ == "__main__":
    # Example dynamic rules loaded from an environment variable or defined inline.
    gemini_rules = {
        "High": {"min_likes": 100, "min_retweets": 50},
        "Medium": {"min_likes": 50, "min_retweets": 20},
        "Low": {"min_likes": 10, "min_retweets": 5}
    }

    # Example X post.
    x_post_example = {
        "text": "There is a critical bug causing the app to crash immediately on startup.",
        "likes": 150,
        "retweets": 75
    }

    classification = post_to_card(x_post_example, gemini_rules, "Product ABC: A revolutionary new product.")
    if classification["success"]:
        print(json.dumps(classification["result"], indent=2))
    else:
        print("Error:", classification["error"])