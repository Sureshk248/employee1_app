import sqlite3


def create_employee(pernr, name, desig, dob, attachment):

    try:

        conn = sqlite3.connect("employee.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO employee(pernr,name,desig,dob,attachment) VALUES(?,?,?,?,?)
        """,
            (pernr, name, desig, dob, attachment),
        )

        conn.commit()

        return {"status": "S", "message": "Employee created successfully"}

    except Exception as e:
        return {"status": "E", "error": str(e)}

    finally:
        conn.close()
