import pymysql


def establish_connection():
    connection = pymysql.connect(
        host='',
        user='',
        password='',
        database='',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def add_user(name,nickname,discordid,serverid):
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `user` (name,nickname,discordid,serverid) VALUES (%s,%s,%s,%s)"
            cursor.execute(insert_query, (name,nickname,discordid,serverid))
            connection.commit()


def user_exist(discordid,serverid):
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            select_query = "SELECT * FROM user WHERE discordid = %s AND serverid = %s"
            cursor.execute(select_query, (discordid,serverid))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
            
def get_all_server_users(serverid):
    connection = establish_connection()
    with connection:
        with connection.cursor() as cursor:
            select_query = "SELECT * FROM user WHERE serverid = %s"
            cursor.execute(select_query, (serverid))
            result = cursor.fetchall()
            return result
        
