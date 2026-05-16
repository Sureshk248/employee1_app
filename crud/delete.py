import sqlite3


def delete_employee(pernr):
    try:
        conn = sqlite3.connect("employee.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM employee WHERE pernr=?
        """,
            (pernr,),
        )

        conn.commit()

        return {"status": "S", "message": "Employee deleted successfully"}

    except Exception as e:
        return {"status": "E", "error": str(e)}

    finally:
        conn.close()
