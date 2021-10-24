from util import dists, colored, valid, add, delta
from colorama import Style, init
import random
import torch

init(convert = True)

class LITSboard:
    def __init__(self,seed=None):
        self.left = {"L": 5, "I": 5, "T": 5, "S": 5}
        self.played = []
        self.occupied = set()
        self.letters = {}
        self.moves = pieces
        self.X = set()
        self.O = set()
        if seed is None:
            while len(self.X) < 30:
                tup = (random.randint(0, 9), random.randint(0, 9))
                if tup not in self.X and tup not in self.O:
                    self.X.add(tup)
                    self.O.add((9 - tup[0], 9 - tup[1]))
        else:
            for i in range(10):
                for j in range(10):
                    if seed[i][j] == "X":
                        self.X.add((i, j))
                    elif seed[i][j] == "O":
                        self.O.add((i, j))
    def getseed(self):
        out = [[0] * 10 for i in range(10)]
        for guy in self.X:
            out[guy[0]][guy[1]] = "X"
        for guy in self.O:
            out[guy[0]][guy[1]] = "O"
        return out
    def query(self):
        m = input().split()
        ints = list(map(int, m[1:]))
        self.play(LITSpiece(m[0], (ints[0], ints[1]), (ints[2], ints[3]), (ints[4], ints[5]), (ints[6], ints[7])))
    def diff(self):
        out = 0
        for guy in self.X:
            if guy not in self.occupied:
                out += 1
        for guy in self.O:
            if guy not in self.occupied:
                out -= 1
        if len(self.played) % 2 == 1:
            out = -out
        return out
    def score(self):
        x = 0
        o = 0
        for guy in self.X:
            if guy not in self.occupied:
                x += 1
        for guy in self.O:
            if guy not in self.occupied:
                o += 1
        return (x, o)
    def vector(self, piece = None):
        out = [0.] * 200
        val = 1. if len(self.played) % 2 == 0 else -1.
        if piece is not None:
            val = -val
        for guy in self.X:
            out[10 * guy[0] + guy[1]] = val
        for guy in self.O:
            out[10 * guy[0] + guy[1]] = -val
        for guy in self.occupied:
            out[100 + 10 * guy[0] + guy[1]] = 1.
            out[10 * guy[0] + guy[1]] = 0.
        if piece is not None:
            for guy in piece.locs:
                out[100 + 10 * guy[0] + guy[1]] = 1.
                out[10 * guy[0] + guy[1]] = 0.
        return out
    def __repr__(self):
        let = []
        for i in range(10):
            let.append([0] * 10)
        for guy in self.X:
            let[guy[0]][guy[1]] = Style.RESET_ALL + "X"
        for guy in self.O:
            let[guy[0]][guy[1]] = Style.RESET_ALL + "O"
        for i in range(10):
            for j in range(10):
                if let[i][j] == 0:
                    let[i][j] = " "
        for piece in self.played:
            for loc in piece.locs:
                let[loc[0]][loc[1]] = colored[piece.let]
        for i in range(10):
            let[i] = " ".join(let[i])
        return "\n".join(let) + Style.RESET_ALL
    def play(self, piece, update=True):
        self.played.append(piece)
        self.occupied |= set(piece.locs)
        for guy in piece.locs:
            self.letters[guy] = piece.let
        self.left[piece.let] -= 1
        
        if update:
            if len(self.played) == 1:
                self.moves = enabled[tuple(piece.locs)]
            else:
                new = []
                for guy in self.moves:
                    if self.valid(guy):
                        new.append(guy)
                for guy in enabled[tuple(piece.locs)]:
                    if self.valid(guy):
                        new.append(guy)
                self.moves = new
    def goodmove(self,model):
        pos = [self.vector(guy) for guy in self.moves]
        out = model(torch.tensor(pos))
        sml = float('inf')
        move = None
        for i in range(len(pos)):
            if out[i].item() < sml:
                sml = out[i].item()
                move = self.moves[i]
                #print(move.locs,out[i].item())
        self.play(move)
        
    def valid(self,piece):
        if len(self.played) == 0:
            return True
        if self.left[piece.let] == 0:
            return False
        for guy in piece.locs:
            if guy in self.occupied:
                return False
        bad = True
        for i in range(4):
            for j in range(4):
                f = add(piece.locs[i], delta[j])
                if f in self.occupied:
                    if self.letters[f] == piece.let:
                        return False
                    bad = False
        if bad:
            return False
        check = set()
        for l in piece.locs:
            check.add(add(l, (-1, -1)))
            check.add(add(l, (-1, 0)))
            check.add(add(l, (0, -1)))
            check.add(l)
        a = self.occupied | set(piece.locs)
        for guy in check:
            if guy in a and add(guy, (0, 1)) in a and add(guy, (1, 0)) in a and add(guy, (1, 1)) in a:
                return False
        return True
    def legal(self):
        out = []
        for guy in pieces:
            if self.valid(guy):
                out.append(guy)
        return out

