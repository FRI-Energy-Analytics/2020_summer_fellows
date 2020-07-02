var inc = 0.05;

function setup() {
  createCanvas(256, 256);
  pixelDensity(1);
}

function draw() {
  var xoff = 0;
  var yoff = 0;
  
  loadPixels();
  for(var x = 0; x<width; x++) {
    yoff = 0;
    for(var y = 0; y<height; y++) {
      var index = (x+y*width)*4;
      var r = noise(xoff, yoff)*255;
      pixels[index] = r;
      pixels[index+1] = r;
      pixels[index+2] = r;
      pixels[index+3] = 255;
      
      yoff+=inc;
    }
    xoff+=inc;
  }
  updatePixels();
}