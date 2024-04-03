from sql import establish_connection

def create_tables():
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            create_table_users = """
                CREATE TABLE IF NOT EXISTS user (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(45) NOT NULL,
                    nickname VARCHAR(45),
                    discordid VARCHAR(45) NOT NULL,
                    serverid VARCHAR(45) NOT NULL,
                    warn INT DEFAULT 0
                )
            """
            try:
                cursor.execute(create_table_users)
                print("[LOG] Tables was seccsessfuly created")
            except Exception as e:
                print("[ERROR]:", e)

if __name__ == "__main__":
    create_tables()