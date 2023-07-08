# Portfolio
Portfolio for Game Development and Technology 

Welcome to my portfolio showcasing some games I have developed by myself using Python during my free time over the past year. I self-taught the libraries and had tons of fun figuring out how to create these projects. Explore and enjoy!

For each game I have provided a brief overview of what the game is about, reasons on why the game was made and the controls to play the game. I will also provide the libraries used in each game and included some images to show how the games looks like.

# Games
- Ice pong
- Minesweeper
- mini golf
- UNO discord bot
- puzzle plunge

# Ice pong
Ice pong is a unique twist on the classic Pong game, where everything is set on an icy surface. The paddles and the ball slides across the slippery ice, making every move more challenging and unpredictable. Players must adjust their strategies and timing to account for the slippery nature of the game, as the ice affects the trajectory and speed of the ball.

Project inspiration:
For this project, it was my first ever project without following any tutorials from YouTube. I learned methods for moving different rectangles, creating circles, and practicing the use of hitboxes. I believe that creating Pong with a new twist is a great way to begin developing a game from scratch.

Libraries used:
- Pygame

![image](https://github.com/D-exter/Portfolio/assets/138134061/20bc01b8-ca23-4f24-80dc-cca92e7aa571)

Controls
- Player 1: W for up, S for down
- Player 2: Up key, Down key


# Minesweeper
A simple recreation of Minesweeper the game. Customize the size of the minefield and adjust the number of bombs to your liking. Minesweeper allows you to test your skills and logic in a game that never gets old. Uncover the squares, avoid the hidden bombs, and aim for a high score in this timeless puzzle adventure.

Project inspiration:
I really enjoyed playing Minesweeper back in secondary school, but I felt limited by the lack of customization options when I wanted to adjust the number of mines. This project taught me valuable skills in randomly generating mines in the field and capturing user clicks and correctly displaying information on the screen.

Libraries used:
- Pygame
- random

![image](https://github.com/D-exter/Portfolio/assets/138134061/e61a42d5-f68c-47dc-b737-030b908f4ec9)
![image](https://github.com/D-exter/Portfolio/assets/138134061/27e7d858-5e77-4201-98a1-d06d84899b05)

Controls
- Uncover Tile: Left click 
- Set Flag: Right click


# Mini golf
Mini Golf is a game of precision and skill as you navigate through various challenging levels. Use simple controls by clicking and dragging on the ball to determine the direction and strength of your shot. With customizable game features, you can adjust the size of the course and the number of obstacles. Aim for the lowest number of shots possible for each level.

Project inspiration:
This project is a recreation of the mini golf game that I used to play with my friends on Plato. My goal was to challenge myself and learn how to create realistic ball movement and accurately implement hitboxes. 

Libraries used:
- Pygame
- random

![image](https://github.com/D-exter/Portfolio/assets/138134061/a7419830-0cd8-485b-86eb-ce9798ab2cf5)

Controls
- First shot: Click in orange box area
- Move ball: Click and drag in ball


# UNO discord bot
The Uno Discord bot is an experience of the classic card game Uno right in your Discord server. Uno is a game where you play strategically and match the color or number of the top card on the discard pile. Special cards like Skip, Reverse, and Draw Two add twists and turns to the gameplay.

Project inspiration:
After watching some videos on creating Discord bots with Python, I was inspired to create something that would allow me to play games with my friends. The main objective of this project was to learn the Discord library and leverage its functionalities to develop a multiplayer game. Discord serves as the platform or medium through which players can interact and participate in the game.

Libraries used:
- Discord
- Json
- Random

![image](https://github.com/D-exter/Portfolio/assets/138134061/9cb8aeb9-1f77-465d-ac66-a8a625150d61)
![image](https://github.com/D-exter/Portfolio/assets/138134061/576f5f65-4ea5-4e16-af1e-fc14cc78e438)
![image](https://github.com/D-exter/Portfolio/assets/138134061/4688102a-5424-4057-87cb-dec37e60f95e)


Commands

!join - 
Join the game

!leave - 
Leave the game

!startgame - 
Once everyone has joined, start the game

!playcard - 
To play a card in Uno, use the playcard command and specify the position or index of the card you want to play. For example, if you want to play the third card from the left in your hand, type !playcard 3. This means you'll count the cards in your hand from left to right and select the corresponding position to play the desired card. Make sure to choose a valid card that matches the color, number, or special actions required by the current card at the top. do not worry as the bot will send back a message to tell you if the card cannot be played

!draw - 
Play this command if you do not have any playable cards but you can still draw even if you have a playable card.
If there is card chaining and you do not have a +2 or +4 wild card to play you can play !draw to draw all the accumulated penalty cards.

!c - 
When a wild card is played, this command becomes available for that player to choose the color of the next playable card.
e.g., !c r for red, !c g for green, etc.


# Puzzle plunge
Puzzle Plunge is game where you navigate through a grid-based maze, collecting coins and reaching the designated goal square. Once a movement key is pressed, you will continue moving in that direction until it hits a wall. You have to collect all coins before you are allowed to reach the goal and complete the level. In the main menu there is a level editor where you use a simple interface to create your own level and play it after.

Project inspiration:
I created this project with the goal of designing a grid-based puzzle game that features a level editor allowing players to save and play their own custom levels. Inspired by the idea of movement-based puzzles, I developed a simple yet engaging game concept. The game utilizes color-coded boxes representing the player, walls, coins, and goals, which adds visual clarity and enhances the gameplay experience. By incorporating a level editor, players can create and share their unique puzzles with others.

Libraries used:
- Pygame
- Json

![image](https://github.com/D-exter/Portfolio/assets/138134061/7f899bf7-44ec-4e1e-926d-1ae5388f2c2d)

![image](https://github.com/D-exter/Portfolio/assets/138134061/6f00c825-dd44-47ef-b2ee-6df9f5dc138b)


Controls

- Movement: WASD keys

level editor
- cycle box type: left click box

0 = bg    WHITE / 
1 = player    GREEN / 
2 = wall  BLUE / 
3 = goal  RED / 
4 = coin  YELLOW / 
5 = black bg  BLACK

- set box to bg: right click
