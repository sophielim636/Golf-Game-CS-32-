import random
import time
import sys
import threading

# ─── Clubs ────────────────────────────────────────────────────────────────────
CLUBS = [
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
    {"par": 4, "dist": 380},
    {"par": 3, "dist": 155},
    {"par": 5, "dist": 510},
    {"par": 4, "dist": 420},
    {"par": 4, "dist": 360},
    {"par": 3, "dist": 180},
    {"par": 5, "dist": 490},
    {"par": 4, "dist": 400},
    {"par": 4, "dist": 370},
]

LIE_LABELS = {
    "tee":      "Tee",
    "fairway":  "Fairway",
    "rough":    "Rough",
    "on-green": "Green",
    "fringe":   "Fringe",
}

# ─── Helpers ──────────────────────────────────────────────────────────────────
def rand(lo, hi):
    return random.randint(lo, hi)

def make_water_hazard(total_dist, width):
    min_start = 20
    max_start = total_dist - 90 - width
    if max_start <= min_start:
        return None
    start = rand(min_start, max_start)
    return {"start": start, "end": start + width}

def score_str(strokes, par):
    diff = strokes - par
    names = {
        -3: "Albatross",
        -2: "Eagle",
        -1: "Birdie",
         0: "Par",
         1: "Bogey",
         2: "Double bogey",
         3: "Triple bogey",
    }
    label = names.get(diff, f"{'+' if diff > 0 else ''}{diff}")
    return f"{strokes} ({label})"

def rel_str(diff):
    if diff == 0:
        return "E"
    return f"+{diff}" if diff > 0 else str(diff)

def draw_bar(dist_remaining, total_dist, water=None, water2=None):
    width    = int((total_dist / 5) + 6)
    hole     = width - 6
    progress = max(0.0, min(1.0, 1 - dist_remaining / total_dist))
    ball_pos = int(progress * (hole - 1))
    chars    = ["." for _ in range(hole)]

    if water:
        water_start = int((water["start"] / total_dist) * (hole - 1))
        water_end   = int((water["end"]   / total_dist) * (hole - 1))
        for i in range(water_start, min(water_end + 1, hole)):
            chars[i] = "~"

    if water2:
        water_start = int((water2["start"] / total_dist) * (hole - 1))
        water_end   = int((water2["end"]   / total_dist) * (hole - 1))
        for i in range(water_start, min(water_end + 1, hole)):
            chars[i] = "~"

    for i in range(ball_pos):
        if chars[i] == ".":
            chars[i] = "="

    chars[ball_pos] = "O"
    if ball_pos != hole - 1:
        chars[hole - 1] = "⛳️"

    bar = "[" + "".join(chars) + "......]"
    return f"\n  {bar}\n  Tee {'':>{hole - 10}} \n  ~ = Water hazard"


# ─── Power Meter ──────────────────────────────────────────────────────────────
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

# ─── Shot outcome logic ───────────────────────────────────────────────────────
def get_outcome(lie, club, dist, power_val):
    lo, hi = club["range"]

    # 1 = lo yardage, 10 = hi yardage
    hit = int(lo + (((power_val) / 10) * (hi - lo)))
    print(f"  You hit the ball {hit} yards with your {club['name']}!")

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

# ─── Display helpers ──────────────────────────────────────────────────────────
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

# ─── Main game loop ───────────────────────────────────────────────────────────
def play_hole(hole_idx, total_strokes, total_par):
    hole    = HOLES[hole_idx]
    par     = hole["par"]
    dist    = hole["dist"]
    lie     = "tee"
    strokes = 0
    water   = make_water_hazard(hole["dist"],random.randint(10, 90))
    water2  = make_water_hazard(hole["dist"], random.randint(10, 90))


    print(f"\n  >>> Hole {hole_idx + 1}  Par {par}  —  {dist}y  <<<")

    if hole_idx <= 1:
        print(draw_bar(dist, hole["dist"], water=water, water2=None))
    elif 2 <= hole_idx <= 7:
        print(draw_bar(dist, hole["dist"], water=water, water2=water2))

    while True:
        print_header(hole_idx, par, dist, strokes, lie, total_strokes + strokes, total_par)
  #      print(draw_bar(dist, hole["dist"], water=water, water2=water2))
        print_clubs()

        # ── Club selection ────────────────────────────────────────────
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

        # ── Power meter ───────────────────────────────────────────────
        lo, hi = club["range"]
        print(f"  0 = {lo}y  ───────────────  10 = {hi}y")

        power_val = shot_power_meter()

        strokes += 1
        old_dist = dist

        result, new_dist = get_outcome(lie, club, dist, power_val)

        # ── Out of bounds ─────────────────────────────────────────────
        if result == "tee":
            print("\n  OUT OF BOUNDS! You hit too far past the hole.")
            print("  Your ball has been sent back to the tee box :(")
            dist = hole["dist"]
            lie  = "tee"
            continue

        # ── Water hazard ──────────────────────────────────────────────
        for hazard in [water, water2]:
            if hazard and result != "hole":
                landing_spot = hole["dist"] - new_dist
                if hazard["start"] <= landing_spot <= hazard["end"]:
                    print("\n  WATER HAZARD! Your ball went for a swim.")
                    print("  Adding a penalty stroke and returning you to previous shot.")
                    strokes += 1
                    dist = old_dist
                    break
        else:
            hazard = None

        if hazard:
            continue

        if result == "hole":
            print(f"  *** IN THE HOLE! {club['name']} finds the cup! ***")
            print(f"  Hole complete in {strokes} stroke{'s' if strokes != 1 else ''}. {score_str(strokes, par)}")
            print(draw_bar(0, hole["dist"], water=water))
            return strokes

        result_msgs = {
            "on-green":   f"  Nice shot! Ball is on the green — {new_dist}y to pin.",
            "fairway":    f"  Good strike! Sitting in the fairway — {new_dist}y remaining.",
            "rough":      f"  Shot drifts into the rough — {new_dist}y left. Tougher next swing.",
            "fringe":     f"  Ball rests on the fringe — {new_dist}y from the cup.",
            "miss-green": f"  Putt misses! Still {new_dist}y on the green.",
        }
        print(result_msgs.get(result, f"  {new_dist}y remaining."))

        lie  = result
        dist = new_dist

def main():
    print()
    print("  WELCOME TO GOLF 32 \u26F3\uFE0F")
    name = input("  What would you like to name your golf course? ")
    print()
    print(f"  Course: {name} GC  |  Par 32")

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
