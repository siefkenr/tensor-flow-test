#import test

def state(snake,food):
    grid = []
    #print(snake)
    #print(food)
    count = 0
    for i in range(20):
        #print(i)
        apped = False
        for j in range(20):
            #print(i,j)
            for h in snake:
                if h[0] == i and h[1] ==j and not apped:
         #           print(i,j)
          #          print (h[0],h[1])
                    grid.append(1)
                    apped=True
            if food[0] == i and food[1] == j:
                if apped:
                    grid[count] = 2
                else:
                    grid.append(2)
            elif not apped:
                grid.append(0)
            count += 1
            apped = False
    return grid

def posibleMoves(head,firstbp):
    #print(head,firstbp)
    if head [0] == firstbp[0] and head[1] > firstbp[1]:
        pm = ["left", "right", "down"]
    elif head [0] == firstbp[0] and head[1] < firstbp[1]:
        pm = ["left", "right", "up"]
    elif head [1] == firstbp[1] and head[0] > firstbp[0]:
        pm = ["up", "right", "down"]
    elif head [1] == firstbp[1] and head[0] < firstbp[0]:
        pm = ["left", "up", "down"]
    else:
        pm = []
    #print (pm)
def futureState(s, move, past_move):
    newBody =[]
    for x in range(len(s.body)):
        if move == "up":
            if x == 0:
                newBody.append((s.body[0].pos[0], (s.body[0].pos[1] - 1)))
            else:
                if past_move == "up":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] - 1)))
                elif past_move == "right":
                    newBody.append(((s.body[x].pos[0] + 1), s.body[x].pos[1]))
                elif past_move == "down":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] + 1)))
                elif past_move == "left":
                    newBody.append(((s.body[x].pos[0] - 1), s.body[x].pos[1]))
        elif move == "right":
            if x == 0:
                newBody.append(((s.body[0].pos[0] + 1),s.body[0].pos[1]))
            else:
                if past_move == "up":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] - 1)))
                elif past_move == "right":
                    newBody.append(((s.body[x].pos[0] + 1), s.body[x].pos[1]))
                elif past_move == "down":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] + 1)))
                elif past_move == "left":
                    newBody.append(((s.body[x].pos[0] - 1), s.body[x].pos[1]))
        elif move == "down":
            if x == 0:
                newBody.append((s.body[0].pos[0], (s.body[0].pos[1] + 1)))
            else:
                if past_move == "up":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] - 1)))
                elif past_move == "right":
                    newBody.append(((s.body[x].pos[0] + 1), s.body[x].pos[1]))
                elif past_move == "down":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] + 1)))
                elif past_move == "left":
                    newBody.append(((s.body[x].pos[0] - 1), s.body[x].pos[1]))
        elif move == "left":
            if x == 0:
                newBody.append(((s.body[0].pos[0] - 1), s.body[0].pos[1]))
            else:
                if past_move == "up":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] - 1)))
                elif past_move == "right":
                    newBody.append(((s.body[x].pos[0] + 1), s.body[x].pos[1]))
                elif past_move == "down":
                    newBody.append((s.body[x].pos[0], (s.body[x].pos[1] + 1)))
                elif past_move == "left":
                    newBody.append(((s.body[x].pos[0] - 1), s.body[x].pos[1]))

    return newBody

def reward(shp, shf, food):
    r= 0
    #print(shp[0], food[0], shf[0]) # x higher towards right
    #print(shp[1], food[1], shf[1]) # y higher as it goes lower
    if abs(max(food[0],shp[0]) - min(shp[0],food[0])) < abs(max(food[0],shf[0]) - min(shf[0],food[0])):
        r = r - .1
    elif abs(max(food[0],shp[0]) - min(shp[0],food[0])) > abs(max(food[0],shf[0]) - min(shf[0],food[0])):
        r =r + 1
    elif abs(food[1] - shp[1]) > abs(food[1] - shf[1]):
        r = r + 1
    elif abs(food[1] - shp[1]) < abs(food[1] - shf[1]):
        r = r - .1
    print(r)
    return r