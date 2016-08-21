var http = require('http');
var server = http.createServer(function(req, res){
  res.writeHead(200, {"Content/Type" : "text/html"});
  res.write('Arcade server');
});
var io = require('socket.io');

server.listen(8080);

console.log('server is now running');
