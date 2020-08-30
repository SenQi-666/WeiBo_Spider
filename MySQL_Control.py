import pymysql


class MySQLClient:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost', port=3306, user='root', password='19981010', db='weibo_comments', charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def insert(self, usrid, usr, gender, date, time, content):
        try:
            sql = 'INSERT INTO comments(usrid, usrname, usrgender, comment_date, comment_time, content) VALUES(%s, %s, %s, %s, %s, %s)'
            param = (usrid, usr, gender, date, time, content)
            self.cursor.execute(sql, param)
            self.conn.commit()
            print(usrid, usr, gender, date, time, content)
        except Exception as e:
            print(e)
            self.conn.rollback()

    def show(self):
        comments_lst = []
        sql = 'SELECT content FROM comments'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for row in data:
            comments_lst.append(row[0])
        return comments_lst


if __name__ == '__main__':
    MySQLClient().show()


