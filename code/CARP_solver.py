import random
import time
import sys
import multiprocessing as mp
import copy
import _thread
import numpy as np
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
table = []
TIME = 0
SEED = 0
filepath = ''
#------------------------------------全局变量
def read(filepath):
    file = open(filepath,"r",encoding= "utf-8")
    global NAME, VERTICES, DEPOT, Required,REQUIRED_EDGES, REQUIRED_EDGES, NON_REQUIRED_EDGES, VEHICLES, CAPACITY, TOTAL_COST_OF_REQUIRED_EDGES
    for i in range(0,9):
        line = file.readline().split()
        #print(line)
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
    global dijk
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
    depot = DEPOT
    free = copy.deepcopy(Required)
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
            #nealestack = (0,0)
            #minack = MAX
            #for item in free:
            #    if dijk[now][item[0]] < minack or dijk[now][item[1]] < minack:
            #        minack = min(dijk[now][item[0]],dijk[now][item[1]])
            #        nealestack = item
            d = MAX
            index = -1
            q = 0
            r = random.random()
            #print(r)
            if r < 0.5 and len(Route[k]) == 0:
                if len(free) == 0:
                    break
                rr = int(random.random()*(len(free)))
                aa = free[rr]
                #print(rr,len(free)-1)
                if load[k] + table[aa[0]][aa[1]][1] <= CAPACITY:
                    if dijk[now][aa[0]] <= dijk[now][aa[1]]:
                        dmin = dijk[now][aa[0]]
                        arcmin = (aa[0],aa[1])
                    else:
                        dmin = dijk[now][aa[1]]
                        arcmin = (aa[1],aa[0])
                    d = dmin
                    q = table[aa[0]][aa[1]][1]
                    arc = arcmin
                    index = rr
            else:
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
                       elif dmin == d :
                           #arc 为之前的解， arrcmin是当前需better的
                           if better(arcmin,arc,load[k],now):
                               arc = arcmin
                               q = table[aa[0]][aa[1]][1]
                               d = dmin
                               index = i

            if d!= MAX:
                # 啊哈哈哈哈我独创的剪枝方法 王之释放你的所有潜力！
                if dijk[now][arc[0]] == dijk[now][depot] + dijk[depot][arc[0]] and dijk[now][depot]!=0 and dijk[depot][arc[0]]!=0:
                   break
                else:
                    #print("nealestack",nealestack,"arc",arc)
                    #if nealestack != arc and (nealestack[1],nealestack[0]) != arc:
                    #    break
                    now = arc[1]
                    Route[k].append(arc)
                    #print (free[index])
                    if index != -1:
                        free.pop(index)
                    load[k] += q
                    cost[k] += d + table[arc[0]][arc[1]][0]
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
        if type(Route[i]) != list:
            Route[i]=[Route[i]]
        for j in range(len(Route[i])):
            s += '('+ str(Route[i][j][0]) + ',' + str(Route[i][j][1]) + '),'
        s += '0'
        if i != len(Route) -1:
            s += ','
    print('s',s)
    print('q', totalcost)

#----------------MEANS
### ---


def initialization(startt,CAPACITYt, bestpop, Requiredt, tablet, dijkt,TIMEt,DEPOTt,SEEDt):
    global CAPACITY, Required, table, dijk,TIME,DEPOT,SEED
    start = startt
    CAPACITY = CAPACITYt
    Required = Requiredt
    table = tablet
    dijk = dijkt
    TIME = TIMEt
    DEPOT = DEPOTt
    SEED =SEEDt
    np.random.seed (SEED)
    #print("initial")
    pop = []
    ubtrial = 1000000 # trial's num
    psize = 30 # pop size
    psize0 = 0
    l = MAX
    limit = TIME*1/5
    for i in range(ubtrial):
        Route, totalcost = pathscan(table)
        if not CloneSimple(pop, Route, totalcost):
            pop.append((Route, totalcost))
            if totalcost < l:
                l = totalcost
                print(i,l)
        if time.time() - start > limit:#limit:
            #print("break?",time.time(),start)
            break
    pop.sort(key=takecost,reverse=False)
    poptemp = []
    poptemp = copy.deepcopy(pop) + copy.deepcopy(bestpop)
    poptemp.sort (key=takecost, reverse=False)
    bestpop += copy.deepcopy(poptemp[0:15])
    bestpop.sort (key=takecost, reverse=False)
    while 15 < len(bestpop):
        bestpop.pop(15)
    #printformat(pop[0][0],pop[0][1])
    #print("best:",bestpop)
    means(poptemp[0:psize],start,bestpop)

