import frappe


def after_install():
    """Run ERPNext helper to create Address and Contact custom fields on app install.
    This ensures fields like `is_billing_contact` are present in the site DB.
    """
    try:
        # Import helper from ERPNext (exists when ERPNext app is installed)
        from erpnext.setup.install import create_address_and_contact_custom_fields

        create_address_and_contact_custom_fields()
        frappe.db.commit()
    except Exception as e:
        # Log error but don't fail installation import
        try:
            frappe.log_error(title="after_install failed for zatca_erpgulf", message=str(e))
        except Exception:
            pass
