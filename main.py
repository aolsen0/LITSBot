from LITSclass import *
from LITSnode import LITSnode
import time

model1 = torch.load('model1.pt')
model2 = torch.load('model2.pt')
model3 = torch.load('model3.pt')
model4 = torch.load('model4.pt')
model5 = torch.load('model5.pt')
model6 = torch.load('model6.pt')

models = [model1, model2, model3, model4, model5, model6]
even = models[1::2]
odd = models[::2]

seed = None
s = input()
if s == "i":
    seed = []
    for i in range(10):
        seed.append(input())
if seed is not None:
    a = LITSboard(seed)
else:
    a = LITSboard()
    

while len(a.moves) > 0:
    print(a)
    s = input()
    if s == "i":
        a.query()
        print("-------------------")
    elif s[0] == "g":
        t = int(s[2:])
        r = LITSnode(a,None,None,None,even,odd,True)
        start = time.time()
        if len(a.played) == 0:
            d = 0
            r.birth()
            r.children.sort(key = lambda x: abs(x.value))
            #for i in range(30):
                #print(r.children[i].pieces[-1].locs,r.children[i].value)
            while time.time() < start + t and d < 15:
                d += 1
                for i in range(30):
                    r.children[i].alphabeta(d, -float('inf'), float('inf'), source = True)
                #print(d,[round(r.children[i].value,3) for i in range(30)])
            #for i in range(30):
                #print(r.children[i].pieces[-1].locs,r.children[i].value)
            sml = float('inf')
            move = None
            for guy in r.children[:30]:
                if abs(guy.value) < sml:
                    sml = abs(guy.value)
                    move = guy.pieces[-1]
            a.play(move)
        else:
            d = 0
            while time.time() < start + t and d < 15:
                d += 1
                #print(d,
                r.alphabeta(d, -float('inf'), float('inf'), source = True)
            a.play(r.fave())
        print('-------------------')
    elif s[0] == "e":
        t = int(s[2:])
        r = LITSnode(a, None, None, None, even, odd, True)
        start = time.time()
        d = 0
        while time.time() < start + t and d < 15:
            d += 1
            #print(d,
            r.alphabeta(d, -float('inf'), float('inf'), source = True)
        print(r.value)
        print(r.fave().locs)
    elif s[0] == "p":
        r = LITSnode(a, None, None, None, even, odd, True)
        r.birth()
        for guy in r.children[:16]:
            print(guy.pieces[-1].locs, guy.value)
    elif s[0] == "c":
        print(len(a.moves))
    elif s[0] == "q":
        r = LITSnode(a, None, None, None, even, odd, True)
        r.birth()
        nice = [r.children[0]]
        inds = [0]
        pieces = [r.children[0].pieces[-1]]
        best = r.children[0].value
        for _ in range(9):
            x = 1 / (_ + 1)
            good = False
            for i in range(len(r.children)):
                if i in inds:
                    continue
                if r.children[i].value - best < x or r.children[i].pieces[-1].sim(pieces) < x:
                    good = True
                    inds.append(i)
                    pieces.append(r.children[i].pieces[-1])
                    nice.append(r.children[i])
                    break
            if not good:
                break
        print(inds)
        for guy in nice:
            print(guy.pieces[-1].locs, guy.value)
print(a)
print(a.diff())