def takecost(e):
    return e[1]

def means(pop,start,bestpop):
    #print("sssmaens")
    pls = 0.2 # proberbility of local search
    gm =500 # number of gene
    psizem = 30
    gm0 = 0
    sample = 0
    while gm0 < gm:
        print("开始繁殖第",gm0,"代")
        if gm0 == 0:
            startt = time.time()
        else:
            poptemp = copy.deepcopy (pop) + copy.deepcopy (bestpop)
            poptemp.sort (key=takecost, reverse=False)
            bestpop += copy.deepcopy (poptemp[0:15])
            bestpop.sort (key=takecost, reverse=False)
            while 15 < len (bestpop):
                bestpop.pop (15)
            pop = copy.deepcopy (poptemp[0:30])
            #print ("best:", bestpop[0][1])

        popt =copy.deepcopy(pop)
        psize = len(pop)
        opsize = 6 * len(pop) ##唐老师是6倍
        i = 0
        j = 0
        while i < opsize and j < 500:
            mother = int(random.random()*(psize))
            father = int(random.random()*(psize))
            while father == mother:
                father = int(random.random() * (psize))

            son = SBX(pop[mother], pop[father]) # two existed solutions
            #if random.random() < pls:
            #    #print("local")
            #    son = localsearch(son)
            #print(son)
            if not Clone(popt,son[0],son[1]):
                popt.append(son)
                i += 1
            j+=1

        popt.sort(key=takecost,reverse=False)
        if len(popt) > psizem:
            pop = popt[0:psizem+1]
        else:
            pop = popt

        printformat (pop[0][0], pop[0][1])



        if gm0 == 0:
            sample = time.time () - startt
        if time.time() -start > TIME-sample-1:
            #print(time.time() -start)
            break
        gm0 += 1

    #print("end")
    #printformat(pop[0][0],pop[0][1])

def localsearch(son):
    solutionY = copy.deepcopy(son[0])
    costY = son[1]
    ###single insert start
    routeindex = int(random.random()*len(solutionY))
    taskindex = int(random.random()*len(solutionY[routeindex]))

    task = solutionY[routeindex].pop(taskindex)
    min = costY
    minSolution = []
    for i in range(len(solutionY)):
        #print(1)
        if caldemand (solutionY[i]) + table[task[0]][task[1]][1] <= CAPACITY:
            for j in range(len(solutionY[i])+1):
                solveT = copy.deepcopy(solutionY)
                solveT[i].insert(j,task)
                costnow = calTT(solveT)
                if costnow < min:
                    min = costnow
                    minSolution = copy.deepcopy(solveT)
                    return (minSolution, min)

    task = (task[1],task[0])
    for i in range(len(solutionY)):
        #print(2)
        if caldemand (solutionY[i]) + table[task[0]][task[1]][1] <= CAPACITY:
            for j in range(len(solutionY[i])+1):
                solveT = copy.deepcopy(solutionY)
                solveT[i].insert(j,task)
                costnow = calTT(solveT)
                if costnow < min:
                    min = costnow
                    minSolution = copy.deepcopy(solveT)
                    return (minSolution, min)
    solveT = copy.deepcopy (solutionY)
    solveT.append([task])
    costnow = calTT (solveT)
    if costnow < min:
        min = costnow
        minSolution = copy.deepcopy (solveT)

    if min < costY:
        return (minSolution,min)
    else:
        return son
    ## Single insert done
