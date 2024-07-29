import frappe
import requests

@frappe.whitelist()
def get_agent_info(phone_number):
    # Print for debugging purposes
    print("Method called")
    
    # Fetch the current logged-in user's username
    user_name = frappe.session.user
    
    # Retrieve agent information based on the user
    agent_info = frappe.get_all('Tata Flo Agent', filters={'user_name': user_name}, fields=['login_id', 'caller_id'], limit=1)
    
    if not agent_info:
        return {'message': 'No agent information found for the current user.'}
    
    agent_info = agent_info[0]
    login_id = agent_info.get('login_id')
    caller_id = agent_info.get('caller_id')

    if not login_id or not caller_id:
        return {'message': 'Incomplete agent information.'}

    # Fetch the authorization token from the Smartflow Setting doctype
    settings = frappe.get_single('Smartflow Setting')
    if not settings or not settings.authorization_token:
        return {'message': 'Authorization token is missing in Smartflow Setting.'}
    
    authorization_token = settings.authorization_token

    # Define the API URL and payload
    url = "https://api-smartflo.tatateleservices.com/v1/click_to_call"
    payload = {
        "agent_number": login_id,
        "destination_number": phone_number,
        "caller_id": caller_id,
        "async": 1
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
        return response.json()  # Return the JSON response from the API
    except requests.exceptions.RequestException as e:
        frappe.throw(f"API request failed: {str(e)}")
