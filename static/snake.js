const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let snake = [{ x: 150, y: 150 }];
let dx = 15;
let dy = 0;
let food = spawnFood();
let score = 0;
let gameOver = false;

document.addEventListener("keydown", moveSnake);

function moveSnake(e) {
  if (e.key === "ArrowUp" && dy === 0) { dx = 0; dy = -15; }
  else if (e.key === "ArrowDown" && dy === 0) { dx = 0; dy = 15; }
  else if (e.key === "ArrowLeft" && dx === 0) { dx = -15; dy = 0; }
  else if (e.key === "ArrowRight" && dx === 0) { dx = 15; dy = 0; }
}

function spawnFood() {
  return {
    x: Math.floor(Math.random() * (canvas.width / 15)) * 15,
    y: Math.floor(Math.random() * (canvas.height / 15)) * 15,
  };
}

function draw() {
  if (gameOver) return;

  ctx.fillStyle = "#1e1e1e";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  snake.unshift({ x: snake[0].x + dx, y: snake[0].y + dy });

  // collision
  if (snake[0].x < 0 || snake[0].x >= canvas.width || snake[0].y < 0 || snake[0].y >= canvas.height ||
      snake.slice(1).some(s => s.x === snake[0].x && s.y === snake[0].y)) {
    gameOver = true;
    sendScore(score);
    alert("Game Over! Score: " + score);
    window.location.href = "/dashboard";
    return;
  }

  if (snake[0].x === food.x && snake[0].y === food.y) {
    score += 1;
    food = spawnFood();
  } else {
    snake.pop();
  }

  // draw food
  ctx.fillStyle = "red";
  ctx.fillRect(food.x, food.y, 15, 15);

  // draw snake
  ctx.fillStyle = "lime";
  snake.forEach(s => ctx.fillRect(s.x, s.y, 15, 15));

  // draw score
  ctx.fillStyle = "white";
  ctx.font = "16px consolas";
  ctx.fillText("Score: " + score, 10, 20);
}

setInterval(draw, 120);

function sendScore(score) {
  console.log("Sending score:", score);
  fetch("/update_score", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ score: score })
  }).then(response => {
    console.log("Server response:", response.status);
  });
}



