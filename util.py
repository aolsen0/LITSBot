from colorama import Fore, init

init(convert = True)

def dist(a,b): #squared distance between two cells
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def dists(l): #list of squared distances between pairs of cells
    out=[]
    for i in range(len(l) - 1):
        for j in range(i + 1, len(l)):
            out.append(dist(l[i], l[j]))
    return sorted(out)

colored={"L": Fore.RED + "■", "I": Fore.MAGENTA + "■", "T": Fore.GREEN + "■", "S": Fore.BLUE + "■"}

def valid(loc): #checks if a cell is actually on the board
    if 0 <= loc[0] <= 9 and 0 <= loc[1] <= 9:
        return True
    return False

def add(x , y):
    return (x[0] + y[0], x[1] + y[1])

delta = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}