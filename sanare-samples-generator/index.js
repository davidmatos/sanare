'use strict';

const ENDPOINTS_FILE_PATH = 'endpoints.json';

const fs = require('fs');
const http = require('http')
const mysql = require('mysql');



let rawdata = fs.readFileSync(ENDPOINTS_FILE_PATH);
let endpointsFile = JSON.parse(rawdata);

const httpOptions = {
    hostname: endpointsFile.hostname,
    port: endpointsFile.port,
    //protocol: endpointsFile.protocol
  }


var con = mysql.createConnection({
    host: "127.0.0.1",
    port: "3306",
    user: "root",
    password: "somewordpress",
    database: "wordpress"
  });



//var sqlQuery =  "select event_time, user_host, command_type, convert(argument using utf8) as query from mysql.general_log where event_time > '2020-11-02 17:30:00.0' limit 10"

con.connect(function(err) {
    if (err) throw err; 



    let urlsLength = endpointsFile.endpoints.length;

    for(let i = 0; i < urlsLength; i++){
        performHttpRequest(endpointsFile.endpoints[i]);
    
    }



    





});




var i = 0;
function performHttpRequest(endpoint){
    if(endpoint.method === 'GET'){
        httpOptions.method = 'GET';
        httpOptions.path = endpoint.path; 

        
        var dateStr = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '') + '.0';
        const req = http.request(httpOptions, res => {
            console.log("Executing: " + endpoint.path);
            console.log(`statusCode: ${res.statusCode}npm `);
            res.on('data', d => {
              //process.stdout.write(d)

            var sqlQuery =  "select event_time, user_host, command_type, convert(argument using utf8) as query from mysql.general_log where event_time > '"+dateStr+"'"

            
              con.query(sqlQuery, function (err, result) {
                if (err) throw err;
                //console.log(result);
                console.log('batatas' + (i++));
            });
              
            })
          })
          
          req.on('error', error => {
            console.error(error)
          })
          
          req.end()


    }else{
        //PUT, POST and DELETE
        


        const httpOptions = {
            hostname: 'whatever.com',
            port: 443,
            path: '/todos',
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Content-Length': data.length
            }
          }
          
          const req = http.request(httpOptions, res => {
            console.log(`statusCode: ${res.statusCode}`)
          
            res.on('data', d => {
              process.stdout.write(d)
            })
          })
          
          req.on('error', error => {
            console.error(error)
          })
          
          req.write(data)
          req.end()


    }


}