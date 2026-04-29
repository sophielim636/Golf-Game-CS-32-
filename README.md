# Golf-Game-CS-32-
Final project for CS32
## Python Golf is a text-based 9-hole stroke play golf game. Players choose clubs, hit shots, manage different lies like tee, fairway, rough, fringe, and green, and try to finish the course with the lowest score possible. The game tracks strokes, par, running score, and displays a scorecard after each hole.

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

#Future plans!!
1. Main Game Loop

The main function will control the full 18-hole game. It will:
- Display the game introduction
- Iterate through all 18 holes
- Track total strokes and score relative to par
- Display a running score and final scorecard at the end

2. Hole/Game Loop

Each hole will have its own game loop where the player plays until the ball is in the hole. This loop will:
- Prompt the player to choose a club each turn
- Use predefined club distances and accuracy values
- Call the shot outcome function to determine results
- Update the player’s lie and remaining distance
- Continue until the hole is completed

Additional Improvements**

- More detailed shot feedback after each swing
- Clearer display of hole information (par, distance, strokes)
- Improved club selection interface
- Score tracking per hole and overall scorecard
- after this, we also need to add a function that deals with when the ball goes beyond the green. Our condition will be if you are beyond the green by 30 yards, the user will encounter a hazard that sends them back to the beginning of their current hole. 