class LITSpiece:
    def __init__(self, let, z1, z2, z3, z4):
        self.let = let
        self.locs = sorted([z1, z2, z3, z4])
        lens = dists(self.locs)
        if let == "L":
            if lens != [1, 1, 1, 2, 4, 5]:
                raise ValueError
        elif let == "I":
            if lens != [1, 1, 1, 4, 4, 9]:
                raise ValueError
        elif let == "T":
            if lens != [1, 1, 1, 2, 2, 4]:
                raise ValueError
        elif let == "S":
            if lens != [1, 1, 1, 2, 2, 5]:
                raise ValueError
        else:
            raise ValueError
    def __eq__(self, piece):
        if self.locs == piece.locs:
            return True
        return False
    def sim(self, pieces):
        a = len(pieces)
        tot = 0
        for guy in pieces:
            same = 0
            for boi in guy.locs:
                if boi in self.locs:
                    same += 1
            tot += same * same / 10
        return tot / a

def piecegen(): #generates list of all possible piece locations
    Ls = []
    Is = []
    Ts = []
    Ss = []
    # find pieces which can be a represented as a path of four cells
    for x in range(10):
        for y in range(10):
            for a in range(4):
                for b in range(4):
                    for c in range(4):
                        z1 = (x , y)
                        z2 = add(z1, delta[a])
                        z3 = add(z2, delta[b])
                        z4 = add(z3, delta[c])
                        if valid(z2) and valid(z3) and valid(z4):
                            lens = dists([z1, z2, z3, z4])
                            if lens == [1, 1, 1, 2, 4, 5]:
                                Ls.append(tuple(sorted([z1, z2, z3, z4])))
                            elif lens == [1, 1, 1, 4, 4, 9]:
                                Is.append(tuple(sorted([z1, z2, z3, z4])))
                            elif lens == [1, 1, 1, 2, 2, 5]:
                                Ss.append(tuple(sorted([z1, z2, z3, z4])))
    # find other pieces (only Ts)
    for x in range(10):
        for y in range(10):
            for a in range(4):
                nums = [0, 1, 2, 3]
                nums.remove(a)
                z1 = (x, y)
                z2 = add(z1, delta[nums[0]])
                z3 = add(z1, delta[nums[1]])
                z4 = add(z1, delta[nums[2]])
                if valid(z2) and valid(z3) and valid(z4):
                    lens = dists([z1, z2, z3, z4])
                    if lens == [1, 1, 1, 2, 2, 4]:
                        Ts.append(tuple([z1, z2, z3, z4]))
    Ls = set(Ls)
    Is = set(Is)
    Ts = set(Ts)
    Ss = set(Ss)
    pieces = []
    for guy in Ls:
        pieces.append(LITSpiece("L", guy[0], guy[1], guy[2], guy[3]))
    for guy in Is:
        pieces.append(LITSpiece("I", guy[0], guy[1], guy[2], guy[3]))
    for guy in Ts:
        pieces.append(LITSpiece("T", guy[0], guy[1], guy[2], guy[3]))
    for guy in Ss:
        pieces.append(LITSpiece("S", guy[0], guy[1], guy[2], guy[3]))
    return pieces

def enabledgen(): #finds possible second moves for each first move
    enabled = {}
    for piece in pieces:
        a = LITSboard()
        a.play(piece, False)
        enabled[tuple(piece.locs)] = a.legal()
    return enabled

pieces = piecegen()
enabled = enabledgen()