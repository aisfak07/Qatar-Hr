import frappe


def after_install():
    # create_employee_custom_fields()
    create_salary_structure_custom_fields()
    create_salary_structure_assignment_custom_fields()
    create_leave_encashment_custom_fields()
    create_leave_application_custom_fields()
    create_salary_slip_custom_fields()


def create_salary_slip_custom_fields():
    fields = [
        {
            "fieldname": "qhr_attendance_summary_section",
            "label": "Qatar HR Attendance Summary",
            "fieldtype": "Section Break",
            "insert_after": "payment_days",
            "collapsible": 1,
            "depends_on": "eval:(doc.qhr_present_days || 0) > 0 || (doc.qhr_paid_leave_days || 0) > 0 || (doc.qhr_leave_without_pay_days || 0) > 0",
        },
        {
            "fieldname": "qhr_present_days",
            "label": "Present Days",
            "fieldtype": "Float",
            "precision": "2",
            "insert_after": "qhr_attendance_summary_section",
            "read_only": 1,
            "depends_on": "eval:(doc.qhr_present_days || 0) > 0",
        },
        {
            "fieldname": "qhr_paid_leave_days",
            "label": "Paid Leave Days",
            "fieldtype": "Float",
            "precision": "2",
            "insert_after": "qhr_present_days",
            "read_only": 1,
            "depends_on": "eval:(doc.qhr_paid_leave_days || 0) > 0",
        },
        {
            "fieldname": "qhr_leave_without_pay_days",
            "label": "Leave Without Pay Days",
            "fieldtype": "Float",
            "precision": "2",
            "insert_after": "qhr_paid_leave_days",
            "read_only": 1,
            "depends_on": "eval:(doc.qhr_leave_without_pay_days || 0) > 0",
        },
    ]

    for field in fields:
        custom_field_name = f"Salary Slip-{field['fieldname']}"

        if frappe.db.exists("Custom Field", custom_field_name):
            custom_field = frappe.get_doc("Custom Field", custom_field_name)

            for key, value in field.items():
                custom_field.set(key, value)

            custom_field.save(ignore_permissions=True)

        else:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Salary Slip",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()
    

def create_leave_application_custom_fields():
    fields = [
        {
            "fieldname": "forecasted_leave",
            "label": "Forecasted Leave",
            "fieldtype": "Float",
            "insert_after": "leave_type",
            "read_only": 1,
            "depends_on": "eval:doc.leave_type == 'Annual Leave' && doc.from_date"
        }
    ]

    for field in fields:
        custom_field_name = f"Leave Application-{field['fieldname']}"

        if frappe.db.exists("Custom Field", custom_field_name):
            custom_field = frappe.get_doc("Custom Field", custom_field_name)
            for key, value in field.items():
                custom_field.set(key, value)
            custom_field.save(ignore_permissions=True)
        else:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Leave Application",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()


# Leave Encashment Custom Fields: These fields will be added to the `Leave Encashment` doctype to accommodate work ledger requirements. They will be used to store forecasted encashable days, track if the employee is leaving the company, and store the relieving date for accurate leave encashment calculations and reporting in the work ledger.
def create_leave_encashment_custom_fields():
    fields = [
        {
            "fieldname": "forecasted_encashable_days",
            "label": "Forecasted Encashable Days",
            "fieldtype": "Float",
            "insert_after": "actual_encashable_days",
        },
        {
            "fieldname": "employee_separation_section",
            "label": "Employee Separation",
            "fieldtype": "Section Break",
            "insert_after": "encashment_amount",
        },
        {
            "fieldname": "employee_leaving_company",
            "label": "Employee Leaving Company",
            "fieldtype": "Check",
            "insert_after": "employee_separation_section",
        },
        {
            "fieldname": "relieving_date",
            "label": "Relieving Date",
            "fieldtype": "Date",
            "insert_after": "employee_leaving_company",
            "depends_on": "eval:doc.employee_leaving_company == 1",
            "read_only": 1,
        },
    ]

    for field in fields:
        custom_field_name = f"Leave Encashment-{field['fieldname']}"

        if frappe.db.exists("Custom Field", custom_field_name):
            custom_field = frappe.get_doc("Custom Field", custom_field_name)
            for key, value in field.items():
                custom_field.set(key, value)
            custom_field.save(ignore_permissions=True)
        else:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Leave Encashment",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()


