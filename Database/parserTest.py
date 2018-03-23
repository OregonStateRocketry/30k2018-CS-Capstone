import unittest
from Mariadb import Mariadb
from parser import Parser
import os

class TestParser(unittest.TestCase):
    """Tests for `Database/parser.py`"""

    def test_all(self):
        db = Mariadb('configTest.yml')

        print('Dropping database tables... ',
        "OK" if db.importSQLFile('drop_db.sql')==0 else "FAIL")

        print('Creating database tables... ',
        "OK" if db.importSQLFile('create_db.sql')==0 else "FAIL")

        try:
            os.remove('logTest.csv')
        except FileNotFoundError as e:
            pass

        parser = Parser(dbConfig='configTest.yml', log='logTest.csv')

        # self.assertIsNotNone( parser.displayImportMenu([1]) )
        with self.assertRaises(SystemExit):
            parser.importFile('missingFile.csv')

        self.assertIsNone( parser.insertRocketAvionics(None) )
        self.assertIsNone( parser.insertPayloadAvionics(None) )
        self.assertIsNone( parser.insertOther(None) )

        self.assertEqual( 1, parser.insertBeelineGPS(
                {'callsign': 'AG7IU-1', 'audio level': 195, 'lat': 45.5528, \
                'lon': 122.7777, 'alt': 1118, 'alt units': 'ft', 'f_id': 1, \
                'serialNum': '0000'})
            )

        self.assertTrue( parser.listen(0) )

        self.assertIsNone( parser.importFile('logTest.csv') )
        with open('logTest.csv', 'a+') as f:
            f.write('2018-03-23 08:36:14.763732,AG7IU-1,'+
                    '195,45.5528,122.7777,1118,ft,1,0000\n'
                    )
        self.assertIsNone( parser.importFile('logTest.csv') )

        self.assertTrue( parser.listen(1) )

        with self.assertRaises(SystemExit):
            with open('logTest.csv', 'a+') as f:
                f.write('bad data')
            parser.importFile('logTest.csv')

if __name__ == '__main__':
    unittest.main()
