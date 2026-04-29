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

# Need a dictionary for the lies

#____________________________________________

# Helper functions

#lo,hi is range tuple from CLUBS dictionary
def rand(lo, hi):
    return random.randint(lo, hi)



# Shot function

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

    print('\n' + f'hit: {hit},  accuracy: {acc},  roll: {roll}\n')
    return new_dist, lie

#call function choosing 9 iron, in the rough, on a 200 yard hole
get_outcome("rough",CLUBS[4],200)






