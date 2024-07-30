import frappe
import requests

@frappe.whitelist()
def get_agent_info(phone_number):
    # Fetch the current logged-in user's username
    user_name = frappe.session.user
    
    # Retrieve agent information based on the user
    agent_info = frappe.get_all('Tata SmartFlo Agent', filters={'user_name': user_name}, fields=['login_id', 'caller_id'], limit=1)
    
    if not agent_info:
        return {'message': 'No agent information found for the current user.'}
    
    agent_info = agent_info[0]
    login_id = agent_info.get('login_id')
    caller_id = agent_info.get('caller_id')

    if not login_id or not caller_id:
        return {'message': 'Incomplete agent information.'}

    # Fetch the authorization token from the Tata SmartFlo Settings doctype
    settings = frappe.get_single('Tata SmartFlo Settings')
    
    authorization_token = settings.get_password('authorization_token')

    # Define the API URL and payload
    url = "https://api-smartflo.tatateleservices.com/v1/click_to_call"
    payload = {
        "agent_number": login_id,
        "destination_number": phone_number,
        "caller_id": caller_id,
        "async": 1,
        "get_call_id": 1
    }
    
    # Define headers including Authorization token
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {authorization_token}"  # Use the authorization_token in the header
    }

    # Make the POST request
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        result = response.json()
        
        if 'call_id' not in result:
            return {'message': 'Call ID not returned from the API.'}
        
        call_id = result['call_id']
        
        # Log the call ID and response
        print(f"Call ID: {call_id}")
        print(f"Response from click_to_call API: {result}")

        # Fetch live call details using the call ID
        live_call_url = "https://api-smartflo.tatateleservices.com/v1/live_calls"
        live_call_response = requests.get(f"{live_call_url}?call_id={call_id}", headers=headers)
        live_call_response.raise_for_status()
        call_details = live_call_response.json()
        
        # Log the response from live_calls API
        print(f"Response from live_calls API: {call_details}")
        
        return result  # Return the JSON response from the click_to_call API

    except requests.exceptions.RequestException as e:
        frappe.throw(f"API request failed: {str(e)}")