def check(solution):
    for x in solution:
        for y in x:
            if y not in Required and (y[1],y[0]) not in Required:
                print("wtf!!1",y)
                return False

    for k in range(len(Required)):
        chuxian = 0
        for i in range(len(solution)):
            j = 0
            while j < len(solution[i]):
                if solution[i][j] == Required[k] or (solution[i][j][1],solution[i][j][0]) == Required[k]:
                    chuxian += 1
                j += 1
        if chuxian != 1:
            #print("重复：",Required[k],chuxian)
            return False
    return True


def SBX(mothert, fathert):
    mother = copy.deepcopy(mothert)
    father = copy.deepcopy(fathert)
    #print("run SBX")
    #mother[0] 是 solution mother[1]是cost
    momo = copy.deepcopy(mother[0])
    if not check(momo):
        print("cao t nainai1111: ", momo)
    fafa = copy.deepcopy(father[0])
    indexm = int(random.random() * (len(mother[0])))
    indexf = int(random.random() * (len(father[0])))
    motherR = copy.deepcopy(mother[0][indexm]) #染色体的位置
    fatherR = copy.deepcopy(father[0][indexf]) # random route in solution

    if type(motherR) != list:
        motherR = [motherR]
    if type(fatherR) != list:
        fatherR = [fatherR]

    if len(motherR) <= 1:
        return father
    if len(fatherR) <= 1:
        return mother
    mo, fa = 0, 0
    while mo == 0 or mo == len(motherR):
        #print("wo cao")
        mo = int(random.random() * (len(motherR)))
    while fa == 0 or fa == len(fatherR):
        #print ("wo ri")
        fa = int(random.random() * (len(fatherR)))
    #print ("!",momo)
    mo1 = motherR[0:mo]
    mo2 = motherR[mo:]
    fa1 = fatherR[0:fa]
    fa2 = fatherR[fa:]#精子和卵子
    ## mother side
    sonmom = copy.deepcopy(mother[0])
    son1 = combine(sonmom,indexm,mo1,fa2)
    cost1 = calTT (son1)
    sonfa = copy.deepcopy(father[0])
    #print ("?",momo)
    son2 = combine(sonfa,indexf,fa1,mo2)
    cost2 = calTT(son2)
    #print (momo,id(momo))
    if not check(son1):
        print("cao t nainai1: ", momo)
        if not check (son2):
            print ("cao t nainai2: ", son2)
            return mother
    elif not check (son2):
        return (son1,cost1)
    elif cost1 < cost2:
        newson = (son1,cost1)
        return newson
    else:
        newson = (son2, cost2)
        return newson

def caldemand(son):
    if type(son)!= list:
        son = [son]
    cost = 0
    for i in range(len(son)):
        cost += table[son[i][0]][son[i][1]][1]
    return cost
def findlack(solution):
    lack = []
    for item in Required:
        chuxian = 0
        for i in range(len(solution)):
            j = 0
            while j < len(solution[i]):
                if solution[i][j] ==item or (solution[i][j][1],solution[i][j][0]) == item:
                    if chuxian == 0:
                        chuxian += 1
                        j += 1
                    elif chuxian >= 1:
                        solution[i].pop(j)
                else:
                    j += 1
        if chuxian == 0:
            lack.append(item)
    return lack, solution
