import random as rnd
import matplotlib.pyplot as plt
import copy

#遺伝子の生成
def gene(num, pop_num):
    x = []
    y = []
    for i in range(num):
        x.append(rnd.randint(0, 100))
        y.append(rnd.randint(0, 100))
    pos_info = {}
    for i in range(num):
        pos_info[i] = [x[i], y[i]]
    sel_num = []
    for i in range(num):
        sel_num.append(i)
    all_route = []
    for _ in range(pop_num):
        all_route.append(rnd.sample(sel_num, num)) #遺伝子
    return pos_info, all_route

#評価値
def evalute(pos_info, all_route, loop=0):
    e_val = []
    for i in range(len(all_route)):
        tmp = []
        for j in range(len(all_route[i])):
            if j == (len(all_route[i]) - 1):
                xs = pos_info[all_route[i][j]][0]
                ys = pos_info[all_route[i][j]][1]
                xd = pos_info[all_route[i][0]][0]
                yd = pos_info[all_route[i][0]][1]
            else:
                xs = pos_info[all_route[i][j]][0]
                ys = pos_info[all_route[i][j]][1]
                xd = pos_info[all_route[i][j+1]][0]
                yd = pos_info[all_route[i][j+1]][1]
            tmp.append(((xs - xd) ** 2 + (ys - yd) ** 2) ** 0.5)
        e_val.append(sum(tmp))
    return e_val

#エリート保存
def select(all_route, e_val, sel_num, sel_size, elite_num, ascending=False):
    sel_pop = []
    elite_pop =[]
    while True:
        sel = rnd.sample(e_val, sel_size)
        sel.sort(reverse=ascending)
        for i in range(sel_num):
            val = sel[i]
            ind = e_val.index(val)
            sel_pop.append(all_route[ind])
        if len(sel_pop) >= (len(all_route) / 2):
            break
    sort_e_val = copy.deepcopy(e_val)
    sort_e_val.sort(reverse=ascending)
    for i in range(elite_num):
        val = sort_e_val[i]
        ind = e_val.index(val)
        elite_pop.append(all_route[ind])
    return sel_pop, elite_pop

#交叉
def cross(sel_pop, cross_prob):
    cross_pop = rnd.sample(sel_pop, 2)
    pop1 = cross_pop[0]
    pop2 = cross_pop[1]
    check = rnd.randint(0,100)
    if check <= cross_prob:
        new_pop1 = []
        cut_ind = rnd.randint(1, len(pop1)-2)
        new_pop1.extend(pop1[:cut_ind])
        for i in range(len(pop1)):
            if pop2[i] not in new_pop1:
                new_pop1.append(pop2[i])
        new_pop2 = []
        new_pop2.extend(pop1[cut_ind:])
        for i in range(len(pop1)):
            if pop2[i] not in new_pop2:
                new_pop2.append(pop2[i])
        return new_pop1, new_pop2
    else:
        return pop1, pop2

#突然変異
def muta(pop, muta_prob, num):
    check = rnd.randint(0,100)
    if check <= muta_prob:
        sel_num = []
        for i in range(num):
            sel_num.append(i)
        sel_ind = rnd.sample(sel_num, 2)
        a = pop[sel_ind[0]]
        b = pop[sel_ind[1]]
        pop[sel_ind[1]] = b
        pop[sel_ind[0]] = a
    return pop

num = 30
pop_num = 200
sel_num = 2
sel_size = 10
elite_num = 1
cross_prob = 50
muta_prob = 3
gene_num = 200
val = []
#初期生成
pos_info, all_route = gene(num, pop_num)
#評価
e_val = evalute(pos_info, all_route)
loc_ind = e_val.index(min(e_val))
loc_inf = all_route[loc_ind]
x = []
y = []
for i in range(len(loc_inf)):
    x.append(pos_info[loc_inf[i]][0])
    y.append(pos_info[loc_inf[i]][1])
plt.plot(x, y, marker="o")
plt.show()
val.append(min(e_val))
for i in range(gene_num):
    #エリート選択
    sel_pop, elite_pop = select(all_route, e_val, sel_num, sel_size, elite_num)
    next_pop = []
    while True:
        #交叉
        pop1, pop2 = cross(sel_pop, cross_prob)
        #突然変異
        pop1 = muta(pop1, muta_prob, num)
        pop2 = muta(pop2, muta_prob, num)
        
        next_pop.append(pop1)
        next_pop.append(pop2)
        if len(next_pop) >= (pop_num - elite_num):
            break
        
    #エリート
    next_pop.extend(elite_pop)
    #評価
    e_val = evalute(pos_info, next_pop, loop=i+1)
    val.append(min(e_val))
    all_route = next_pop
plt.plot(val)
plt.show()
loc_ind = e_val.index(min(e_val))
loc_inf = all_route[loc_ind]
x = []
y = []
for i in range(len(loc_inf)):
    x.append(pos_info[loc_inf[i]][0])
    y.append(pos_info[loc_inf[i]][1])
plt.plot(x, y, marker="o")
plt.show()