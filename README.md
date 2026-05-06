# Golf-Game-CS-32-
Final project for CS32
## Python Golf is a text-based 9-hole stroke play golf game. Players choose clubs, hit shots, manage different lies like tee, fairway, rough, fringe, and green, and try to finish the course with the lowest score possible. The game tracks strokes, par, running score, and displays a scorecard after each hole.

New learning situation: 
- one is the power bar, imported sys and threading library. We used AI to learn about them (how/what we learned and how we implemented them is explained in the video).
- Used AI for formatting of our dictionaries at the beginning.
- Originally we were going to do key press method to choose our shot power. We used code online in an older version of the code, but instead elected for the power bar with number 0-10. The reason we didn't do an oscillating 0-10 is because we wanted to increase difficulty - when you try to hit it at power 10 (for maximum distance), there's a chance you hit it at 0 or 1, so it's high risk high reward.

## How to Run

1. Make sure Python 3 is installed.
2. Save the game code in a file, such as `golf.py`.
3. Open a terminal in the folder containing the file.
4. Run.
5. In the code the user will be prompted to choose a club and they will be provided with the distance each club goes. They will then input a number in the terminal to select the club for each stroke. 
6. After each shot, the following will be displayed on the screen until the completion:
    a. how far their ball went
    b. how much distance they have left to target
    c. their total score
    d. their current lie (fairway, fringe, green, or rough)
    e. information about the current hole (par, distance) 
    f. strokes on the current hole

#FP Update
Currently we have coded:
- Multiple golf clubs with realistic ranges and accuracy values
- 9-hole course with different pars and distances
- Shot outcome system that simulates:
  - Distance hit
  - Accuracy randomness
  - Effects of different lies (tee, fairway, rough, green, fringe)
- Rough penalty (reduced distance and accuracy)
- Putter logic for short distances
- Dynamic feedback after each shot
- Visual distance bar showing progress from tee to hole

The game calculates where the ball lands after each shot and updates the player's situation accordingly.


1. Main Game Loop

The main function will control the full 8-hole game. It will:
- Display the game introduction
- Iterate through all 8 holes
- Track total strokes and score relative to par
- Display a running score and final scorecard at the end

2. Hole/Game Loop

Each hole will have its own game loop where the player plays until the ball is in the hole. This loop will:
- Prompt the player to choose a club each turn
- prompt player to hit enter to choose a 'power' from a fast moving scale of 0-10 to determine distance
- Use predefined club distance ranges and accuracy values
- Call the shot outcome function to determine results
- Update the player’s lie and remaining distance
- Continue until the hole is completed

- Clearer display of hole information (par, distance, strokes)
- Club selection choices printed for player
- Score tracking per hole and overall scorecard
- if you are beyond the green by 30 yards, the user will be sent back to the beginning of their current hole
- if you hit into a water hazard, your score will gain a penalty stroke of 1 and you'll be sent back to your previous shot.
- water hazards are randomly generated (can be from 10 to 90 yards), we make sure they don't overlap with the tee box or the green.
- there can be max 1 water hazard on the first 4 holes, and can be up to 2 water hazards on the second 4 holes (to increase difficulty)


- Hole Gameplay Loop (`play_hole`)
  - Implemented a loop that allows the player to play an entire hole from tee to finish
  - Continues prompting the user until the ball is in the hole

- Input for Club Selection
  - Players can choose a club by entering a number in the terminal
  - Difficulty in choosing power - trying to hit it at the right power

- After Shot 
  - After each shot, the game prints a message describing the result (fairway, rough, green, etc.)

- Stroke Tracking
  - The number of strokes per hole is now tracked and displayed when the hole is completed

- Win Condition for Each Hole
  - The game detects when the ball goes in the hole and ends the loop for that hole

- Improved Visualization
  - Added a distance progress bar that updates after each shot
 
Since our FP Status, we have changed the scope of our game to extend from being able to play one hole to play all 8 and keep score throughout. In addition, we have added the player input part of the game where the player has control in how each shot is hit through the power bar moving 0-10 scale. Instead of printing all the numbers repeating on the same line with the sys library. We also added more penalty and difficulty in the game with the water hazards and the out of bounds penalty for hitting over the green. We added a visual representation of the green to the draw_bar by adding more ticks after the hole. When hitting out of bounds over the green, the player's sent back to the tee box and if in the water, the player gets sent back to the previous shot with an extra stroke added. In both cases, the score keeps counting as is. If we were to continue the project, some next steps we'd take would be to possibly add a network so you could play against another player or a computer. You could play the same course simultaneously and compare scores. This would be ideal because each time you play the game, although each hole will be the same yardage, the water hazards are randomly generated each time so the course is different each time. Additionally, we would exten the graphics to be in two dimensions so we could also depict hitting into the rough on the left or the right.

