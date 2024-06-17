import os
import pymysql
import dotenv

dotenv.load_dotenv()

connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
)

with connection:
    with connection.cursor() as cursor:
        #SQL
        print(cursor)
#Sempre q abre uma conexão ou um cursor, tem q fechar dps
#cursor = conection.cursor()
#cursor.close()
#connection.close()