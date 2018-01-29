  /**
   * Creates a Spritesheet
   * @param {string} - Path to the image.
   * @param {number} - Width (in px) of each frame.
   * @param {number} - Height (in px) of each frame.
   */
function SpriteSheet(path, frameWidth, frameHeight) {
    this.image = new Image();
    this.frameWidth = frameWidth;
    this.frameHeight = frameHeight;

    // calculate the number of frames in a row after the image loads
    var self = this;
    this.image.onload = function() {
      self.framesPerRow = Math.floor(self.image.width / self.frameWidth);
    };

    this.image.src = path;
}

function Player() {
    this.sheet = new SpriteSheet('static/images/ryu.gif', 200, 40)
    this.walkAnim  = new Animation(this.sheet, 4, 0, 15);

    // this.jumpAnim  = new Animation(this.sheet, 4, 15, 15);
    // this.fallAnim  = new Animation(this.sheet, 4, 11, 11);f

    this.anim = this.walkAnim
    this.x = 100;
    this.y = 100;


    this.update = function() {
        this.anim.update();
    }
    /**
     * Draw the player at it's current position
     */
    this.draw = function() {
      this.anim.draw(this.x, this.y);
    };
}

/**
 * Creates an animation from a spritesheet.
 * @param {SpriteSheet} - The spritesheet used to create the animation.
 * @param {number}      - Number of frames to wait for before transitioning the animation.
 * @param {array}       - Range or sequence of frame numbers for the animation.
 * @param {boolean}     - Repeat the animation once completed.
 */
function Animation(spritesheet, frameSpeed, startFrame, endFrame) {

    var animationSequence = [];  // array holding the order of the animation
    var currentFrame = 0;        // the current frame to draw
    var counter = 0;             // keep track of frame rate

    // start and end range for frames
    for (var frameNumber = startFrame; frameNumber <= endFrame; frameNumber++) {
      animationSequence.push(frameNumber);
    }

    /**
     * Update the animation
     */
    this.update = function() {

      // update to the next frame if it is time
      if (counter == (frameSpeed - 1))
        currentFrame = (currentFrame + 1) % animationSequence.length;

      // update the counter
      counter = (counter + 1) % frameSpeed;
    };

    /**
     * Draw the current frame
     * @param {integer} x - X position to draw
     * @param {integer} y - Y position to draw
     */
    this.draw = function(x, y) {
      // get the row and col of the frame
      var row = Math.floor(animationSequence[currentFrame] / spritesheet.framesPerRow);
      var col = Math.floor(animationSequence[currentFrame] % spritesheet.framesPerRow);

      ctx.drawImage(
        spritesheet.image,
        col * spritesheet.frameWidth, row * spritesheet.frameHeight,
        spritesheet.frameWidth, spritesheet.frameHeight,
        x, y,
        spritesheet.frameWidth, spritesheet.frameHeight);
    };
}

function animate() {
    if (stop) {
        return;
    }
    requestAnimFrame( animate );
    ctx.clearRect(0, 0, canvas.width, canvas.height);

      // background.draw();
    player.update();
    player.draw(100, 100);
}

/**
 * Request Animation Polyfill
 */
var requestAnimFrame = (function(){
return  window.requestAnimationFrame       ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        window.oRequestAnimationFrame      ||
        window.msRequestAnimationFrame     ||
        function(callback, element){
          window.setTimeout(callback, 1000 / 60);
        };
})();


var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

var player = new Player()

var stop = false;

function startGame() {
    animate();
    ctx.scale(2, 2)
}

startGame();

