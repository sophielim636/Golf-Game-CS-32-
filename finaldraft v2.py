import random # used for random numbers like water hazard width, location, and shot accuracy
import time # used to control the speed of the power meter
import sys # used to update the power meter on the same line in the terminal
import threading # lets the power meter run while the player waits to press Enter

# ─── Clubs ────────────────────────────────────────────────────────────────────
CLUBS = [
    # each dictionary stores one club's name, icon, range, accuracy, and if it can be used in rough
    {"name": "Driver",        "icon": "1W", "range": (220, 280), "accuracy": 0.55, "rough": False},
    {"name": "3-iron",        "icon": "3i", "range": (170, 210), "accuracy": 0.65, "rough": True },
    {"name": "5-iron",        "icon": "5i", "range": (140, 175), "accuracy": 0.70, "rough": True },
    {"name": "7-iron",        "icon": "7i", "range": (120, 155), "accuracy": 0.75, "rough": True },
    {"name": "9-iron",        "icon": "9i", "range": ( 90, 120), "accuracy": 0.80, "rough": True },
    {"name": "Pitching wedge","icon": "PW", "range": ( 60,  95), "accuracy": 0.82, "rough": True },
    {"name": "Sand wedge",    "icon": "SW", "range": ( 30,  65), "accuracy": 0.75, "rough": True },
    {"name": "Putter",        "icon": "PT", "range": (  1,  30), "accuracy": 0.90, "rough": False},
]

# ─── Course ───────────────────────────────────────────────────────────────────
HOLES = [
    # each hole has a par and a distance
    {"par": 4, "dist": 380},
    {"par": 3, "dist": 155},
    {"par": 3, "dist": 180},
    {"par": 4, "dist": 420},
    {"par": 4, "dist": 360},
    {"par": 5, "dist": 510},
    {"par": 5, "dist": 490},
    {"par": 4, "dist": 400},
]

# turns the code names for lies into nicer labels for printing
LIE_LABELS = {
    "tee":      "Tee",
    "fairway":  "Fairway",
    "rough":    "Rough",
    "on-green": "Green",
    "fringe":   "Fringe",
}

# ─── Helpers - sophie ──────────────────────────────────────────────────────────────────
def rand(lo, hi):
    # returns a random whole number between lo and hi
    return random.randint(lo, hi)

def make_water_hazard(total_dist, width):
    # water cannot start before 20 yards so it is not too close to the tee
    min_start = 20

    # water must leave 90 yards after it ends, so this finds the latest start
    max_start = total_dist - 90 - width

    # if there is not enough space for the water hazard, return None
    if max_start <= min_start:
        return None

    # randomly chooses where the water hazard starts
    start = rand(min_start, max_start)

    # returns the start and end position of the water hazard
    return {"start": start, "end": start + width}

def score_str(strokes, par):
    # finds how many strokes above or below par the player is
    diff = strokes - par

    # matches score differences to golf names
    names = {
        -3: "Albatross",
        -2: "Eagle",
        -1: "Birdie",
         0: "Par",
         1: "Bogey",
         2: "Double bogey",
         3: "Triple bogey",
    }

    # gets the golf name, or shows the number if the score is not in the dictionary
    label = names.get(diff, f"{'+' if diff > 0 else ''}{diff}")

    # returns the score as strokes plus the golf label
    return f"{strokes} ({label})"

def rel_str(diff):
    # if the score is even with par, show E
    if diff == 0:
        return "E"

    # if over par add +, otherwise show the negative number
    return f"+{diff}" if diff > 0 else str(diff)

def draw_bar(dist_remaining, total_dist, water=None, water2=None):
    # makes the bar length based on the total distance of the hole
    width    = int((total_dist / 5) + 6)

    # removes the extra display space to get the actual playable bar length
    hole     = width - 6

    # calculates how far through the hole the ball is
    progress = max(0.0, min(1.0, 1 - dist_remaining / total_dist))

    # converts the progress into a spot on the text bar
    ball_pos = int(progress * (hole - 1))

    # creates the course bar using dots
    chars    = ["." for _ in range(hole)]

    # fills in the course behind the ball with equals signs
    for i in range(ball_pos):
        if chars[i] == ".":
            chars[i] = "="

    # draws the first water hazard if it exists
    if water:
        water_start = int((water["start"] / total_dist) * (hole - 1))
        water_end   = int((water["end"]   / total_dist) * (hole - 1))
        for i in range(water_start, min(water_end + 1, hole)):
            chars[i] = "~"

    # draws the second water hazard if it exists
    if water2:
        water_start = int((water2["start"] / total_dist) * (hole - 1))
        water_end   = int((water2["end"]   / total_dist) * (hole - 1))
        for i in range(water_start, min(water_end + 1, hole)):
            chars[i] = "~"

    # places the ball on the course bar
    chars[ball_pos] = "O"

    # places the flag at the end unless the ball is already there
    if ball_pos != hole - 1:
        chars[hole - 1] = "⛳️"

    # combines the characters into one full bar
    bar = "[" + "".join(chars) + "......]"

    # returns the finished display with the water key
    return f"\n  {bar}\n  Tee {'':>{hole - 10}} \n  ~ = Water hazard"


