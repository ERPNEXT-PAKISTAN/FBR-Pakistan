// DocType = Sales Invoice
// Apply to : Form
// Client Script
//------------------------------------



frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm) {
        // show only for submitted invoices (docstatus = 1)
        if (frm.doc.docstatus !== 1) {
            return;
        }

        // add button (Frappe clears previous buttons on refresh, so safe to call each time)
        let btn = frm.add_custom_button(__("Send to FBR"), function() {
            if (frm.doc.custom_fbr_invoice_no) {
                // Already sent -> show the informational dialog
                frappe.msgprint({
                    title: __("Already Submitted"),
                    indicator: "red",
                    message: `
                        <div style="font-size:14px; line-height:1.6;">
                            <p>🚫 <b>Invoice already sent to Iris-FBR Portal</b></p>
                            <p>Please watch your FBR Invoice No.: <b>${frm.doc.custom_fbr_invoice_no}</b></p>
                            <p style="color:green;">
                                For further clarity please contact Fibersoft ERP Pakistan at 03003360042
                            </p>
                        </div>
                    `
                });
                return;
            }

            // Not sent yet -> call server method
            frappe.call({
                method: "fbr_integration.handler.send_to_fbr_si",
                args: { name: frm.doc.name },
                freeze: true,
                callback: function(r) {
                    if (!r || !r.message) {
                        frappe.msgprint({ title: __("Error"), indicator: "red", message: __("No response from server") });
                        return;
                    }

                    var resp = r.message;
                    if (resp.success === false) {
                        // server reported error
                        frappe.msgprint({
                            title: __("FBR Error"),
                            indicator: "red",
                            message: `
                                <div style="font-size:14px; line-height:1.6;">
                                    <p>❌ <b>Error sending invoice to FBR</b></p>
                                    <pre>${resp.error}</pre>
                                </div>
                            `
                        });
                    } else {
                        // success
                        frappe.msgprint({
                            title: __("Invoice Sent"),
                            indicator: "green",
                            message: `
                                <div style="font-size:14px; line-height:1.6;">
                                    <p>🟢 <b>Invoice Sent</b></p>
                                    <p>🎉 <b>Congratulations!</b></p>
                                    <p>
                                        Your Sales Invoice <b>${frm.doc.name}</b> has been successfully submitted 
                                        to the <b>IRIS Portal – FBR</b>.
                                    </p>
                                    <p><b>FBR Invoice No:</b> ${resp.invoice_no}</p>
                                    <p style="color:green;">☑ Thank you for staying compliant and digital by Fibersoft ERP-Pakistan!</p>
                                </div>
                            `
                        });

                        // reload to fetch fields set by server (custom_fbr_invoice_no etc.)
                        frm.reload_doc();
                    }
                }
            });

        });

        // make button red
        btn.removeClass("btn-default").addClass("btn-danger");
    }
});
