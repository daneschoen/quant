"""
Strike: 10
If you knock down all 10 pins in the first shot of a frame, you get a strike.
How to score: A strike earns 10 points plus the sum of your next two shots.

Spare: 10
If you knock down all 10 pins using both shots of a frame, you get a spare.
How to score: A spare earns 10 points plus the sum of your next one-shot.

Open Frame
If you do not knock down all 10 pins using both shots of your frame (9 or fewer pins knocked down), you have an open frame.
How to score: An open frame only earns the number of pins knocked down.

The 10th Frame

If you roll a strike in the first shot of the 10th frame, you get 2 more shots.
If you roll a spare in the first two shots of the 10th frame, you get 1 more shot.
If you leave the 10th frame open after two shots, the game is over and you do not get an additional shot.
How to Score: The score for the 10th frame is the total number of pins knocked down in the 10th frame.

"""
def bowling(lst_frames):
    score = 0
    for i,frame in enumerate(lst_frames):
        if frame[0] == 10:
            score += 10
            score += frame[1] + frame[2]
        elif frame[0] + frame[1] == 10:
            score += 10
            score += frame[2]
        else:
            score += frame[0] + frame[1]
            if i == 9 and frame[0] + frame[1] < 10:
                return score

    return score

lst_frames = [(10,3,8), (3,7,6), (1,2), (1,2), (1,2),(10,10,10), (4,2), (1,0), (1,2), (1,2) ]
assert bowling(lst_frames) == sum([sum(x) for x in lst_frames])
