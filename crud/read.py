import sqlite3


def read_employee(pernr):
    try:
        conn = sqlite3.connect("employee.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM employee WHERE pernr=?
        """,
            (pernr,),
        )

        employee = cursor.fetchone()

        if employee:
            return {
                "status": "S",
                "employee": {
                    "pernr": employee[0],
                    "name": employee[1],
                    "desig": employee[2],
                    "dob": employee[3],
                    "attachment": employee[4],
                },
            }
        else:
            return {"status": "E", "message": "Employee not found"}

    except Exception as e:
        return {"status": "E", "error": str(e)}

    finally:
        conn.close()
