import random
import time
import sys


#------------------------------------全局变量
NAME = ''
VERTICES = 0
DEPOT = 0
REQUIRED_EDGES = 0
Required = []
NON_REQUIRED_EDGES = 0
VEHICLES = 0
CAPACITY = 0
TOTAL_COST_OF_REQUIRED_EDGES = 0
MAX = 99999
dijk = []
#------------------------------------全局变量
def read(filepath):
    file = open(filepath,"r",encoding= "utf-8")
    global NAME, VERTICES, DEPOT, Required,REQUIRED_EDGES, REQUIRED_EDGES, NON_REQUIRED_EDGES, VEHICLES, CAPACITY, TOTAL_COST_OF_REQUIRED_EDGES
    for i in range(0,9):
        line = file.readline().split()
        if line[0] == 'NAME':
            NAME = line[2]
            print('NAME',NAME)
        elif line[0] == 'VERTICES':
            VERTICES = int(line[2])
            print ('VERTICES', VERTICES)
        elif line[0] == 'DEPOT':
            DEPOT = int(line[2])
            print ('DEPOT', DEPOT)
        elif line[0] == 'REQUIRED':
            REQUIRED_EDGES = int(line[3])
            print ('REQUIRED_EDGES', REQUIRED_EDGES)
        elif line[0] == 'NON-REQUIRED':
            NON_REQUIRED_EDGES = int(line[3])
            print ('NON_REQUIRED_EDGES', NON_REQUIRED_EDGES)
        elif line[0] == 'VEHICLES':
            VEHICLES = int(line[2])
            print ('VEHICLES', VEHICLES)
        elif line[0] == 'CAPACITY':
            CAPACITY = int(line[2])
            print ('CAPACITY', CAPACITY)
        elif line[0] == 'TOTAL':
            TOTAL_COST_OF_REQUIRED_EDGES = int(line[6])
            print ('TOTAL_COST_OF_REQUIRED_EDGES', TOTAL_COST_OF_REQUIRED_EDGES)

    datatable=[[(MAX,0) for j in range(VERTICES+1)] for j in range(VERTICES+1)]
    for i in range(0,REQUIRED_EDGES):
        line = file.readline ().split ()
        x = int(line[0])
        y = int(line[1])
        cost = int(line[2])
        demand = int(line[3])
        #print(x,y,cost,demand)
        datatable[x][y] = (cost,demand)
        datatable[y][x] = (cost, demand)
        Required.append((x,y))

    for i in range(REQUIRED_EDGES,REQUIRED_EDGES+NON_REQUIRED_EDGES):
        line = file.readline ().split ()
        x = int(line[0])
        y = int(line[1])
        cost = int(line[2])
        demand = int(line[3])
        #print(x,y,cost,demand)
        datatable[x][y] = (cost,demand)
        datatable[y][x] = (cost, demand)
    if file.readline () == 'END':
        print("Read successfully")
    return datatable

def Dijkstra(table, node):
    global NAME, VERTICES, DEPOT, Required,REQUIRED_EDGES, REQUIRED_EDGES, NON_REQUIRED_EDGES, VEHICLES, CAPACITY, TOTAL_COST_OF_REQUIRED_EDGES
    final = [0]*(VERTICES+1)
    distance = [0]*(VERTICES+1)
    path = [0]*(VERTICES+1)
    for i in range(1,VERTICES+1):
        distance[i] = table[node][i][0]
        if distance[i] != MAX:
            path[i] = node
        else:
            path[i] = MAX
    final[node] = 1
    path[node] = node
    k = 0
    for i in range(1,VERTICES+1):
        min = MAX
        for j in range(1,VERTICES+1):
            if distance[j] < min and final[j] == 0:
                min = distance[j]
                k = j
        final[k] = True
        for j in range (1, VERTICES + 1):
            if (distance[j] > min + table[k][j][0]) and final[j]==0:
                distance[j] = min + table[k][j][0]
                path[j] = k
    distance[node] = 0
    return distance

def getdijk():
    global dijk
    dijk.append (0)
    for i in range (1, VERTICES + 1):
        dijk.append (Dijkstra (table, i))
    #print (dijk)

def better(arcmin,arc,load,now):
    strategy = random.random()
    if strategy < 0.15:
        if dijk[arcmin[1]][DEPOT] > dijk[arc[1]][DEPOT]:
            return True
        else: return False
    elif strategy <0.3:
        if dijk[arcmin[1]][DEPOT] < dijk[arc[1]][DEPOT]:
            return True
        else:
            return False
    elif strategy < 0.6:##demand/cost
        if table[arcmin[0]][arcmin[1]][1]/(dijk[now][arcmin[0]]+table[arcmin[0]][arcmin[1]][0]) > table[arc[0]][arc[1]][1]/(dijk[now][arc[0]]+table[arc[0]][arc[1]][0]):
            return True
        else:
            return False
    elif strategy < 0.7:
        if table[arcmin[0]][arcmin[1]][1]/(dijk[now][arcmin[0]]+table[arcmin[0]][arcmin[1]][0]) < table[arc[0]][arc[1]][1]/(dijk[now][arc[0]]+table[arc[0]][arc[1]][0]):
            return True
        else:
            return False
    elif strategy < 1:
        if load < CAPACITY / 2 and dijk[arcmin[1]][DEPOT] > dijk[arc[1]][DEPOT]:
            return True
        elif load > CAPACITY / 2 and dijk[arcmin[1]][DEPOT] < dijk[arc[1]][DEPOT]:
            return True
        else:
            return False
