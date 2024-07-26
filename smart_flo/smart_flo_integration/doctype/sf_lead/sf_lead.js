// Copyright (c) 2024, Yash Wadgaonkar and contributors
// For license information, please see license.txt

frappe.ui.form.on("SF Lead", {
    refresh(frm) {
        frm.add_custom_button(__("Call Lead"), function() {
            // Fetch the phone number from the field
            let phone_number = frm.doc.phone_number;

            // Prepare the API request body
            let bodyData = {
                agent_number: "0605056260003",
                destination_number: phone_number,
                caller_id: "+918062413302",
                async: 0
            };

            // Prepare the headers
            let headers = {
                'Content-Type': 'application/json',
                'Authorization': `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1MDU2MjYiLCJpc3MiOiJodHRwczovL2Nsb3VkcGhvbmUudGF0YXRlbGVzZXJ2aWNlcy5jb20vdG9rZW4vZ2VuZXJhdGUiLCJpYXQiOjE3MjE4MDQwNjUsImV4cCI6MjAyMTgwNDA2NSwibmJmIjoxNzIxODA0MDY1LCJqdGkiOiJlZ2IxM0N2b3RvT2REUU5xIn0.LQ19oFKQL2do9DeukGha91yK6vvR18_KtngGLxBs19g` // Replace with your actual authorization key
            };

            // Make the POST request
            fetch('https://api-smartflo.tatateleservices.com/v1/click_to_call', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(bodyData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                frappe.msgprint(__('Call initiated successfully: ' + JSON.stringify(data)));
            })
            .catch(error => {
                console.error('Error:', error);
                frappe.msgprint(__('Error initiating call: ' + error.message));
            });
        });
    }
});
