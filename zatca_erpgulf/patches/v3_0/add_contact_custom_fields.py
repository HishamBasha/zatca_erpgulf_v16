import frappe


def execute():
    """Ensure Address and Contact custom fields are present.

    This patch runs during `bench migrate` (post_model_sync) so the site DB
    always has fields like `Contact.is_billing_contact` which ERPNext expects.
    """
    try:
        # Skip if already present
        if frappe.db.exists("Custom Field", "Contact-is_billing_contact"):
            return

        # Import ERPNext helper to create address/contact custom fields
        from erpnext.setup.install import create_address_and_contact_custom_fields

        create_address_and_contact_custom_fields()
        frappe.db.commit()
    except ModuleNotFoundError:
        # ERPNext not installed on this site; nothing to do
        return
    except Exception as e:
        # Log and continue; patch should not break migrate
        try:
            frappe.log_error(title="add_contact_custom_fields patch failed", message=str(e))
        except Exception:
            pass
