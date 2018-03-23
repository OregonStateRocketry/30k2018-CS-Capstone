var mysql = require('mysql');
var express = require('express')
var config = require('./config.js')
var exphbs = require('express-handlebars');
const app = express();

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');


var db = mysql.createConnection(config.database);

db.connect(function(err) {
  if (err) throw err
  console.log('Connected to the database...')
});
app.use(express.static('public'));

app.get('/', function (req, res) {
-  res.render('index-page'); });

app.get('/summary', function (req, res) {
  // Display a summary of all recorded flights
  sql = `
      SELECT
          B.f_id, B.id, C.callsign, F.status,
          MIN_T.min_time, MIN_T.start_lat, MIN_T.start_lon,
          MAX_T.max_time, MAX_T.end_lat, MAX_T.end_lon,
          ALT.max_alt, ALT.min_alt
      FROM BeelineGPS B
      JOIN (SELECT id, status FROM Flights) F ON F.id = B.f_id
      JOIN (SELECT id, callsign from Callsigns) C ON C.id=B.c_id
      JOIN (
          SELECT f_id, c_id, lat AS end_lat, lon AS end_lon, time AS max_time
          FROM BeelineGPS WHERE time IN (
              SELECT DISTINCT MAX(time) FROM BeelineGPS GROUP BY f_id, c_id
              )
          ) MAX_T ON MAX_T.f_id = F.id
      JOIN (
          SELECT f_id, lat AS start_lat, lon AS start_lon, time AS min_time
          FROM BeelineGPS WHERE time IN (
              SELECT DISTINCT MIN(time) FROM BeelineGPS GROUP BY f_id, c_id
              )
          ) MIN_T ON MIN_T.f_id = MAX_T.f_id
      JOIN (
          SELECT id, MIN(alt) AS min_alt, MAX(alt) AS max_alt FROM BeelineGPS
          GROUP BY f_id, c_id
          ) ALT ON ALT.id = B.id
  `
  db.query(sql,function(err, results) {
      // console.log('Results: '+results['time']);
      //res.render('index-page', summary : result);
      res.send(JSON.stringify(results));

  });

});

//Renders graph pages with queries from index page
app.get('/graph', function (req, res){
    var get = req.query.get;
    var fid = req.query.fid;
    //Special case for multiple flight ids selected
    if (fid == "multi"){
        // Define array of flight IDs and form multi query
        var fid_mult = [];
        var num = req.query.num;
        switch(num){ //Switch should add all selected flights to an array
            default: //Currently supports up to four flights
                fid_mult.push(req.query.fid_3);
            case 3:
                fid_mult.push(req.query.fid_2);
            case 2:
                fid_mult.push(req.query.fid_1);
            case 1:
                fid_mult.push(req.query.fid_0);
        }

        //TODO: Form multi-query
        //Will need to change q? case to allow multiple f_ids

        //In the meantime, the first flight will be used instead
        fid = req.query.fid_0;

    }
    //Remake query to send to page
    var queryText = "q?get=" + get + "&f_id=" + fid +"&";
    //console.log(queryText);
    switch(get){
        case 'altVtime':
            //render alt graph
            var titleText = "Flight " + fid + " Altitude vs Time";
            var partial =  "altitude";
            var nav = 1;
            break;
        case 'receptionVtime':
	        //render recep graph
            var titleText = "Flight " + fid + " Reception vs Time";
            var partial =  "reception";
            var nav = 1;
	        break;
	    case 'map':
	        //render map
            var titleText = "Flight " + fid + " Map";
            var partial = "map";
            var nav = 1;
            break;
        case 'summary':
    	     //render summary page
            var titleText = "Flight Summary For Flight " + fid;
            var partial = "summary";
            var nav = 1;
            break;
        case 'about':
        	//render summary page
            var titleText = "About Our Team";
            var partial = "about";
            var nav = 0;
            break;
	default:
	    //Bad query
	    res.end( 'Bad Query');
    }
    //Render graph page with correct info
    res.render('graph', {title: titleText,
        partialVars: {'query': queryText, 'fid': fid, 'get': get, 'show_nav': nav},
        whichPartial: function() {
            return partial;}
        });
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
            //console.log('Hit altVtime');
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
            //console.log('Hit receptionVtime');
            sql = `SELECT time
                   FROM BeelineGPS WHERE f_id=${f_id}`+time+`
                   ORDER BY time ASC`+limit;
            break;
        case 'flightSummary':
            // Returns flight summary info
            sql = `SELECT B.*
                   FROM Flights AS F
                   INNER JOIN BeelineGPS AS B
                   ON B.f_id = F.flight_id
                   INNER JOIN (
                     SELECT callsign, MAX(time) AS latest
                     FROM BeelineGPS
                     GROUP BY callsign
                   ) AS M
                   ON M.callsign = B.callsign AND M.latest = B.time
                   WHERE F.status = 'Active'
                  `;
            break;
        case 'map':
            // Plots location v time as 2d or 3d map
            //console.log('Hit map');
            sql = `SELECT callsign as Source, time, lat, lon, alt
                   FROM BeelineGPS WHERE f_id=${f_id}`+time+`
                   ORDER BY time ASC`+limit;
            break;
      	case 'fid':
        		//return list of flight IDs
        		sql = `SELECT DISTINCT flight_id FROM Flights`;
        		break;
        default:
            // Invalid or missing get field
            //console.log('DEFAULT.  get='+get);
    }

    if(sql){
        // console.log('SQL = '+sql)
        db.query(sql,function(err, results) {
            // console.log('Results: '+results['time']);
            res.send(JSON.stringify(results));
        });
    } else {
        console.log('No SQL');
        res.end('No SQL');
    }
});

app.get('/beeline', function(req, res){
    //console.log('Beeline!');
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
