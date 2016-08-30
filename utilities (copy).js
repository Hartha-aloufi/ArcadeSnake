
 function Snake(color, points, width, height, start_point, direc){
    // body[0] is the snake head


      this.body = [new Rectangle(start_point[0], start_point[1], width, height)];
      this.color = color;
      this.points = points;
      this.direc = direc;


    this.can_eat = function(food){
        // collision detection
        if (this.body[0].x < food.rect.x + food.rect.width &&  this.body[0].x + this.body[0].width > food.rect.x && this.body[0].y < food.rect.y + food.rect.height && this.body[0].height + this.body[0].y > food.rect.y )
            return true;

        return false;
    }


    this.eat = function(){
        this.points += 1;
        this.body.append(Rectangle(this.body[0].x, this.body[0].y, this.body[0].width, this.body[0].height));
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
            var tempx = this.body[0].x;
            var tempy = this.body[0].y;

            this.body[0].y = new_y;
            this.body[0].x = new_x;
            this.move_body();

            if (this.detect_this_collision()){
                this.body[0].x = tempx;
                this.body[0].y = tempy;
                return false;
            }

        return true;
      }}

    this.move_body = function(){
        var length = len(this.body);

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

    this.detect_this_collision = function(){
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
    this.rect = Rectangle(0,0,7,7);
    this.calc_new_pos();

    this.calc_new_pos = function(){
        this.rect.y = (Math.random() * this.screen_height-20);
        this.rect.x = (Math.random() * this.screen_width - 20);
    }
  }
