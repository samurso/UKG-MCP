from ukg_mcp.employees import get_employee_names

if __name__ == "__main__":
    try:
        employees = get_employee_names()

        print("✅ Employee List Retrieved Successfully\n")

        for emp in employees:
            print(emp)

    except Exception as e:
        print("❌ Error:", e)