# Salary Structure Assignment` doctype custom fields to accommodate work ledger requirements. These fields will be used to store various allowances for accurate salary calculations and reporting in the work ledger.
def create_salary_structure_assignment_custom_fields():
    fields = [
        {
            "fieldname": "housing_allowance",
            "label": "Housing Allowance",
            "fieldtype": "Currency",
            "insert_after": "base",
        },
        {
            "fieldname": "transportation_allowance",
            "label": "Transportation Allowance",
            "fieldtype": "Currency",
            "insert_after": "housing_allowance",
        },
        {
            "fieldname": "food_allowance",
            "label": "Food Allowance",
            "fieldtype": "Currency",
            "insert_after": "transportation_allowance",
        },
        {
            "fieldname": "mobile_allowance",
            "label": "Mobile Allowance",
            "fieldtype": "Currency",
            "insert_after": "food_allowance",
        },
        {
            "fieldname": "other_allowance",
            "label": "Other Allowance",
            "fieldtype": "Currency",
            "insert_after": "mobile_allowance",
        },
        {
            "fieldname": "total_salary",
            "label": "Total Salary",
            "fieldtype": "Currency",
            "insert_after": "leave_encashment_amount_per_day",
        },
    ]

    for field in fields:
        custom_field_name = f"Salary Structure Assignment-{field['fieldname']}"

        if frappe.db.exists("Custom Field", custom_field_name):
            custom_field = frappe.get_doc("Custom Field", custom_field_name)
            for key, value in field.items():
                custom_field.set(key, value)
            custom_field.save(ignore_permissions=True)
        else:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Salary Structure Assignment",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()

# Custom fields for Salary Structure doctype to accommodate work ledger requirements. These fields will be used to store the leave salary formula for accurate leave encashment calculations.
def create_salary_structure_custom_fields():
    fields = [
        {
            "fieldname": "leave_salary_formula",
            "label": "Leave Salary Formula",
            "fieldtype": "Code",
            "options" : "PythonExpression",
            "allow_on_submit" : 1,
            "insert_after": "leave_encashment_amount_per_day",
        }
    ]

    for field in fields:
        custom_field_name = f"Salary Structure-{field['fieldname']}"

        if frappe.db.exists("Custom Field", custom_field_name):
            custom_field = frappe.get_doc("Custom Field", custom_field_name)
            for key, value in field.items():
                custom_field.set(key, value)
            custom_field.save(ignore_permissions=True)
        else:
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Salary Structure",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()


# Custom fields for Employee doctype to accommodate work ledger requirements. These fields will be used to link salary structure assignment, track overtime eligibility and assigned shifts, and store additional personal details such
def create_employee_custom_fields():
    fields = [
        # Salary Tab
        {
            "fieldname": "salary_structure_assigned",
            "label": "Salary Structure Assigned",
            "fieldtype": "Link",
            "options": "Salary Structure Assignment",
            "insert_after": "payroll_cost_center",
        },

        # Attendance / Shift area
        {
            "fieldname": "overtime_eligible",
            "label": "Overtime Eligible?",
            "fieldtype": "Check",
            "insert_after": "attendance_device_id",
        },
        {
            "fieldname": "assigned_shift",
            "label": "Assigned Shift",
            "fieldtype": "Link",
            "options": "Shift Type",
            "insert_after": "overtime_eligible",
        },

        # Personal Details
        {
            "fieldname": "nationality",
            "label": "Nationality",
            "fieldtype": "Link",
            "options": "Country",
            "insert_after": "person_to_be_contacted",
        },
        {
            "fieldname": "signature",
            "label": "Signature",
            "fieldtype": "Attach Image",
            "insert_after": "nationality",
        },
        {
            "fieldname": "religion",
            "label": "Religion",
            "fieldtype": "Select",
            "options": "\nIslam\nChristianity\nHinduism\nBuddhism\nOther",
            "insert_after": "signature",
        },

        # QID Section after Passport Details Section
        {
            "fieldname": "qid_section",
            "label": "QID Section",
            "fieldtype": "Section Break",
            "insert_after": "place_of_issue",
        },
        {
            "fieldname": "qid",
            "label": "QID",
            "fieldtype": "Data",
            "insert_after": "qid_section",
        },
        {
            "fieldname": "qid_expiry_date",
            "label": "QID Expiry Date",
            "fieldtype": "Date",
            "insert_after": "qid",
        },

        # Visa Section after QID Section
        {
            "fieldname": "visa_details_section",
            "label": "Visa Details Section",
            "fieldtype": "Section Break",
            "insert_after": "qid_expiry_date",
        },
        {
            "fieldname": "visa_no",
            "label": "Visa No",
            "fieldtype": "Data",
            "insert_after": "visa_details_section",
        },
        {
            "fieldname": "visa_expiry_date",
            "label": "Visa Expiry Date",
            "fieldtype": "Date",
            "insert_after": "visa_no",
        },
    ]

    for field in fields:
        custom_field_name = f"Employee-{field['fieldname']}"

        if not frappe.db.exists("Custom Field", custom_field_name):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Employee",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()
    