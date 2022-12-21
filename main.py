import socket
from _thread import *
import random
import _pickle as pickle
import time
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import datetime

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
PORT = 1512
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)
_id = 0
width, height = 15, 15
howmanydogs = 3
dogs = []
players = []
holes = []
dogpos = []
dogrichtungen = []
start = False
connections = 0
finaltime = -1

try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print(f"[{datetime.datetime.now()}] Server could not start")
    quit()

S.listen()  # listen for connections

print(f"[{datetime.datetime.now()}] Server Started with IP: {SERVER_IP}")


class timer:
    def __init__(self):
        self.startpoint = time.time()
        self.ispause = False

    def start(self):
        self.startpoint = time.time()

    def gettime(self):
        return time.time() - self.startpoint

    def pause(self):
        if not self.ispause:
            self.timeofpause = self.gettime()
            self.ispause = True

    def resume(self):
        if self.ispause:
            self.startpoint = time.time() - self.timeofpause
            self.ispause = False


class dog:
    def __init__(self):
        self.distance = 0
        matrixl = []
        self.richtung = 0
        row = 0
        self.shortestdistance = 100000
        self.anzahlrichtungen = 0
        self.fastrichtung = 0
        self.target = players[0]
        for i in range(int(len(l) / width)):
            matrixl.append(l[row:row + width])
            row += width
        for i in range(len(matrixl)):
            for j in range(len(matrixl[i])):
                matrixl[i][j] = 0 if matrixl[i][j] == "w" else 1

        grid = Grid(matrix=matrixl)
        while True:
            self.x = random.randint(0, width - 1) + 0.5
            self.y = random.randint(0, height - 1) + 0.5
            if l[int(self.x) + int(self.y) * height][0] == "p":
                break
        self.start = grid.node(int(self.x), int(self.y))
        self.end = grid.node(0, 0)
        self.path = []

    def pathfind(self):
        matrixl = []
        row = 0
        for i in range(int(len(l) / width)):
            matrixl.append(l[row:row + width])
            row += width
        for i in range(len(matrixl)):
            for j in range(len(matrixl[i])):
                matrixl[i][j] = 0 if matrixl[i][j] == "w" else 1
        grid = Grid(matrix=matrixl)
        self.start = grid.node(int(self.x), int(self.y))
        for player in players:
            self.end = grid.node(int(player.x), int(player.y))
            finder = AStarFinder()
            maybepath, self.distance = finder.find_path(self.start, self.end, grid)

            if self.distance < self.shortestdistance:
                self.shortestdistance = self.distance
                self.path = maybepath
                self.target = player

    def run(self):

        if len(self.path) != 0:
            if self.target.mousepoweractivated.gettime() > 45:

                geschw = 0.01

                self.fastrichtung = 0
                self.anzahlrichtungen = 0
                if self.x < int(self.path[0][0]) + 0.475:
                    self.fastrichtung += 3
                    self.anzahlrichtungen += 1
                    self.x += geschw
                if self.x > int(self.path[0][0]) + 0.525:
                    self.fastrichtung += 1
                    self.anzahlrichtungen += 1
                    self.x -= geschw
                if self.y < int(self.path[0][1]) + 0.475:
                    self.fastrichtung += 2
                    self.anzahlrichtungen += 1
                    self.y += geschw
                if self.y > int(self.path[0][1]) + 0.525:
                    self.fastrichtung += 0
                    self.anzahlrichtungen += 1
                    self.y -= geschw
                if int(self.y) == int(self.path[0][1]) and int(self.x) == int(self.path[0][0]) and not len(
                        self.path) == 0:
                    self.path.pop(0)
                if self.anzahlrichtungen != 0:
                    self.richtung = self.fastrichtung / self.anzahlrichtungen


speedruntimer = timer()
dogshowtimer = timer()