def pathscan(table):
    global NAME, VERTICES, DEPOT, Required,REQUIRED_EDGES, REQUIRED_EDGES, NON_REQUIRED_EDGES, VEHICLES, CAPACITY, TOTAL_COST_OF_REQUIRED_EDGES, dijk
    depot = DEPOT
    free = Required.copy()
    #print(Required)
    k = -1
    Route = []
    load = []
    cost = []
    #print(free)
    total = 0 #cost
    while len(free) != 0:
        k += 1
        Route.append(0)
        load.append(0)
        cost.append(0)
        now = depot
        Route[k] = []
        arc = (0,0)
        while True:
            d = MAX
            index = 0
            q = 0
            for i in range(0,len(free)):
                aa = free[i]
                #print(load[k])
                if load[k] + table[aa[0]][aa[1]][1] <= CAPACITY:
                    if dijk[now][aa[0]] <= dijk[now][aa[1]]:
                        dmin = dijk[now][aa[0]]
                        arcmin = (aa[0],aa[1])
                    else:
                        dmin = dijk[now][aa[1]]
                        arcmin = (aa[1],aa[0])
                    if dmin < d :
                        d = dmin
                        q = table[aa[0]][aa[1]][1]
                        arc = arcmin
                        index = i
                    elif dmin <= d+7:
                        #arc 为之前的解， arrcmin是当前需better的
                        if better(arcmin,arc,load[k],now):
                            arc = arcmin
                            q = table[aa[0]][aa[1]][1]
                            d = dmin
                            index = i

            if d!= MAX:
                # 啊哈哈哈哈我独创的剪枝方法 王之释放你的所有潜力！
                #if dijk[now][arc[0]] == dijk[now][depot] + dijk[depot][arc[0]] and dijk[now][depot]!=0 and dijk[depot][arc[0]]!=0:
                #   break
                #else:
                    now = arc[1]
                    Route[k].append(arc)
                    #print (free[index])
                    free.pop(index)
                    load[k] += q
                    cost[k] += d + table[arc[0]][arc[1]][0]


                #if cost[k] >= (2*CAPACITY)/3:
                #    yunqi = random.random()
                #    if yunqi > 0.8 and dijk[now][depot] > dijk[arc[0]][depot]:
                #        break
            else:
                break
            #print ("?", free)
        cost[k] += dijk[Route[k][len(Route[k])-1][1]][depot]
        total += cost[k]
    return Route, total

def printformat(Route, totalcost):
    s = ''
    for i in range(len(Route)):
        s += '0,'
        for j in range(len(Route[i])):
            s += '('+ str(Route[i][j][0]) + ',' + str(Route[i][j][1]) + '),'
        s += '0'
        if i != len(Route) -1:
            s += ','
    print('s',s)
    print('q', totalcost)

def calCost(sont):
    cost = 0
    now = DEPOT
    for i in range(len(sont)):
        cost += dijk[now][sont[i][0]] + table[sont[i][0]][sont[i][1]][0]
        now = sont[i][1]
    cost += dijk[now][DEPOT]
    return cost

def calTT(solution):
    cost = 0
    for i in range(len(solution)):
        cost += calCost(solution[i])
    return cost

if __name__ == '__main__':
    start = time.time()
    filepath = '/home/snwk/桌面/STUDY/AI/CARP/CARP_samples/egl-s1-A.dat'
    table = read(filepath)
    getdijk()
    Route, totalcost = pathscan (table)
    print(calTT(Route))
    for i in range(100):
        RouteT, totalcostT = pathscan(table)
        if totalcostT < totalcost:
            totalcost = totalcostT
            Route =RouteT
            print(i,totalcost)
            print(calTT(Route))

    printformat(Route, totalcost)
    end = time.time()
    print("THE END, total time is ", end - start)


#s 0,(1,116),(116,117),(117,2),(117,119),(118,114),(114,113),(113,112),(112,110),(110,107),(107,108),(107,112),0,0,(110,111),(107,106),(106,105),(105,104),(104,102),(66,67),(69,71),(71,72),(72,73),(73,44),(44,43),0,0,(108,109),(66,62),(62,63),(63,64),(64,65),(55,140),(140,49),0,0,(87,86),(86,85),(85,84),(84,82),(82,80),(80,79),(79,78),(78,77),(77,46),(46,43),(43,37),(37,36),(36,38),(38,39),(39,40),0,0,(124,126),(126,130),(68,67),(67,69),(44,45),(45,34),(34,139),(139,33),(33,11),(11,12),(12,13),(20,22),0,0,(95,96),(96,97),(97,98),(56,55),(55,54),(49,48),(11,27),(28,29),(30,32),(30,28),(28,27),(27,25),(25,24),(24,20),0,0,(11,8),(8,6),(6,5),(8,9),(13,14),0
#q 5876