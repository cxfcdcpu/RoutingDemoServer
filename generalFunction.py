import math
from numba import jit
def pointToLineDis(x1,y1,x2,y2,x0,y0):
    return abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/math.sqrt((y2-y1)**2+(x2-x1)**2)
    
def pointToLineDisTup(p1,p2,x0,y0):
    x1=p1[0]
    x2=p2[0]
    y1=p1[1]
    y2=p2[1]
    return abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/math.sqrt((y2-y1)**2+(x2-x1)**2)
    
def archArea(radius,dis):
    return radius**2*math.acos(dis/radius)-dis*math.sqrt(radius**2-dis**2)
    

   
def euDis(c1,c2):
    return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    
def lineAngleRad(c1,c2):
    y=c2[1]-c1[1]
    x=c2[0]-c1[0]
    if x==0 and y==0:
        return 0
    res=math.atan2(y,x)
    return -res
        
def radToDeg(rad):
    return rad*180/math.pi

def lineAngle(c1,c2):
    return radToDeg(lineAngleRad(c1,c2))
        
        
    
