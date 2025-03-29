import requests

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

def create_trello_ticket_with_priority(api_key: str, token: str, board_id: str, list_name: str, card_name: str, priority: str, description: str = ""):
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
    try:
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
        if description:
            card_params['desc'] = description

        response = requests.post(create_card_url, params=card_params)
        response.raise_for_status()
        return {"success": True, "card": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def add_trello_card(api_key: str, token: str, list_name: str, priority: str, card_name: str, card_desc: str,  board_id: str = None, board_name: str = None):
    # Get or create the board using either provided board id or board name.

    if not board_id and not board_name:
        return {"success": False, "error": "Either board_id or board_name must be provided" }

    board_id = get_or_create_board(api_key, token, board_id=board_id, board_name=board_name)
    try:
        new_card = create_trello_ticket_with_priority(api_key, token, board_id, list_name, card_name, priority, card_desc)
        return {"success": True, "card": new_card}
    except requests.exceptions.HTTPError as err:
        return {"success": False, "error": str(err)}