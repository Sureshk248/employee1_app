import sqlite3


def update_employee(pernr, name, desig, dob, attachment):
    try:

        conn = sqlite3.connect("employee.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE employee SET name=?, desig=?, dob=?, attachment=? WHERE pernr=?
        """,
            (name, desig, dob, attachment, pernr),
        )

        conn.commit()

        return {"status": "S", "message": "Employee updated successfully"}

    except Exception as e:
        return {"status": "E", "error": str(e)}

    finally:
        conn.close()
