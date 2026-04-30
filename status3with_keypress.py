import random
import time

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
   {"par": 4, "dist": 370},
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


def draw_bar(dist_remaining, total_dist, width=40):
   progress = 1 - dist_remaining / total_dist
   filled = int(progress * (width - 1))
   bar = "[" + "=" * filled + "O" + "." * (width - 1 - filled) + "]"
   return f"  {bar}\n  Tee {'':>{filled}}{'':>{width - filled - 5}} Hole"




#lie - string, club - dictionary index, dist - integer

def get_outcome(lie, club, dist, swing_time):
   lo, hi = club["range"]
   hit = rand(lo, hi)

   #3 seconds = perfect hit
   base_time = 3.0
   mid_dist = (lo+hi)/2

   #shot power is related to how long you held key relative to 3 seconds
   power = swing_time/base_time
   #power min and max
   power = max(0.2, min(power, 1.8))
   #hit is the power you put on the shot times the club's average range
   hit = int(mid_dist*power)


   if lie == "rough":
       hit = int(hit * 0.80)
           #only goes 80% as far when in rough
           #less distance
           #integer to not be float

   new_dist = dist - hit
   if lie == "rough":
       acc = club["accuracy"] * (0.85)
   else:
       acc = club["accuracy"] * 1.0



   #generate rand float 0.0 to 1.0, f
   #your chances of hitting a good shot
   #if roll is less than accuracy, then shot was good
   # for ex. if accuracy is 90%
   roll = (random.randint(0,100))/100


#new stuff for FP status submission 4/22/26:

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
# end of getoucome function

# NEW
def play_hole(hole_idx, total_strokes, total_par):
   hole = HOLES[hole_idx]
   par = hole["par"]
   dist = hole["dist"]
   lie = "tee"
   strokes = 0

   print(f"\n Hole  {hole_idx + 1} Par {par} - {dist} yards")
   # print(draw_bar(dist,dist))

   while True:
      # GRAPHICS GO HERE
      print(draw_bar(dist, hole["dist"]))

      # Club selection
      while True:
         try:
            club_choice = input("\n Choose club: ").strip()
            club_choice = int(club_choice)
            if (0 <= club_choice < len(CLUBS)) == False:
               raise ValueError
         except ValueError:
            print(" Please enter a valud club number.")
            pass # is this the right thing?

         club = CLUBS[club_choice]
         lo, hi = club["range"]
         break

      # Hit

      input("Press Enter to start swing...")
      t = time.time()
      input("Press Enter to end swing...")
      time_taken = round(time.time() - t, 2)
      print("You held it for", time_taken, "seconds")

      strokes += 1
      result, new_dist = get_outcome(lie, club, dist,time_taken)

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


# we will turn this into a loop to be able to play any hole
# RIGHT NOW THIS ONLY WORKS ONCE
play_hole(hole_idx=1, total_strokes=0, total_par=0)

#call function choosing club, in the rough, on a 200 yard hole

# shot = get_outcome("rough",CLUBS[3], 200)
# outcome_lie = shot[0]
# dist_remaining = shot[1]
# print(f'\n You are in the {outcome_lie} and you have {dist_remaining} yards remaining!')
# print(draw_bar(dist_remaining,200) + '\n')
