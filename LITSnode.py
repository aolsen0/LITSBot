from LITSclass import LITSboard
import torch
from util import *


class LITSnode:
    def __init__(self, root, parent, val, piece, even, odd, isroot = False):
        self.root = root
        self.parent = parent
        self.legal = []
        self.pieces = parent.pieces[:] if not isroot else root.played[:]
        if not isroot:
            self.pieces.append(piece)
        self.children = []
        self.updated = False
        self.value = val
        self.even = even
        self.odd = odd
    def birth(self):
        self.updated = True
        b = LITSboard(self.root.getseed())
        if self.parent is not None:
            for guy in self.pieces[:-1]:
                b.play(guy,False)
            b.moves = self.parent.legal
            b.play(self.pieces[-1])
        else:
            for guy in self.pieces:
                b.play(guy,False)
            b.moves = self.root.moves
        if len(b.moves) == 0:
            self.value = b.diff()
        else:
            self.legal = []
            seen = set()
            for guy in b.moves:
                a = tuple(guy.locs)
                if a not in seen:
                    seen.add(a)
                    self.legal.append(guy)
            vectors = torch.tensor([b.vector(move) for move in self.legal])
            # choose appropriate models for use
            x = self.odd[min(len(self.odd) - 1, max(0, (12 - len(self.pieces)) // 2))]
            y = self.even[min(len(self.even) - 1, max(0, (11 - len(self.pieces)) // 2))]
            vals1 = x(vectors)
            vals2 = y(vectors)
            self.children = []
            for i in range(len(self.legal)):
                self.children.append(LITSnode(self.root, self, (vals1[i].item() + vals2[i].item()) / 2, self.legal[i], self.even, self.odd))
            self.children.sort(key = lambda x : x.value)
    def fave(self):
        best = float('inf')
        move = None
        if len(self.nice) > 0:
            l = self.nice
        else:
            cut = max(10, 900 // len(self.children))
            l = self.chidlren[:cut]
        for guy in l:
            if guy.value < best:
                best = guy.value
                move = guy.pieces[-1]
        return move
    def alphabeta(self, depth, alpha, beta, cut=None, skip=True, source=False, normal=True):
        if depth == 0:
            return self.value
        if not self.updated:
            self.birth()
        if len(self.children) == 0:
            x = 30
            o = 30
            for guy in self.pieces:
                for boi in guy.locs:
                    if boi in self.root.X:
                        x -= 1
                    elif boi in self.root.O:
                        o -= 1
            d = x - o
            if len(self.pieces) % 2 == 1:
                d = -d
            if d == 0:
                d = -.9
            return d
        val =- float('inf')
        if cut is None:
            cut = max(10, 900 // len(self.children))
        if normal and cut < len(self.children):
            self.nice = [self.children[0]]
            inds = [0]
            pieces = [self.children[0].pieces[-1]]
            best = self.children[0].value
            for _ in range(cut - 1):
                x = 1 / (_ + 1)
                good = False
                for i in range(len(self.children)):
                    if i in inds:
                        continue
                    if self.children[i].value - best < x or self.children[i].pieces[-1].sim(pieces) < x:
                        good = True
                        inds.append(i)
                        pieces.append(self.children[i].pieces[-1])
                        self.nice.append(self.children[i])
                        break
                if not good:
                    break
            i = 0
            while len(self.nice) < cut and i < len(self.children):
                if i not in inds:
                    self.nice.append(self.children[i])
                i += 1
        else:
            self.nice = self.children[:cut]
        for child in self.nice:
            x = child.alphabeta(depth - 1, -beta, -alpha)
            val = max(val, -x)
            alpha = max(val, alpha)
            if alpha > beta and skip:
                break
        self.value = val
        if not source:
            self.children = []
            self.nice = []
            self.updated = False
        return val