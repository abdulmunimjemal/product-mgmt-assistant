import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
API_KEY = os.getenv('TRELLO_API_KEY')
TOKEN = os.getenv('TRELLO_TOKEN')
BOARD_ID = os.getenv('TRELLO_BOARD_ID')          # Optional: Use this if you already have a board id
BOARD_NAME = os.getenv('TRELLO_BOARD_NAME')      # Optional: Use this if you want to create/find a board by name
LIST_NAME = os.getenv('TRELLO_LIST_NAME') or "Social Media Sentiments"

# Check that critical credentials exist
missing_vars = []
if not API_KEY:
    missing_vars.append('TRELLO_API_KEY')
if not TOKEN:
    missing_vars.append('TRELLO_TOKEN')
if not (BOARD_ID or BOARD_NAME):
    missing_vars.append('TRELLO_BOARD_ID or TRELLO_BOARD_NAME')

if missing_vars:
    raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

def get_or_create_board(api_key, token, board_id=None, board_name=None):
    """
    Retrieve a board by ID or by name. If board_id is provided, use it.
    Otherwise, if board_name is provided, search among the user's boards and return the matching board id.
    If no matching board is found, create a new board with that name.
    """
    if board_id:
        # Assume provided board_id is valid.
        print(f"Using provided board ID: {board_id}")
        return board_id

    if board_name:
        # Search for board by name among the user's boards.
        url = "https://api.trello.com/1/members/me/boards"
        params = {
            'key': api_key,
            'token': token,
            'fields': 'name'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        boards = response.json()
        for board in boards:
            if board['name'] == board_name:
                print(f"Found board '{board_name}' with id {board['id']}.")
                return board['id']
        # If not found, create a new board without default lists.
        print(f"Board '{board_name}' not found. Creating new board...")
        create_url = "https://api.trello.com/1/boards"
        create_params = {
            'name': board_name,
            'defaultLists': 'false',
            'key': api_key,
            'token': token
        }
        create_response = requests.post(create_url, params=create_params)
        create_response.raise_for_status()
        new_board = create_response.json()
        print(f"Created board '{board_name}' with id {new_board['id']}.")
        return new_board['id']

    raise ValueError("Either board_id or board_name must be provided.")

def get_or_create_list(api_key, token, board_id, list_name):
    """
    Retrieve a list by name from a board. If it doesn't exist, create it.
    
    Parameters:
        api_key (str): Your Trello API key.
        token (str): Your Trello token.
        board_id (str): The ID of the Trello board.
        list_name (str): The name of the list to search for or create.
    
    Returns:
        str: The ID of the found or newly created list.
    """
    # URL to get all lists on the board.
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {
        'key': api_key,
        'token': token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    lists = response.json()
    
    # Look for the list by name (case-sensitive)
    for lst in lists:
        if lst['name'] == list_name:
            print(f"Found list '{list_name}'.")
            return lst['id']
    
    # If not found, create the list.
    print(f"List '{list_name}' not found. Creating new list...")
    create_url = "https://api.trello.com/1/lists"
    create_params = {
        'name': list_name,
        'idBoard': board_id,
        'key': api_key,
        'token': token
    }
    create_response = requests.post(create_url, params=create_params)
    create_response.raise_for_status()
    new_list = create_response.json()
    print(f"Created list '{list_name}' with id {new_list['id']}.")
    return new_list['id']

def create_trello_ticket_with_priority(api_key, token, board_id, list_name, card_name, priority, card_desc=None):
    """
    Create a Trello card in the specified list. The card's name will include the given priority.
    
    Parameters:
        api_key (str): Your Trello API key.
        token (str): Your Trello token.
        board_id (str): The ID of the Trello board.
        list_name (str): The name of the list to add the card to.
        card_name (str): The base name for the card.
        priority (str): The priority level (e.g., "High", "Medium", "Low").
        card_desc (str, optional): A description for the card.
    
    Returns:
        dict: The JSON response from the Trello API with details about the created card.
    """
    # Get or create the list on the board.
    list_id = get_or_create_list(api_key, token, board_id, list_name)
    
    # Prepend the priority to the card name.
    card_name_with_priority = f"[{priority}] {card_name}"
    
    # URL to create a new card.
    create_card_url = "https://api.trello.com/1/cards"
    card_params = {
        'key': api_key,
        'token': token,
        'idList': list_id,
        'name': card_name_with_priority
    }
    if card_desc:
        card_params['desc'] = card_desc

    response = requests.post(create_card_url, params=card_params)
    response.raise_for_status()
    
    card_info = response.json()
    print(f"Created card '{card_name_with_priority}' in list '{list_name}'.")
    return card_info

def add_trello_card(CARD_NAME, PRIORITY, CARD_DESC):
    # Get or create the board using either provided board id or board name.
    board_id = get_or_create_board(API_KEY, TOKEN, board_id=BOARD_ID, board_name=BOARD_NAME)
    try:
        new_card = create_trello_ticket_with_priority(API_KEY, TOKEN, board_id, LIST_NAME, CARD_NAME, PRIORITY, CARD_DESC)
        return {"success": True, "card": new_card}
    except requests.exceptions.HTTPError as err:
        return {"success": False, "error": str(err)}

# Example usage
add_trello_card("Test Card", "High", "This is a test card created from Python.")