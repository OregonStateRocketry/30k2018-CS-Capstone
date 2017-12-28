var mysql = require('mysql');
var getJSON = require('get-json')
var express = require('express')
var config = require('./config')
var exphbs = require('express-handlebars');
const app = express();

var db = mysql.createConnection(config.database);

db.connect(function(err) {
  if (err) throw err
  console.log('Connected to the database...')
});
app.use(express.static('public'));

app.get('/', function (req, res) {
  res.send('Page that will display flight data from the ESRA 30k Rocket')
});

app.get('/q', function(req, res){
    var get = req.query.get;
    var f_id = req.query.f_id;
    var limit = (req.query.limit) ? ' LIMIT '+req.query.limit : '';
    var time = (req.query.time) ? " AND time >= '"+req.query.time+"'" : '';
    var sql = null;

    switch(get){
        case 'altVTimeSources':
            // Returns a list of the unique callsigns for a flight id
            sql = `SELECT DISTINCT
                   callsign FROM BeelineGPS WHERE f_id=${f_id}`+time+`
                   UNION
                   SELECT 'Rocket'
                   FROM Rocket_Avionics WHERE f_id=${f_id}`+time+`
                   UNION
                   SELECT 'Payload'
                   FROM Payload_Avionics WHERE f_id=${f_id}`+time+`
                   ORDER BY source DESC`+limit;
            break;
        case 'altVtime':
            // Plots altitude vs time
            console.log('Hit altVtime');
            sql = `SELECT callsign AS Source, time, alt
                   FROM BeelineGPS WHERE f_id=${f_id}`+time+`
                   UNION
                   SELECT 'Rocket', time, alt
                   FROM Rocket_Avionics WHERE f_id=${f_id}`+time+`
                   UNION
                   SELECT 'Payload', time, alt
                   FROM Payload_Avionics WHERE f_id=${f_id}`+time+`
                   ORDER BY time ASC`+limit;
            break;
        case 'receptionVtime':
            // Plots reception vs time
            console.log('Hit receptionVtime');
            sql = `SELECT time
                   FROM BeelineGPS WHERE f_id=${f_id}`+time+`
                   ORDER BY time ASC`+limit;
           break;
        case 'map':
            // Plots location v time as 2d or 3d map
            console.log('Hit map');
            sql = `SELECT callsign as Source, time, lat, lon, alt
                   FROM BeelineGPS WHERE f_id=${f_id}`+time+`
                   ORDER BY time ASC`+limit;
            break;
        default:
            // Invalid or missing get field
            console.log('DEFAULT.  get='+get);
    }

    if(sql){
        // console.log('SQL = '+sql)
        db.query(sql,function(err, results) {
            // console.log('Results: '+results);
            res.send(JSON.stringify(results));
        });
    } else {
        console.log('No SQL');
        res.end('No SQL');
    }
});

app.get('/beeline', function(req, res){
    console.log('Beeline!');
    db.query(
        "SELECT * FROM BeelineGPS LIMIT 3",
        function(err, results) {
            res.send(results);
        });
});

// Usage: esra.local:3000/q?get=altVtime&f_id=1&
app.listen(
    config.server.port,
    () => console.log('ESRA server listening on port '+config.server.port)
);
