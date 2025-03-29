from services.x import fetch_tweets
from services.gemini import post_to_card
from services.trello import add_trello_card
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def execute_workflow(
    product_name: str,
    product_description: str,
    trello_api_key: str,
    trello_token: str,
    prioritization_rule: str,
    time_period: str = '1d',
    max_tweets: int = 5,
    board_id: str = None,
    board_name: str = "Product Development",
    list_name: str = "Social Media"
):
    start_time = time.time()
    metrics = {
        'time_taken': 0.0,
        'processed_tweets': 0,
        'cards_added': 0,
        'classification_errors': 0,
        'trello_errors': 0
    }
    
    result = {
        "success": True,
        "error": None,
        "stage": None,
        "metrics": metrics
    }

    try:
        # Step 1: Fetch Tweets
        tweets = fetch_tweets(product_name, time_period, max_tweets)
        if not tweets:
            metrics['time_taken'] = time.time() - start_time
            return {**result, "message": "No tweets found"}
        if isinstance(tweets, dict) and tweets.get("success") == False:
            metrics['time_taken'] = time.time() - start_time
            return {
                "success": False,
                "error": tweets.get("error", "Unknown error"),
                "stage": "Fetching Tweets",
                "metrics": metrics
            }

        # Step 2: Process Tweets
        for tweet in tweets:
            metrics['processed_tweets'] += 1
            classification = post_to_card(tweet, prioritization_rule, product_description)
            
            if classification["success"]:
                card = classification["result"]
                if card.get("add", False):
                    # Step 3: Add Card to Trello
                    add_response = add_trello_card(
                        trello_api_key,
                        trello_token,
                        list_name,
                        card["priority"],
                        card["card_name"],
                        card["card_description"],
                        board_id,
                        board_name
                    )
                    
                    if add_response["success"]:
                        metrics['cards_added'] += 1
                        logger.info(f"Added card '{card['card_name']}' to Trello.")
                    else:
                        metrics['trello_errors'] += 1
                        logger.error(f"Failed to add card '{card['card_name']}': {add_response['error']}")
            else:
                metrics['classification_errors'] += 1
                logger.error(f"Classification failed for tweet: {classification['error']}")

        metrics['time_taken'] = time.time() - start_time
        return {**result, "message": "Workflow executed successfully"}

    except Exception as e:
        metrics['time_taken'] = time.time() - start_time
        return {
            "success": False,
            "error": str(e),
            "stage": "Unknown",
            "metrics": metrics
        }