def combine(solutiont,pindex,a,b):
    haha = copy.deepcopy(solutiont)

    solution = copy.deepcopy(solutiont)
    #print("solution", id(solution))
    #print(solution)
    parent = copy.deepcopy(solutiont[pindex])#最初始要更改的solution里的route

    if type(a) != list and type(b) != list:
        son = []
        son.append(a)
        son.append(b)
    elif type(a) != list:
        son = b.copy()
        son.append(a)
    elif type(b) != list:
        son = a.copy()
        son.append (b)
    else:
        son = a + b

    duoyu = []
    for i in range(len(son)) :
        if (son[i] not in parent )and ((son[i][1],son[i][0]) not in parent):
            duoyu.append(son[i])
    #找出所有冗余任务
            #son.pop(index)
        #    continue
        #else:
        #    index+=1
    index = 0
    #bsize = len(b)
    #print (son)
    while index < len(son)-1:
        for j in range(index+1,len(son)) :
            if (son[index] == son[j] or (son[index][1], son[index][0]) == son[j]):
                son.pop(j)
                break
        index += 1#pop出所有重复任务

    solution[pindex] = son.copy()

    #pop duoyu
    for i in range(len(duoyu)):
        for j in range(len(solution)):
            if j == pindex:
                continue
            else:
                k = 0
                while k < len(solution[j]):
                    if (solution[j][k] == duoyu[i] or (duoyu[i][1],duoyu[i][0]) == solution[j][k]):
                        solution[j].pop(k)
                    else:
                        k += 1

    lack,_= findlack(copy.deepcopy(solution))


    while caldemand(solution[pindex]) > CAPACITY:
        popindex = int(random.random()*len(solution[pindex]))
        node = solution[pindex].pop(popindex)
        lack.append(node)

    #将所有多余的pop出去 遍历一遍

    #将少了的插回去
    uppp = 0
    success = 0
    while len(lack)!=0 and uppp < 6 and success == 0:
        i = 0
        success = 1
        uptrailt = 0
        #print("lack",lack)
        up = max(len(lack)*len(lack)/2,10)
        TTresult = copy.deepcopy(solution)
        lackt = lack.copy()

        while lackt!=[] and uptrailt < up:
            #print("lack:",lackt)
            #print("run insertion")
            #print("di yi ceng",lack)
            isinsert = 0
            uptrial = 0
            obj = lackt[0]
            while isinsert == 0 and uptrial <len(TTresult):
                #print ("di er ceng",lackt)
                k = int(random.random()*len(TTresult))
                if (table[obj[0]][obj[1]][1] + caldemand(TTresult[k])) <= CAPACITY:
                    cost = MAX
                    indexn = 0
                    arc = lackt[i]
                    reverse = 0
                    for j in range (0, len (TTresult[k]) + 1):
                        sont = copy.deepcopy(TTresult[k])
                        sont.insert (j, arc)
                        costt = calCost (sont)
                        if costt < cost:
                            cost = costt
                            indexn = j
                    arc = (arc[1], arc[0])
                    for j in range (0, len (TTresult[k]) + 1):
                        sont = copy.deepcopy(TTresult[k])
                        sont.insert (j, arc)
                        costt = calCost (sont)
                        if costt < cost:
                            cost = costt
                            indexn = j
                            reverse = 1
                    if reverse == 1:
                        TTresult[k].insert (indexn, arc)
                    else:
                        TTresult[k].insert (indexn, lackt[i])
                    #print(k,lackt[0],TTresult[k])
                    lackt.pop(0)
                    isinsert += 1
                    break
                uptrial+=1
            if lackt == []:
                break
            if isinsert == 0:
                success = 0
                break
            uptrailt += 1
        #print(TTresult)
        if lackt == [] :
            lack = lackt.copy()
            solution = copy.deepcopy(TTresult)
        else:
            uppp +=1
            continue

    lack, _ = findlack (copy.deepcopy(solution))

    #print("solution", id(solution))
    #print(solution)
    if lack==[]:
        return solution
    else:
        return haha

def calCost(sont):
    cost = 0
    now = DEPOT
    if type(sont) != list:
        #print(now,sont)
        cost += dijk[now][sont[0]] + table[sont[0]][sont[1]][0]
        now = sont[1]
    else:
        for i in range(len(sont)):
            #print(sont)
            cost += dijk[now][sont[i][0]] + table[sont[i][0]][sont[i][1]][0]
            now = sont[i][1]
    cost += dijk[now][DEPOT]
    return cost