def maze(ms):
    visited_cells = []
    walls = []

    map = [['w' for _ in range(ms)] for _ in range(ms)]

    def check_neighbours(ccr, ccc):
        neighbours = [
            [ccr, ccc - 1, ccr - 1, ccc - 2, ccr, ccc - 2, ccr + 1, ccc - 2, ccr - 1, ccc - 1, ccr + 1, ccc - 1],
            # left
            [ccr, ccc + 1, ccr - 1, ccc + 2, ccr, ccc + 2, ccr + 1, ccc + 2, ccr - 1, ccc + 1, ccr + 1, ccc + 1],
            # right
            [ccr - 1, ccc, ccr - 2, ccc - 1, ccr - 2, ccc, ccr - 2, ccc + 1, ccr - 1, ccc - 1, ccr - 1, ccc + 1],  # top
            [ccr + 1, ccc, ccr + 2, ccc - 1, ccr + 2, ccc, ccr + 2, ccc + 1, ccr + 1, ccc - 1, ccr + 1,
             ccc + 1]]  # bottom
        visitable_neighbours = []
        for i in neighbours:  # find neighbours to visit
            if i[0] > 0 and i[0] < (ms - 1) and i[1] > 0 and i[1] < (ms - 1):
                if map[i[2]][i[3]] == 'p' or map[i[4]][i[5]] == 'p' or map[i[6]][i[7]] == 'p' or map[i[8]][
                    i[9]] == 'p' or map[i[10]][i[11]] == 'p':
                    walls.append(i[0:2])
                else:
                    visitable_neighbours.append(i[0:2])
        return visitable_neighbours

    # StartingPoint

    scr = random.randint(1, ms - 1)
    scc = random.randint(1, ms - 1)
    ccr, ccc = scr, scc
    map[scr][scc] = "p"

    finished = False
    while not finished:
        visitable_neighbours = check_neighbours(ccr, ccc)
        if len(visitable_neighbours) != 0:
            d = random.randint(1, len(visitable_neighbours)) - 1
            ncr, ncc = visitable_neighbours[d]
            map[ncr][ncc] = 'p'
            visited_cells.append([ncr, ncc])
            ccr, ccc = ncr, ncc
        if len(visitable_neighbours) == 0:
            try:
                ccr, ccc = visited_cells.pop()
            except:
                finished = True

    for i in range(int(len(map[0]))):
        map[0][i] = "w"

    for i in range(len(map[-1])):
        map[-1][i] = "w"

    for i in range(len(map)):
        map[i][0] = "w"
        map[i][-1] = "w"

    maze = []

    for i in range(len(map)):
        maze += map[i]
    return maze


def doeselementinlistexist(list, index):
    try:
        if list[index]:
            return True
    except:
        return False


class playermultiplayer():
    def __init__(self, id, name):
        self.richtung = 0

        self.mousepoweractivated = timer()
        self.mousepoweractivated.startpoint = 0
        self.dogshowtimer = timer()
        self.fat = 0
        self.id = id
        self.name = name
        self.x, self.y = 1,1
        self.startx, self.starty = 1,1
        self.dead = False

    def new_round(self):
        self.dead = False
        self.richtung = 0
        self.mousepoweractivated = timer()
        self.mousepoweractivated.startpoint = 0
        self.dogshowtimer = timer()
        self.fat = 0
        while True:
            self.startx = random.randint(0, width - 1) + 0.5
            self.starty = random.randint(0, height - 1) + 0.5
            self.x, self.y = self.startx, self.starty
            if l[int(self.x) + int(self.y) * height][0] == "p":
                break
    def run(self):
        if doeselementinlistexist(fish, 0):
            if fish[0] == int(self.x) + int(self.y) * height:
                fish.pop(0)
                self.fat += 3

        for i in range(len(mice)):
            if doeselementinlistexist(mice, i) and mice[i] == int(self.x) + int(self.y) * height:
                mice.pop(i)
                self.mousepoweractivated.start()


def reset():
    global fish, l, holes, mice, dogs, dogpos, dogrichtungen
    l = maze(15)
    fish = []
    paths = 0
    dogpos = []
    dogrichtungen = []
    for i in l:
        if i[0] == "p":
            paths += 1

    for i in range(min(paths, 5)):
        go = True
        while go:
            feld = random.randint(0, width * height - 1)
            if l[feld][0] == "p" and fish.count(feld) == 0:
                fish.append(feld)
                go = False

    holes = []

    for i in range(min(paths, 3)):
        go = True
        while go:
            feld = random.randint(0, width * height - 1)
            if l[feld][0] == "p" and fish.count(feld) == 0 and holes.count(feld) == 0:
                holes.append(feld)
                go = False

    mice = []

    for i in range(min(paths, 2)):
        go = True
        while go:
            feld = random.randint(0, width * height - 1)
            if l[feld][0] == "p" and fish.count(feld) == 0 and holes.count(feld) == 0 and mice.count(feld) == 0:
                mice.append(feld)
                go = False
    dogs = []
    for _ in range(howmanydogs):
        dogs.append(dog())
    for i in dogs:
        i.pathfind()