# ─── Power Meter - adrian ──────────────────────────────────────────────────────────────
power_val     = 0
power_stopped = False

def power_animate():
    global power_val, power_stopped
    while not power_stopped:
        sys.stdout.write(f"\r  Power: {power_val:>2}")
        sys.stdout.flush()
        power_val += 1
        if power_val > 10:
            power_val = 0
        time.sleep(0.12)

def shot_power_meter():
    global power_val, power_stopped
    power_val     = 0
    power_stopped = False

    print("\n  Press ENTER to lock in power...")

    t = threading.Thread(target=power_animate, daemon=True)
    t.start()

    input()
    power_stopped = True
    t.join()

    locked = int(power_val - 1)
    if locked == -1:
        locked = 10

    return locked

# ─── Shot outcome logic - sirina ───────────────────────────────────────────────────────
def get_outcome(lie, club, dist, power_val):
    lo, hi = club["range"]

    # 1 = lo yardage, 10 = hi yardage
    hit = int(lo + (((power_val) / 10) * (hi - lo)))
    print(f"\n  You hit the ball {hit} yards with your {club['name']}!")

    if lie == "rough":
        hit = int(hit * 0.80)

    new_dist = dist - hit
    acc      = club["accuracy"] * (0.85 if lie == "rough" else 1.0)
    roll     = random.random()

    if club["name"] == "Putter":
        if new_dist <= 0:
            return "hole", 0
        if roll < acc:
            return "on-green", max(1,new_dist)
        return "miss-green", max(3, new_dist)

    if new_dist <= 0:
        if -4 <= new_dist <= 0:
            return "hole", 0

        if new_dist <= -30:
            return "tee", dist

        return "on-green", abs(new_dist)

    if new_dist <= 4:
        return "hole", 0

    if new_dist <= 20:
        if roll < acc * 1.1:
            return "on-green", max(1, new_dist)
        return "fringe", max(5, new_dist)

    if new_dist <= 60:
        if roll < acc:
            return "fairway", new_dist
        return "rough", new_dist

    if roll < acc:
        return "fairway", new_dist
    if roll < acc + 0.15:
        return "rough", new_dist
    return "rough", new_dist

# ─── Display helpers - adrian ──────────────────────────────────────────────────────────
def print_header(hole_idx, par, dist, strokes, lie, total_strokes, total_par):
    total_diff = total_strokes - total_par
    print()
    print("=" * 52)
    print(f"  HOLE {hole_idx + 1}  |  Par {par}  |  Running score: {rel_str(total_diff)}")
    print("=" * 52)
    print(f"  Distance to hole : {dist}y")
    print(f"  Current lie      : {LIE_LABELS.get(lie, lie)}")
    print(f"  Strokes this hole: {strokes}")

def print_clubs():
    print()
    print("Clubs available:\n")
    print(f"  {'#':>2}  {'Club':<16} {'Range':>10}  {'Acc':>5}")
    print("-" * 48)
    for i, c in enumerate(CLUBS):
        lo, hi = c["range"]
        print(f"  {i+1:>2}  {c['name']:<16} {lo:>4}-{hi:<4}y  {int(c['accuracy'] * 100):>4}%")

def print_scorecard(scores):
    if not scores:
        return
    print()
    print("  ── Scorecard ──────────────────────────────────────")
    holes_line = "  Hole  : " + "  ".join(f"{i + 1:>3}" for i in range(len(scores)))
    par_line   = "  Par   : " + "  ".join(f"{HOLES[i]['par']:>3}" for i in range(len(scores)))
    score_line = "  Score : " + "  ".join(f"{s:>3}" for s in scores)
    print(holes_line)
    print(par_line)
    print(score_line)
    total_s = sum(scores)
    total_p = sum(HOLES[i]["par"] for i in range(len(scores)))
    diff    = total_s - total_p
    print(f"  Total  : {total_s} strokes  ({rel_str(diff)} vs par {total_p})")

