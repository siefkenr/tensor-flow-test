# Snake Tutorial Python
import state
import pygame
import tkinter as tk
from tkinter import messagebox
import copy
from keras import models
from keras import layers
from keras.optimizers import Adam
from collections import deque
import random
import numpy as np


class SnakeAgent:
    def __init__(self):
            self.gamma = 0.99

            self.epsilon = 1
            self.epsilon_decay = 0.05

            self.epsilon_min = 0.01

            self.learingRate = .4

            self.replayBuffer = deque(maxlen=10000)
            self.trainNetwork = self.createNetwork()

            self.episodeNum = 400

            self.iterationNum = 201  # max is 200

            self.numPickFromBuffer = 25

            self.targetNetwork = self.createNetwork()

            self.targetNetwork.set_weights(self.trainNetwork.get_weights())
    def createNetwork(self):
        model = models.Sequential()
        state_shape = (400,)

        model.add(layers.Dense(24, activation='relu', input_shape=(400,)))
        model.add(layers.Dense(48, activation='relu'))
        model.add(layers.Dense(48, activation='relu'))
        model.add(layers.Dense(48, activation='relu'))
        model.add(layers.Dense(48, activation='relu'))
        model.add(layers.Dense(3, activation='linear'))
        # model.compile(optimizer=optimizers.RMSprop(lr=self.learingRate), loss=losses.mean_squared_error)
        model.compile(loss='mse', optimizer=Adam(lr=self.learingRate))
        return model
    def getBestAction(self, state):

        self.epsilon = max(self.epsilon_min, self.epsilon)

        if np.random.rand(1) < self.epsilon:
            action = np.random.randint(0, 3)
        else:
            action = np.argmax(self.trainNetwork.predict(state))
        #print(action)
        return action
    def trainFromBuffer_Boost(self):
        if len(self.replayBuffer) < self.numPickFromBuffer:
            return
        samples = random.sample(self.replayBuffer, self.numPickFromBuffer)
        npsamples = np.array(samples)
        states_temp, actions_temp, rewards_temp, newstates_temp, dones_temp = np.hsplit(npsamples, 5)
        states = np.concatenate((np.squeeze(states_temp[:])), axis=0)
        rewards = rewards_temp.reshape(self.numPickFromBuffer, ).astype(float)
        targets = self.trainNetwork.predict(states)
        newstates = np.concatenate(np.concatenate(newstates_temp))
        dones = np.concatenate(dones_temp).astype(bool)
        notdones = ~dones
        notdones = notdones.astype(float)
        dones = dones.astype(float)
        Q_futures = self.targetNetwork.predict(newstates).max(axis=1)
        targets[(np.arange(self.numPickFromBuffer),
                 actions_temp.reshape(self.numPickFromBuffer, ).astype(int))] = rewards * dones + (
                    rewards + Q_futures * self.gamma) * notdones
        self.trainNetwork.fit(states, targets, epochs=1, verbose=0)

    def trainFromBuffer(self):
        if len(self.replayBuffer) < self.numPickFromBuffer:
            return

        samples = random.sample(self.replayBuffer, self.numPickFromBuffer)
        #print(self.replayBuffer)
        states = []
        newStates = []
        for sample in samples:

            state, action, reward, new_state, done = sample
            #print(new_state)
            states.append(state)
            newStates.append(new_state)

        newArray = np.array(states)
        states = newArray.reshape(self.numPickFromBuffer, 400)

        newArray2 = np.array(newStates)
        #print(newArray2)
        newStates = newArray2.reshape(self.numPickFromBuffer, 400)

        targets = self.trainNetwork.predict(states)
        new_state_targets = self.targetNetwork.predict(newStates)

        i = 0
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = targets[i]
            if done:
                target[action] = reward
            else:
                Q_future = max(new_state_targets[i])
                target[action] = reward + Q_future * self.gamma
            i += 1

        self.trainNetwork.fit(states, targets, epochs=5, verbose=0)

class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.sa = SnakeAgent()
        self.m = "right"

    def move(self, e, bm):
        for event in e:
            if event.type == pygame.QUIT:
                pygame.quit()

        if bm == "left":
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            self.m = "left"


        elif bm == "right":
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            self.m = "right"


        elif bm == "up":
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            self.m = "up"


        elif bm == "down":
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            self.m = "down"


        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)





def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)

    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 625
    rows = 25
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    s.addCube()
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    snack.pos = (5 , 5)
    flag = True
    clock = pygame.time.Clock()
    bodyList=[]
    f = 1
    eventList=[]
    pm = "right"
    rewardSum = 0
    done = False
    r = "right"
    reward = 0
    foodlist = [cube(randomSnack(rows, s), color=(0, 255, 0)),cube(randomSnack(rows, s), color=(0, 255, 0))]
    switch = True
    current_head = []
    t = 5
    y = 5
    while flag:
        pygame.time.delay(10)
        for event in pygame.event.get():
            eventList.append(event)
            #print(event)
        clock.tick(10)

        for x in range(len(s.body)):
            bodyList.append(s.body[x].pos)
        ns = state.futureState(s, s.m, pm)
        nextstate = state.state(ns, snack.pos)
        curstate = state.state(bodyList, snack.pos)
        current_head = bodyList[0]
        l = np.array(curstate)
        #print(l.reshape(1,400))
        r = s.sa.getBestAction(l.reshape(1,400))
        #print(r,"hi")
        if r == 0: #straight
            bm = pm

        elif r == 1: #right
            if pm == "right":
                bm = "down"
            elif pm == "down":
                bm = "left"
            elif pm == "left":
                bm = "up"
            elif pm == "up":
                bm = "right"
        elif r == 2: #left
            if pm == "right":
                bm = "up"
            elif pm == "down":
                bm = "right"
            elif pm == "left":
                bm = "down"
            elif pm == "up":
                bm = "left"
        #print(state.state(nextstate, snack.pos))
        #print(bm)

        s.move(eventList,bm)
        print(s.m)
        ns = state.futureState(s, s.m, pm)
        nextstate = state.state(ns, snack.pos)
        #print(s.m)
        if s.body[0].pos == snack.pos:
            s.addCube()

            t += 1
            if t > 20:
                t = 0
                y += 1
            snack.pos = (t, y)
            reward += 1

            #curstate = state.state(bodyList, snack.pos)

        for x in range(len(s.body)):
            #print(s.body[0].pos[0], snack.pos[0])
            if s.body[0].pos[0] == -1 or\
                    s.body[0].pos[1] == -1 or\
                    s.body[0].pos[1] == rows or\
                    s.body[0].pos[0] == rows or\
                    s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                #print('Score: ', len(s.body))
                #message_box('You Lost!', 'Play again...')
                reward -= 1
                s.sa.replayBuffer.append([curstate, r, reward, nextstate, done])
                s.sa.trainFromBuffer()
                #snack.pos = (random.randrange(rows), random.randrange(rows))
                s.reset((10, 10))
                break

        reward = state.reward(current_head, ns[0], snack.pos)
        #print(nextstate)
        s.sa.replayBuffer.append([curstate, r, reward, nextstate, done])
        s.sa.trainFromBuffer()

        #nextstate= state.futureState(s, "right","right")

        paststate = curstate
        redrawWindow(win)
        if f == 1:
            f = 0
            s.reset((10,10))
            redrawWindow(win)
        bodyList = []
        #print(s.body[0].pos)
        #print(curstate)
            #print(s.body[x].pos)

        bodyList = []
        eventList=[]
        rewardSum += reward
        #print(rewardSum)
        pm = s.m

        s.sa.epsilon -= s.sa.epsilon_decay
main()

