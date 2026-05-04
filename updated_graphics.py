import random


# Dictionaries
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


HOLES = [
   {"par": 4, "dist": 380},
   {"par": 3, "dist": 155},
   {"par": 5, "dist": 510},
   {"par": 4, "dist": 420},
   {"par": 4, "dist": 360},
   {"par": 3, "dist": 180},
   {"par": 5, "dist": 490},
   {"par": 4, "dist": 400},
]


LIE_LABELS = {
   "tee":      "Tee",
   "fairway":  "Fairway",
   "rough":    "Rough",
   "on-green": "Green",
   "fringe":   "Fringe",
}


# Helper functions


#lo,hi is range tuple from CLUBS dictionary
def rand(lo, hi):
   return random.randint(lo, hi)

# draws the visualization
def draw_bar(dist_remaining, total_dist, width=40):
   progress = 1 - dist_remaining / total_dist
   filled = int(progress * (width - 1))
   bar = "[" + "=" * filled + "O" + "." * (width - 1 - filled) + "]"
   return f"  {bar}\n  Tee {'':>{filled}}{'':>{width - filled - 5}} Hole"

# scoring function
def score_str(strokes, par):
   diff = strokes - par
   names = {-3: "Albatross", -2: "Eagle", -1: "Birdie", 0: "Par", 1: "Bogey",2: "Double bogey", 3: "Triple bogey"}
   label = names.get(diff, f"{'+' if diff > 0 else ''}{diff}")
   return f"{strokes} ({label})"

# total scoring function
def rel_str(diff):
   if diff == 0:
      return "E"
   return f"+{diff}" if diff > 0 else str(diff)

# prints a header
def print_header(hole_idx, par, dist, strokes, lie, total_strokes, total_par):
    total_diff = total_strokes - total_par
    print()
    print("=" * 52)
    print(f"  HOLE {hole_idx + 1}  |  Par {par}  |  "
          f"Running score: {rel_str(total_diff)}")
    print("=" * 52)
    print(f"  Distance to hole : {dist}y")
    print(f"  Current lie      : {LIE_LABELS.get(lie, lie)}")
    print(f"  Strokes this hole: {strokes}")

# prints the clubs
def print_clubs():
   print("\n")
   print("Clubs available:\n")
   print(f"  {'#':>2}  {'Club':<16} {'Range':>10}  {'Acc':>5}")
   print("-" * 48)
   for i,c in enumerate(CLUBS):
      lo, hi = c["range"]
      print(f"  {i:>2}  {c['name']:<16} {lo:>4}-{hi:<4}y  {int(c['accuracy'] * 100):>4}%")

# the scorecard
def print_scorecard(scores):
    if not scores:
        return
    print()
    print("  ── Scorecard ──────────────────────────────────────")
    holes_line  = "  Hole  : " + "  ".join(f"{i+1:>3}" for i in range(len(scores)))
    par_line    = "  Par   : " + "  ".join(f"{HOLES[i]['par']:>3}" for i in range(len(scores)))
    score_line  = "  Score : " + "  ".join(f"{s:>3}" for s in scores)
    print(holes_line)
    print(par_line)
    print(score_line)
    total_s = sum(scores)
    total_p = sum(HOLES[i]["par"] for i in range(len(scores)))
    diff = total_s - total_p
    print(f"  Total  : {total_s} strokes  ({rel_str(diff)} vs par {total_p})")


#lie - string, club - dictionary index, dist - integer

