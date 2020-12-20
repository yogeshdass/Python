from math import sqrt 

def find_dist(x1,y1, x2,y2):
    return sqrt((x1-x2)^2 + (y1-y2)^2)

if __name__ == "__main__":
    print(find_dist(x1=4,y1=3,x2=2,y2=1))
