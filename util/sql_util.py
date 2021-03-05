import pymysql
class MysqlUtil():
    @staticmethod
    def get_conn():
        try:
            conn = pymysql.connect(host='114.67.80.160', user='tj', password='Summer_888', db='erp',
                                   charset='utf8')
            return conn, conn.cursor()
        except:
            return None

    @staticmethod
    def close(conn):
        try:
            conn.close()
        except:
            pass

if __name__ == '__main__':
    MysqlUtil()