def get_outcome(lie, club, dist):
   lo, hi = club["range"]
   hit = rand(lo, hi)


   if lie == "rough":
       hit = int(hit * 0.80)
           #only goes 80% as far when in rough
           #less distance
           #integer to not be float

   new_dist = dist - hit
   if lie == "rough":
       acc = club["accuracy"] * (0.85)
   else:
       club["accuracy"] * 1.0



   #generate rand float 0.0 to 1.0, f
   #your chances of hitting a good shot
   #if roll is less than accuracy, then shot was good
   # for ex. if accuracy is 90%
   roll = (random.randint(0,100))/100

    #within getoucome function
    #if statements to return lie and distance remaining accoringly
    #accuracy/chances of proximity to hole changes with how far away you are

   if club["name"] == "Putter":
      if new_dist <= 0:
         return "hole",0
      if roll < acc:
         return "on-green",new_dist
      else:
         return "missed green", new_dist + rand(2,8)

   if new_dist <= 0:
      new_dist = abs(new_dist) + rand(1,10)
      if new_dist <=4:
        return "You made it in the hole!",0
      else:
         return "on-green", new_dist

   if new_dist <= 30:
      if roll < acc*1.1:
         return "on-green", max(1,new_dist)

   if new_dist <= 60:
      if roll < acc:
         return "fairway", new_dist
      else:
         return "rough", new_dist + rand(0,15)

   if roll < acc:
      return "fairway", new_dist
   if roll < acc + .15:
      return "rough", new_dist + rand(5,20)
   else:
      return "rough", new_dist + rand(10,30)
# end of get_outcome function

# Loop to play a hole
def play_hole(hole_idx, total_strokes, total_par):
   hole = HOLES[hole_idx]
   par = hole["par"]
   dist = hole["dist"]
   lie = "tee"
   strokes = 0

   print(f"\n Hole  {hole_idx + 1} Par {par} - {dist} yards")
   # print(draw_bar(dist,dist))

   while True:
      print_header(hole_idx, par, dist, strokes, lie,total_strokes + strokes, total_par)
      print(draw_bar(dist, hole["dist"]))
      print_clubs()

      # Club selection
      while True:
         try:
            club_choice = input("\n Choose club: ").strip()
            club_choice = int(club_choice)
            if (0 <= club_choice < len(CLUBS)) == False:
               raise ValueError
         except ValueError:
            print(" Please enter a valid club number.")
            continue

         club = CLUBS[club_choice]
         lo, hi = club["range"]
         break

      # Hit
      strokes += 1
      result, new_dist = get_outcome(lie, club, dist)

      # Commentary
      print("\n")
      if result == "hole":
         print(f" IT'S IN THE HOLE! Made with {club['name']}!")
         print(f" Hole completed in {strokes}.")
         print(draw_bar(0, hole["dist"]))
         return strokes

      result_msgs = {
         "on-green":   f"  Nice shot! Ball is on the green — {new_dist}y to pin.",
         "fairway":    f"  Good strike! Sitting in the fairway — {new_dist}y remaining.",
         "rough":      f"  Shot drifts into the rough — {new_dist}y left. Tougher next swing.",
         "fringe":     f"  Ball rests on the fringe — {new_dist}y from the cup.",
         "miss-green": f"  Putt misses! Still {new_dist}y on the green.",
      }
      print(result_msgs.get(result, f" {new_dist}y remaining."))

      lie = result
      dist = new_dist

# MAIN GAME LOOP
def main():
    print('\n')
    print("  WELCOME TO GOLF 32 \u26F3\uFE0F")
    name = input("  What would you like to name your golf course? ")
    print('\n')
    print(f"  Course: {name} GC  |  Par 32")

    scores        = []
    total_strokes = 0
    total_par     = 0

    for i in range(len(HOLES)):
        input(f"\n  Press Enter to tee off on Hole {i + 1}...")
        s = play_hole(i, total_strokes, total_par)
        scores.append(s)
        total_strokes += s
        total_par += HOLES[i]["par"]
        print_scorecard(scores)

    # Final summary
    diff = total_strokes - total_par
    print()
    print("=" * 52)
    print("  ROUND COMPLETE")
    print("=" * 52)
    print(f"  Total strokes : {total_strokes}")
    print(f"  Par           : {total_par}")
    print(f"  Score         : {rel_str(diff)}")
    if diff <= -5:
        verdict = "Outstanding! You're a scratch golfer."
    elif diff <= -2:
        verdict = "Excellent round — well under par!"
    elif diff == 0:
        verdict = "Solid golf — right on par!"
    elif diff <= 3:
        verdict = "Decent round. A few shots to clean up."
    else:
        verdict = "Tough day on the course. Hit the range!"
    print(f"  Verdict       : {verdict}")
    print('\n')
    print_scorecard(scores)
    print('\n')

if __name__ == "__main__":
    main()