def getPlayerById(id):
    for i in players:
        if i.id == id:
            return i


def getPlayerIndexById(id):
    for i in range(len(players)):
        if players[i].id == id:
            return i

dogpos = []
dogrichtungen = []
def threaded_client(conn, _id,ipofplayer):
    global connections, players, start, fish, finaltime, dogpos, dogrichtungen

    current_id = _id
    data = conn.recv(64)
    name = data.decode("utf-8")
    print(f"[{datetime.datetime.now()}]", name, "["+ipofplayer+"] connected to the server.")
    players.append(playermultiplayer(_id, name))
    if start:
        conn.send(pickle.dumps((0, players, current_id, l, speedruntimer.gettime(), dogs, holes, fish)))
    else:
        conn.send(pickle.dumps((2, players, finaltime)))

    while True:

        if start:
            if current_id == players[0].id:
                if len(fish) != 0:

                    if dogshowtimer.gettime() > 5:
                        dogpos = []
                        dogrichtungen = []
                        dogshowtimer.start()
                        for i in dogs:
                            dogpos.append([i.x, i.y])
                            dogrichtungen.append(i.richtung)
                    for i in dogs:
                        i.pathfind()
                    if speedruntimer.gettime() > 10:
                        for i in dogs:
                            i.run()

                else:
                    start = False
            if len(fish) != 0:
                getPlayerById(current_id).run()
            else:
                finaltime = speedruntimer.gettime()
                start = False
        try:
            # Recieve data from client
            data = conn.recv(1024)

            if not data:
                break

            data = data.decode("utf-8")
            #print("[DATA] Recieved", data, "from client id:", current_id)
            if start:
                # look for specific commands from recieved data
                if data.split(" ")[0] == "dead":
                    getPlayerById(current_id).dead = True
                if data.split(" ")[0] == "update":
                    split_data = data.split(" ")
                    getPlayerById(current_id).x = float(split_data[1])
                    getPlayerById(current_id).y = float(split_data[2])
                    getPlayerById(current_id).richtung = float(split_data[3])
                    getPlayerById(current_id).fat = float(split_data[4])
                    getPlayerById(current_id).mousepoweractivated.startpoint = float(split_data[5])



                # any other command just send back list of players
                send_data = pickle.dumps((0, players, current_id, l, speedruntimer.gettime(), dogs, dogpos, dogrichtungen, holes, fish, mice))
            else:
                if data.split(" ")[0] == "start":
                    print(f"[{datetime.datetime.now()}]", name, "["+ipofplayer+"] started the game.")

                    reset()
                    for i in players:
                        i.new_round()
                    speedruntimer.start()
                    start = True
                    send_data = pickle.dumps((1, players, current_id, l, 0, dogs, dogpos, dogrichtungen, holes, fish))

                else:
                    send_data = pickle.dumps((2, players, finaltime))

            # send data back to clients
            conn.send(send_data)

        except Exception as e:
            print(e)
            break  # if an exception has been reached disconnect client

        time.sleep(0.001)

    # When user disconnects
    print(f"[{datetime.datetime.now()}] Name:", name, ", Client Id:", current_id, ", IP:",ipofplayer,"disconnected")

    connections -= 1
    del players[getPlayerIndexById(current_id)]
    conn.close()


print(f"[{datetime.datetime.now()}] Waiting for connections...")
l = maze(width)
while True:
    host, addr = S.accept()

    # increment connections start new thread then increment ids
    connections += 1
    start_new_thread(threaded_client, (host, _id,addr[0]))
    _id += 1

# when program ends
print(f"[{datetime.datetime.now()}] Server offline")