# ─── Main game loop - sirina───────────────────────────────────────────────────────────
def play_hole(hole_idx, total_strokes, total_par):
    hole    = HOLES[hole_idx]
    par     = hole["par"]
    dist    = hole["dist"]
    lie     = "tee"
    strokes = 0
    water   = make_water_hazard(hole["dist"],random.randint(10, 90))
    water2  = make_water_hazard(hole["dist"], random.randint(10, 90))

    print(f"\n  >>> Hole {hole_idx + 1}  Par {par}  —  {dist}y  <<<")

    while True:
        print_header(hole_idx, par, dist, strokes, lie, total_strokes + strokes, total_par)
        if hole_idx <= 2:
            print(draw_bar(dist, hole["dist"], water=water, water2=None))
        elif 3 <= hole_idx <= 7:
            print(draw_bar(dist, hole["dist"], water=water, water2=water2))

        print_clubs()

        # ── Club selection - sirina ────────────────────────────────────────────
        while True:
            try:
                raw    = input("\n  Choose club (number): ").strip()
                choice = int(raw) - 1
                if not (0 <= choice < len(CLUBS)):
                    raise ValueError
            except ValueError:
                print("  Please enter a valid club number.")
                continue

            club = CLUBS[choice]

            if club["name"] == "Putter" and dist > 30:
                print("  You can only putt from the green within 30y. Choose another club.")
                continue

            if not club["rough"] and lie == "rough":
                print(f"  You can't use the {club['name']} from the rough. Choose another club.")
                continue

            break

        # ── Power meter - adrian ───────────────────────────────────────────────
        lo, hi = club["range"]
        print(f"  0 = {lo}y  ───────────────  10 = {hi}y")

        power_val = shot_power_meter()

        strokes += 1
        old_dist = dist

        result, new_dist = get_outcome(lie, club, dist, power_val)

        # ── Out of bounds - sirina ─────────────────────────────────────────────
        if result == "tee":
            print("\n  OUT OF BOUNDS! You hit too far past the hole.")
            print("  Your ball has been sent back to the tee box :(")
            dist = hole["dist"]
            lie  = "tee"
            continue

        # ── Water hazard - sophie──────────────────────────────────────────────
        for hazard in [water, water2]:
            # only check hazards that exist, and ignore water if the ball went in the hole
            if hazard and result != "hole":
                # calculates where the ball landed from the tee
                landing_spot = hole["dist"] - new_dist

                # checks if the landing spot is inside the hazard
                if hazard["start"] <= landing_spot <= hazard["end"]:
                    print("\n  WATER HAZARD! Your ball went for a swim.")
                    print("  Adding a penalty stroke and returning you to previous shot.")

                    # adds penalty stroke and returns to old distance
                    strokes += 1
                    dist = old_dist
                    break

        # if no water hazard was hit, set hazard to None
        else:
            hazard = None

        # if water was hit, restart the loop from the previous shot
        if hazard:
            continue

        # if the result is hole, finish the hole
        if result == "hole":
            print(f"  *** IN THE HOLE! {club['name']} finds the cup! ***")
            print(f"  Hole complete in {strokes} stroke{'s' if strokes != 1 else ''}. {score_str(strokes, par)}")
            print(draw_bar(0, hole["dist"], water=water))
            return strokes

        # messages for each possible result
        result_msgs = {
            "on-green":   f"  Nice shot! Ball is on the green — {new_dist}y to pin.",
            "fairway":    f"  Good strike! Sitting in the fairway — {new_dist}y remaining.",
            "rough":      f"  Shot drifts into the rough — {new_dist}y left. Tougher next swing.",
            "fringe":     f"  Ball rests on the fringe — {new_dist}y from the cup.",
            "miss-green": f"  Putt misses! Still {new_dist}y on the green.",
        }

        # prints the correct result message
        print(result_msgs.get(result, f"  {new_dist}y remaining."))

        # updates lie and distance for the next shot
        lie  = result
        dist = new_dist

#_____sirina_______ main game loop
def main():
    print()
    print("  WELCOME TO GOLF 32 \u26F3\uFE0F")
    name = input("  What would you like to name your golf course? ")
    print()
    print(f"  Course: {name} GC  |  Par 32")
    print(f"\nRules of the game: \n\nThere are 8 holes on {name} golf course. " \
    "Choose the club you want to hit for each shot and try to lock in the best power! \nBe careful not" \
    " to hit into any hazards. Hitting in the water will result in a one stroke penalty and a reset to your previous shot." \
    " \nWatch out for more water the further along the course you go!" \
    " \nBe wary of hitting over the green, too. You might get sent all the way back to the tee box!" \
    "\n \nGood luck!")

    scores        = []
    total_strokes = 0
    total_par     = 0

    for i in range(len(HOLES)):
        input(f"\n  Press Enter to tee off on Hole {i + 1}...")
        s = play_hole(i, total_strokes, total_par)
        scores.append(s)
        total_strokes += s
        total_par     += HOLES[i]["par"]
        print_scorecard(scores)

    diff = total_strokes - total_par
    print()
    print("=" * 52)
    print("  ROUND COMPLETE")
    print("=" * 52)
    print(f"  Total strokes : {total_strokes}")
    print(f"  Par           : {total_par}")
    print(f"  Score         : {rel_str(diff)}")
    if   diff <= -5: verdict = "Outstanding! You're a scratch golfer."
    elif diff <= -2: verdict = "Excellent round — well under par!"
    elif diff ==  0: verdict = "Solid golf — right on par!"
    elif diff <=  3: verdict = "Decent round. A few shots to clean up."
    else:            verdict = "Tough day on the course. Hit the range!"
    print(f"  Verdict       : {verdict}")
    print()
    print_scorecard(scores)
    print()

if __name__ == "__main__":
    main()