def calTT(solution):
    cost = 0
    if type(solution) != list:
        solution=[solution]
    for i in range(len(solution)):
        #print (i, solution[i],solution)
        cost += calCost(solution[i])
    return cost

def CloneSimple(pop, Route, totalcost):
    for i in range(len(pop)):
        if totalcost == pop[i][1]:
            return True
    return False

def Clone(pop, Route, totalcost):
    for i in range(len(pop)):
        same0 = 0
        if totalcost == pop[i][1]:
            same1 = 0
            for j in range(len(Route)):
                same1 = 0
                for k in range(len(pop[i][0])):
                    if Route[j] == pop[i][0][k]:
                        same1 = 1
                if same1 == 0:
                    break
            if same1 == 1: same0 = 1
        if same0 == 1 : return True
    return False


if __name__ == '__main__':
    start = time.time()
    #filepath = sys.argv[1]
    filepath = 'CARP_samples/r/egl-s4-B.dat'
    #TIME = int(sys.argv[3])-1
    TIME = 300
    #SEED = abs(int(sys.argv[5]))
    #SEED = 100
    table = read (filepath)
    getdijk ()
    manager = mp.Manager()
    bestpop = manager.list()
    worker = []
    worker_num = 7  ##上传时改成8
    pool = mp.Pool (worker_num-1)
    for i in range (0, worker_num-1):
        pool.apply_async (initialization, args=(start,CAPACITY, bestpop, Required, table, dijk,TIME,DEPOT,SEED+i,))
    while True:
        end = time.time ()
        if end - start > TIME - 2:
            pool.close ()
            break
        else:
            pass
    end = time.time()
    print("THE END, total time is ", end - start)
    printformat(bestpop[0][0],bestpop[0][1])

#s 0,(1,116),(116,117),(117,2),(117,119),(118,114),(114,113),(113,112),(112,110),(110,107),(107,108),(107,112),0,0,(110,111),(107,106),(106,105),(105,104),(104,102),(66,67),(69,71),(71,72),(72,73),(73,44),(44,43),0,0,(108,109),(66,62),(62,63),(63,64),(64,65),(55,140),(140,49),0,0,(87,86),(86,85),(85,84),(84,82),(82,80),(80,79),(79,78),(78,77),(77,46),(46,43),(43,37),(37,36),(36,38),(38,39),(39,40),0,0,(124,126),(126,130),(68,67),(67,69),(44,45),(45,34),(34,139),(139,33),(33,11),(11,12),(12,13),(20,22),0,0,(95,96),(96,97),(97,98),(56,55),(55,54),(49,48),(11,27),(28,29),(30,32),(30,28),(28,27),(27,25),(25,24),(24,20),0,0,(11,8),(8,6),(6,5),(8,9),(13,14),0
#q 5876
#s 0,(1,116),(116,117),(117,119),(117,2),(118,114),(114,113),(113,112),(112,110),(110,107),(107,108),(107,112),0,0,(107,106),(106,105),(105,104),(104,102),(66,67),(69,71),(71,72),(72,73),(73,44),(44,43),(43,46),0,0,(96,97),(97,98),(96,95),(66,62),(62,63),(63,64),(64,65),(56,55),(55,54),(55,140),(140,49),(49,48),(139,34),0,0,(44,45),(45,34),(139,33),(33,11),(11,8),(8,6),(6,5),(8,9),(13,14),(13,12),(69,67),0,0,(37,36),(36,38),(38,39),(39,40),(37,43),(46,77),(77,78),(78,79),(79,80),(80,82),(82,84),(84,85),(85,86),(86,87),(110,111),0,0,(28,27),(27,11),(11,12),(20,22),(20,24),(24,25),(25,27),(30,32),(30,28),(28,29),(67,68),0,0,(124,126),(126,130),(108,109),0
#q 5520