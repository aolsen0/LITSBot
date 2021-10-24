from LITSclass import *
from LITSnode import LITSnode
import torch
from torch.nn import Linear, ReLU
import torch.optim as optim

def train(its, opt, model, lfunc, example, cut):
    # Trains model to approximate the smallest possible value of example after one move on a given board
    # If example is an opponent objective function, model eventually approximates the current player's objective function
    test = []
    testres = []
    for i in range(50):
        a = LITSboard()
        while len(a.moves) > 0:
            test.append(a.vector())
            pos = [a.vector(guy) for guy in a.moves]
            vals = example(torch.tensor(pos))
            sml = float('inf')
            move = None
            for j in range(len(pos)):
                if vals[j].item() < sml:
                    sml = vals[j].item()
                    move = a.moves[j]
            testres.append([-sml])
            a.play(move)
        for j in range(cut):
            test.pop()
            testres.pop()
    test = torch.tensor(test)
    testres = torch.tensor(testres)
    for i in range(its):
        if i % 500 == 0:
            print(i, lfunc(model(test), testres), round(time.time()))
        real = []
        true = []
        for j in range(8):
            a = LITSboard()
            while len(a.moves) > 0:
                real.append(a.vector())
                pos = [a.vector(guy) for guy in a.moves]
                vals = example(torch.tensor(pos))
                sml = float('inf')
                move = None
                for j in range(len(pos)):
                    if vals[j].item() < sml:
                        sml = vals[j].item()
                        move = a.moves[j]
                true.append([-sml])
                a.play(move)
            for k in range(cut):
                real.pop()
                true.pop()
        opt.zero_grad()
        pred = model(torch.tensor(real))
        loss = lfunc(pred,torch.tensor(true))
        loss.backward()
        opt.step()
    print(i, lfunc(model(test), testres), round(time.time()))

def deepen(old_name, new_name, layers, its, depth):
    # Creates model to approximate the value of the position after depth optimal moves are played
    # requires model which approximates value of position after depth-1 optimal moves are played.
    old_model = torch.load(old_name + '.pt')
    new_model = torch.nn.Sequential(*layers)
    lfunc = torch.nn.MSELoss()
    optimizer = optim.Adam(new_model.parameters(), lr = .002)
    train(its, optimizer, new_model, lfunc, old_model, depth - 1)
    torch.save(new_model, new_name + '.pt')

'''
Example usage:
layers = [Linear(200,200),ReLU(),Linear(200,200),ReLU(),Linear(200,200),ReLU(),Linear(200,200),ReLU(),Linear(200,200),ReLU(),Linear(200,200),ReLU(),Linear(200,1)]
deepen('model5', 'model6', layers, 10000, 6)
'''


# Code for training the first model (not based on an example model, but rather on the true value of the position):

#test=[]
#testres=[]
#for i in range(50):
#    a=LITSboard()
#    while len(a.moves)>0:
#        test.append(a.vector())
#        d=a.diff()
#        val=2*(len(a.played)%2)-1
#        best=-float("inf")
#        move=None
#        for guy in a.moves:
#            change=0
#            for place in guy.locs:
#                if place in a.X:
#                    change+=val
#                if place in a.O:
#                    change-=val
#            if change>best:
#                best=change
#                move=guy
#        a.play(move)
#        testres.append([float(d+best)])
#test=torch.tensor(test)
#testres=torch.tensor(testres)
#
#xs=[]
#losses=[]
#
#for i in range(50000):
#    if i%10==0 and i>1990:
#        xs.append(i)
#        losses.append(lfunc(model(test),testres))
#        if i%5000==0:
#            plt.plot(xs,losses)
#            plt.show()
#    if i%500==0:
#        print(i)
#        print(lfunc(model(test),testres))
#    real=[]
#    true=[]
#    for j in range(8):
#        a=LITSboard()
#        while len(a.moves)>0:
#            real.append(a.vector())
#            d=a.diff()
#            val=2*(len(a.played)%2)-1
#            best=-float("inf")
#            move=None
#            for guy in a.moves:
#                change=0
#                for place in guy.locs:
#                    if place in a.X:
#                        change+=val
#                    if place in a.O:
#                        change-=val
#                if change>best:
#                    best=change
#                    move=guy
#            a.play(move)
#            true.append([float(d+best)])
#    optimizer.zero_grad()
#    predictions=model(torch.tensor(real))
#    loss=lfunc(predictions,torch.tensor(true))
#    loss.backward()
#    optimizer.step()
#    
#torch.save(model,"model1.pt")