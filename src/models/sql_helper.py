import pymysql
import os


class sql_helper:
    def __init__(self):
        self.connection_obj = None

    def connect_database(self):
        try:
            self.connection_obj = pymysql.connect(
                host='simpli.cpwywyg5fzzw.us-east-1.rds.amazonaws.com',
                port=3306,
                user='admin',
                password='1q2w3e4r5t',
                db="simpli",
                autocommit=True
            )
        except:
            pass
            # Need to import error handling class

    def disconnect_database(self):
        try:
            self.connection_obj.close()
        except:
            pass
            # Need to import error handling class

    def run_query(self, query):
        self.connect_database()
        tempCursor = self.connection_obj.cursor()
        tempCursor.execute(query)
        output = tempCursor.fetchall()
        self.disconnect_database()
        return output


if __name__ == '__main__':
    sql = sql_helper()
    output = sql.run_query("show tables")
    print("this is printed!", output)
    print("Hello")
