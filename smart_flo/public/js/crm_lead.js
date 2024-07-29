frappe.ui.form.on("CRM Lead", {
    refresh(frm) { 
        frm.add_web_link(`/crm/leads/${frm.doc.name}`, __("Open in Portal")); 
        frm.add_custom_button(__('Call Lead'), function() {
            let phone_number = frm.doc.mobile_no;

            if (phone_number) {
                frappe.call({
                    method: 'smart_flo.api.fetch_agent.get_agent_info',
                    args: {
                        phone_number: phone_number
                    },
                    callback: function(response) {
                        const result = response.message;
                        if (result.message) {
                            frappe.msgprint({
                                message: result.message,
                            });
                        }
                    }
                });
            } else {
                frappe.msgprint(__('Phone number is missing.'));
            }
        });
    }
});
