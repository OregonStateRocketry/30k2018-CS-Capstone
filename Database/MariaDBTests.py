import unittest
from Mariadb import Mariadb

class TestMariaDB(unittest.TestCase):

    def test_Mariadb(self):
        with self.assertRaises(EnvironmentError):
            Mariadb('missingFile.yml')

        with self.assertRaises(EnvironmentError):
            Mariadb('config.yml.example')

        db = Mariadb('configTest.yml')

        print('Dropping database tables... ',
            "OK" if db.importSQLFile('drop_db.sql')==0 else "FAIL")

        print('Creating database tables... ',
            "OK" if db.importSQLFile('create_db.sql')==0 else "FAIL")

        # Should start with an empty DB but tables created
        self.assertIsNone( db.checkActiveFlight() )
        self.assertIsNone( db.getMaxFlightID() )
        self.assertEqual( db.getFlightTable(), () )
        self.assertEqual( db.getCurrentPosition(), () )
        self.assertIsNotNone( db.getDBTime() )
        self.assertIsNotNone( db.getParserTable() )

        self.assertEqual( db.addNewFlight(), 1 )
        self.assertEqual( db.checkActiveFlight(), 1 )

        self.assertEqual( db.getCurrentPosition(), () )
        self.assertEqual( db.validateCallsign("eagle"), 1 )
        self.assertEqual( db.validateCallsign("eagle"), 1 )
        self.assertEqual( db.insertRow(
                         table = "Callsigns",
                         cols  = "callsign",
                         vals  = ["'falcon'"]
                     ), 2)
        self.assertEqual( db.validateCallsign("falcon"), {'id': 2} )

        self.assertEqual( db.registerParser("TEST"), 1 )
        self.assertIsNotNone( db.getParserTable() )

        self.assertEqual( db.addNewFlight(), 2 )
        self.assertEqual( db.updateParserTable(2, "MOON", "CHEESE"), 0 )
        self.assertEqual( db.updateParserTable(2, "TEST", "CHEESE"), 0 )


if __name__ == '__main__':
    unittest.main()
