var http = require('http');
var server = http.createServer(function(req, res){
	res.end('Arcade server');
});

var io = require('socket.io')(server);

const GREEN = [153, 204, 0];
const YELLOW = [255, 191, 0];
const SELVER = [140, 140, 140];
const RED = [255, 0 , 0];
const SNAKE_WIDTH = 12;
const SNAKE_HEIGHT = 12;
const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 600;
const player1_start_point = [10, 10];
const player2_start_point = [780, 580];
const SPEED = 12;

server.listen(8080);
console.log('server is now running');

var connection = [];
var player = [];

var food = new Food(SCREEN_WIDTH, SCREEN_HEIGHT, RED);
var connectionCounter = 0;

io.on('connection', function(socket){
	connectionCounter++;

	// temprory, to handle double connections
	if((connectionCounter & 1) == 1)
		return;

	console.log('new user connect ');

	socket.on('create new player', function(){
		console.log('dddd');
		connection.push(socket);
		player.push(new Snake(GREEN, 0, SNAKE_WIDTH, SNAKE_HEIGHT, player1_start_point,1));

	});

	socket.on('disconnect', function(){
  		var playerIndex = connection.indexOf(socket);

			if(playerIndex == -1)
				return;

  		player.splice(playerIndex, 1);
  		connection.splice(playerIndex, 1);
  		console.log('player number ' + playerIndex + ' disconnect');
	});

	socket.on('changeDirction', function(newDirection){
		var  idx = connection.indexOf(socket);

		if(idx == -1)
			return;

		var dir = player[idx].direc;

		if((dir % 2 == 0 && dir -1 != newDirection) || (dir % 2 != 0 && dir + 1 != newDirection))
				player[idx].direc = newDirection;
	});

	socket.on('draw request', function(isGameStarted){

		if(player.length < 2 || !isGameStarted){
			io.emit('before start the game');
			return;
		}


		var playerIndex = connection.indexOf(socket);
		// recive draw request from single client only
		if(playerIndex != 0 && connection.length != 0)
			return;

		var winner = -1;

		for (var i = 0; i < player.length; i++) {
			if(player[i].move_head(SPEED, SCREEN_WIDTH, SCREEN_HEIGHT) ){
					if(player[i].detect_self_collision()){
							player[i].color = RED;
							//game over
					} else {
						for (var j = 0; j < player.length; j++) {
							if(i == j)
								continue;
							if(player[i].detect_collision_with_other_player(player[j])){
								player[i].color = RED;
								// game over
							}
						}
					}
			}

			if(player[i].can_eat(food)){
				player[i].eat();

				if(player[i].points == 1){
					winner = i;
				}

				food.calc_new_pos();
			}
		}

		io.emit('draw', {player : player, food : food});

		if(winner != -1)
			io.emit('player win', i);
	});

});





function Snake(color, points, width, height, start_point, direc){
	// body[0] is the snake head


	this.body = [new Rectangle(start_point[0], start_point[1], width, height)];
	this.color = color;
	this.points = points
	this.direc = direc;


	this.can_eat = function(food){
		// collision detection
		if (this.body[0].x < food.rect.x + food.rect.width &&  this.body[0].x + this.body[0].width > food.rect.x && this.body[0].y < food.rect.y + food.rect.height && this.body[0].height + this.body[0].y > food.rect.y )
			return true;

		return false;
	}


	this.eat = function(){
		this.points += 1;
		this.body.push(new Rectangle(this.body[0].x, this.body[0].y, this.body[0].width, this.body[0].height));
	}


	this.move_head = function(speed, width, height){
		var new_x = this.body[0].x;
		var new_y = this.body[0].y;

		if (this.direc == 1)
			new_x += speed;
		else if (this.direc == 2)
			new_x -= speed;
		else if (this.direc == 3)
			new_y -= speed;
		else if (this.direc == 4)
			new_y += speed;

		if (new_x < width && new_x > -1 && new_y < height && new_y > -1){

			this.move_body();
			this.body[0].y = new_y;
			this.body[0].x = new_x;

			return true;
		}

		return false;
	}

	this.move_body = function(){
		var length = this.body.length;

		for(var i = 1; i < this.body.length; i++){
			this.body[length - i].x = this.body[length - i - 1].x;
			this.body[length - i].y = this.body[length - i - 1].y;
		}
	}


	this.detect_collision_with_other_player = function(other){
		for(var i = 1 ; i < other.body.length; i++){
			if (this.body[0].x < other.body[i].x + other.body[i].width &&  this.body[0].x + this.body[0].width > other.body[i].x && this.body[0].y < other.body[i].y + other.body[i].height && this.body[0].height + this.body[0].y > other.body[i].y)
				return true;
		}
	}

	this.detect_self_collision = function(){
		for(var i = 3; i < this.body.length; i++)
			if (this.body[0].x < this.body[i].x + this.body[i].width &&  this.body[0].x + this.body[0].width > this.body[i].x && this.body[0].y < this.body[i].y + this.body[i].height && this.body[0].height + this.body[0].y > this.body[i].y)
				return true;

		return false;
	}

}



function Rectangle(x, y, width, height){
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
}

function Food(screen_width, screen_height, color){

	this.screen_width = screen_width;
	this.screen_height = screen_height;
	this.color = color;
	this.rect = new Rectangle(50,50,7,7);


	this.calc_new_pos = function(){

		this.rect.y = (Math.random() * (this.screen_height-20));
		this.rect.x = (Math.random() * (this.screen_width - 20));

	}
}
