import math;
def getAngle(theta, proposedSpeed):
    x = math.sin(theta)*proposedSpeed
    y = math.cos(theta)*proposedSpeed

    return [x,y]