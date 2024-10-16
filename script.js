// Bouncing logo variables
const logo = document.getElementById("logo");
let xPos = 100;
let yPos = 100;
let xSpeed = 3;
let ySpeed = 3;

function updateLogo() {
  const container = document.querySelector(".container");
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;
  const logoWidth = logo.clientWidth;
  const logoHeight = logo.clientHeight;

  // Move the logo
  xPos += xSpeed;
  yPos += ySpeed;

  // Check for collision with container edges
  if (xPos + logoWidth >= containerWidth || xPos <= 0) {
    xSpeed *= -1; // Reverse direction on the X axis
  }

  if (yPos + logoHeight >= containerHeight || yPos <= 0) {
    ySpeed *= -1; // Reverse direction on the Y axis
  }

  // Update the position of the logo
  logo.style.left = xPos + "px";
  logo.style.top = yPos + "px";

  requestAnimationFrame(updateLogo); // Call update on the next frame
}

updateLogo(); // Start the logo animation

// Eye tracking setup
window.onload = function () {
  // Start WebGazer.js to track eye movement
  webgazer
    .setGazeListener(function (data, elapsedTime) {
      if (data == null) {
        return;
      }

      // Update the position of the eye tracking pointer
      const eyePointer = document.getElementById("eyePointer");
      eyePointer.style.left = data.x + "px";
      eyePointer.style.top = data.y + "px";
    })
    .begin();

  // Optional: to hide the webgazer video and feedback box
  webgazer.showVideoPreview(false).showPredictionPoints(false);
};
