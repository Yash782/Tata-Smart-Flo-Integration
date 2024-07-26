import frappe

@frappe.whitelist()
def get_agent_info(phone_number):
    print("Method called")
    user_email = frappe.session.user
    agent_info = frappe.get_all('Tata Flo Agent', filters={'user_email': user_email}, fields=['login_id', 'caller_id'], limit=1)