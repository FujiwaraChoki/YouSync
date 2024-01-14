import sqlite3

def clear_db():
    conn = sqlite3.connect("../yousync.db")
    c = conn.cursor()

    c.execute("DELETE FROM files")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    clear_db()
