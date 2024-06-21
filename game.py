import streamlit as st
import streamlit.components.v1 as components

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>우주 소행성 회피 게임</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: black; display: flex; justify-content: center; align-items: center; height: 100vh; }
        canvas { border: 2px solid white; }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 800;
        canvas.height = 600;

        let player = { x: canvas.width / 2, y: canvas.height / 2, radius: 10 };
        let asteroids = [];
        let gameState = 'menu'; // menu, playing, gameOver
        let level = 1;
        let timer = 0;
        let startTime;

        function drawStars() {
            for (let i = 0; i < 100; i++) {
                ctx.fillStyle = 'white';
                ctx.beginPath();
                ctx.arc(Math.random() * canvas.width, Math.random() * canvas.height, Math.random() * 2, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        function drawPlayer() {
            ctx.fillStyle = 'cyan';
            ctx.beginPath();
            ctx.moveTo(player.x, player.y - 15);
            ctx.lineTo(player.x - 10, player.y + 10);
            ctx.lineTo(player.x + 10, player.y + 10);
            ctx.closePath();
            ctx.fill();
        }

        function drawAsteroids() {
            asteroids.forEach(asteroid => {
                ctx.fillStyle = 'gray';
                ctx.beginPath();
                ctx.arc(asteroid.x, asteroid.y, asteroid.radius, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        function updateAsteroids() {
            const speed = level === 1 ? 2 : level === 2 ? 3 : 4;
            asteroids.forEach(asteroid => {
                asteroid.x += asteroid.dx * speed;
                asteroid.y += asteroid.dy * speed;

                if (asteroid.x < 0 || asteroid.x > canvas.width || asteroid.y < 0 || asteroid.y > canvas.height) {
                    resetAsteroid(asteroid);
                }
            });

            if (Math.random() < 0.05 && asteroids.length < 10 + level * 5) {
                createAsteroid();
            }
        }

        function createAsteroid() {
            const side = Math.floor(Math.random() * 4);
            let x, y;
            if (side === 0) { // top
                x = Math.random() * canvas.width;
                y = 0;
            } else if (side === 1) { // right
                x = canvas.width;
                y = Math.random() * canvas.height;
            } else if (side === 2) { // bottom
                x = Math.random() * canvas.width;
                y = canvas.height;
            } else { // left
                x = 0;
                y = Math.random() * canvas.height;
            }

            const angle = Math.atan2(player.y - y, player.x - x);
            asteroids.push({
                x: x,
                y: y,
                radius: Math.random() * 20 + 10,
                dx: Math.cos(angle),
                dy: Math.sin(angle)
            });
        }

        function resetAsteroid(asteroid) {
            const side = Math.floor(Math.random() * 4);
            if (side === 0) { // top
                asteroid.x = Math.random() * canvas.width;
                asteroid.y = 0;
            } else if (side === 1) { // right
                asteroid.x = canvas.width;
                asteroid.y = Math.random() * canvas.height;
            } else if (side === 2) { // bottom
                asteroid.x = Math.random() * canvas.width;
                asteroid.y = canvas.height;
            } else { // left
                asteroid.x = 0;
                asteroid.y = Math.random() * canvas.height;
            }

            const angle = Math.atan2(player.y - asteroid.y, player.x - asteroid.x);
            asteroid.dx = Math.cos(angle);
            asteroid.dy = Math.sin(angle);
        }

        function checkCollision() {
            return asteroids.some(asteroid => {
                const dx = asteroid.x - player.x;
                const dy = asteroid.y - player.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                return distance < player.radius + asteroid.radius;
            });
        }

        function drawUI() {
            ctx.fillStyle = 'white';
            ctx.font = '20px Arial';
            ctx.fillText(`레벨: ${level}`, 10, 30);
            ctx.fillText(`시간: ${timer.toFixed(1)}초`, 10, 60);
        }

        function update() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawStars();

            if (gameState === 'menu') {
                ctx.fillStyle = 'white';
                ctx.font = '30px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('우주 소행성 회피 게임', canvas.width / 2, canvas.height / 2 - 50);
                ctx.font = '20px Arial';
                ctx.fillText('클릭하여 시작', canvas.width / 2, canvas.height / 2 + 50);
            } else if (gameState === 'playing') {
                drawPlayer();
                drawAsteroids();
                updateAsteroids();
                drawUI();

                if (checkCollision()) {
                    gameState = 'gameOver';
                }

                const currentTime = Date.now();
                timer = (currentTime - startTime) / 1000;

                const levelDuration = level === 1 ? 10 : level === 2 ? 20 : 30;
                if (timer >= levelDuration) {
                    if (level < 3) {
                        level++;
                        startTime = currentTime;
                        timer = 0;
                        asteroids = [];
                    } else {
                        gameState = 'gameOver';
                    }
                }
            } else if (gameState === 'gameOver') {
                ctx.fillStyle = 'white';
                ctx.font = '30px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('게임 오버', canvas.width / 2, canvas.height / 2 - 50);
                ctx.font = '20px Arial';
                ctx.fillText(`최종 레벨: ${level}, 생존 시간: ${timer.toFixed(1)}초`, canvas.width / 2, canvas.height / 2);
                ctx.fillText('클릭하여 다시 시작', canvas.width / 2, canvas.height / 2 + 50);
            }

            requestAnimationFrame(update);
        }

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            player.x = e.clientX - rect.left;
            player.y = e.clientY - rect.top;
        });

        canvas.addEventListener('click', () => {
            if (gameState === 'menu' || gameState === 'gameOver') {
                gameState = 'playing';
                level = 1;
                timer = 0;
                startTime = Date.now();
                asteroids = [];
                player.x = canvas.width / 2;
                player.y = canvas.height / 2;
            }
        });

        update();
    </script>
</body>
</html>
"""

# Streamlit 앱
def main():
    st.set_page_config(page_title="우주 소행성 회피 게임", page_icon="🚀")
    
    st.title("우주 소행성 회피 게임")
    st.write("아래에서 게임을 플레이하세요!")
    
    # HTML을 Streamlit 컴포넌트로 렌더링
    components.html(HTML_TEMPLATE, height=650, width=850)
    
    st.write("게임 설명:")
    st.write("1. 마우스를 움직여 우주선을 조종하세요.")
    st.write("2. 소행성을 피해 최대한 오래 생존하세요.")
    st.write("3. 레벨이 올라갈수록 게임이 어려워집니다.")
    st.write("4. 3레벨을 클리어하면 게임 클리어!")

if __name__ == "__main__":
    main()