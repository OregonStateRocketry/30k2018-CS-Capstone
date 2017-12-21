var mysql = require('mysql');
var getJSON = require('get-json')
var express = require('express')
const app = express()

var db = mysql.createConnection({
    host: "localhost",
    user: "levi",
    password: "esra18",
    database: "esra"
});

db.connect(function(err) {
  if (err) throw err
  console.log('Connected to the database...')
})

app.get('/', function (req, res) {
  res.send('Page that will display flight data from the ESRA 30k Rocket')
})

app.get('/beeline', function(req, res){
    console.log('Beeline!');
    db.query(
        "SELECT * FROM BeelineGPS LIMIT 3",
        function(err, results) {
            res.send(results);
        });
});

app.listen(3000, () => console.log('Demo listening on port 3000!'))
