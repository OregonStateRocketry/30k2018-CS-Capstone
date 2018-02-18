import pymysql.cursors
import datetime
import yaml

SQL_BUFFER_MAX = 500

class Mariadb:
    ''' Interact with the ESRA avionics database '''

    def __init__(self):
        with open('config.yml', 'r') as cf:
            cf = yaml.load(cf)
        self.connection = pymysql.connect(
            host        =   cf['database']['host'],
            user        =   cf['database']['username'],
            password    =   cf['database']['password'],
            db          =   cf['database']['database'],
            charset     =   'utf8mb4',
            cursorclass =   pymysql.cursors.DictCursor,
            autocommit  =   True
        )
        self.db = self.connection.cursor()
        self.numInserts = 0
        self.sql_buffer = []
        self.sql_buffer_keys = None


    def __del__(self):
        self.db.executemany(self.sql_buffer_keys, self.sql_buffer)
        self.connection.close()


    def insertRow(self, data):
        ''' Inserts a single row into the Payload_Avionics '''
        sql = """
            INSERT INTO Avionics ({keys}) VALUES {vals}
            """.format(
                keys = ",".join(data.keys()),
                vals = tuple(data.values())
            )
        # self.numInserts += 1
        return self.db.execute(sql)


    def insertMany(self, m1, m2, m3):

        # if not self.sql_buffer_keys:
            # self.sql_buffer_keys = data.keys()
        a = tuple(m1.values())
        b = tuple(m2.values())
        c = tuple(m3.values())
        self.sql_buffer.append( a+b+c )

        if len(self.sql_buffer) >= SQL_BUFFER_MAX:
            self.executeMany(self.sql_buffer_keys, self.sql_buffer)

    def executeMany(self, k, v):

        # keys = ",".join(k)
        # Need to fix keys!
        keys = '''
            acc1_x,
            acc1_y,
            acc1_z,
            gyro1_x,
            gyro1_y,
            gyro1_z,
            acc2_x,
            acc2_y,
            acc2_z,
            gyro2_x,
            gyro2_y,
            gyro2_z,
            acc3_x,
            acc3_y,
            acc3_z,
            gyro3_x,
            gyro3_y,
            gyro3_z
        '''
        # vals = "%s,"*len(k)
        # vals = vals[:-1]
        vals = "%s,"*6*3
        vals = vals[:-1]

        sql = """
            INSERT INTO Avionics ({}) VALUES ({})
            """.format(
                keys,
                vals
            )
        # print('keys=', keys)
        # print('v=', v)
        # print('sql=', sql)
        self.sql_buffer = []
        self.sql_buffer_keys = None
        return self.db.executemany(sql, v)

    # def insertRow(self, data):
    #     ''' Inserts a single row into the Payload_Avionics '''
    #     with self.connection.cursor() as c:
    #         sql = """
    #             INSERT INTO Avionics ({keys}) VALUES {vals}
    #             """.format(
    #                 keys = ",".join(data.keys()),
    #                 vals = tuple(data.values())
    #             )
    #         return c.execute(sql)
