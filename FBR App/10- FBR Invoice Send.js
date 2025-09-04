// DocType = Sales Invoice
// Apply to : Form
// Client Script



frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm) {
        // only show for submitted invoices and not already sent
        if (frm.doc.docstatus === 1 && !frm.doc.custom_fbr_invoice_no) {
            frm.add_custom_button(__('Send to FBR'), function() {
                frappe.call({
                    method: "fbr_integration.handler.send_to_fbr_si",
                    args: { name: frm.doc.name },
                    freeze: true,
                    callback: function(r) {
                        if (r.exc) {
                            frappe.msgprint(__('Error sending to FBR: {0}', [r.exc]));
                        } else if (r.message) {
                            frappe.msgprint(__('FBR response: {0}', [JSON.stringify(r.message)]));
                            frm.reload_doc();
                        }
                    }
                });
            }, __('FBR'));
        }
    }
});


------------------------------

-------------------------------------------------------------------------------------

frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm) {
        // Only show button for submitted invoices and not already sent
        if (frm.doc.docstatus === 1 && !frm.doc.custom_fbr_invoice_no) {
            frm.add_custom_button(
                __("Send to FBR"),
                function() {
                    frappe.call({
                        method: "fbr_integration.handler.send_to_fbr_si",
                        args: {
                            name: frm.doc.name,
                        },
                        freeze: true,
                        callback: function(r) {
                            if (r.exc) {
                                frappe.msgprint(
                                    __("Error sending to FBR: {0}", [r.exc])
                                );
                            } else if (r.message) {
                                frappe.msgprint(
                                    __("FBR response: {0}", [
                                        JSON.stringify(r.message),
                                    ])
                                );
                                frm.reload_doc();
                            }
                        },
                    });
                },
                __("FBR")
            );
        }
    },
});
