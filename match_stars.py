import pickle
import os
import numpy as np

def my_file_read(n1):
    f = open(n1)
    ind = 0
    l = []
    for line in f:
        if ind>2:
            cor = line.split()
            # only stars with iluminescence <15
            if float(cor[3])<15:
                l.append((cor[0], float(cor[1]),float(cor[2])))
        ind += 1
    f.close()
    return l

def find_projection(x,y):
    # 4 direction because abs()
    direction = [(1,1),(1,0),(1,-1),(0,-1)]
    return np.array([abs(i[0]*x + i[1]*y) for i in direction])
    

def find_dist(star, list_of_stars):
    gn,gx,gy = star[0], star[1], star[2]
    lista_d = []
    for name,x,y in list_of_stars:
        dist = ((gx-x)**2 + (gy-y)**2)**0.5
        # /dist because invariant to scale, 
        # nearest star need to be found correctly
        # for stars with iluminescence <15 above is correct
        f = find_projection(x-gx, y-gy)/dist
        lista_d.append((str(gn)+"z"+str(name),dist, f, x, y))
    # form the nearest
    lista_d.sort(key = lambda x:x[1])
    return lista_d

def do_one_file(l, name_to_save):
    # create dict for every file
    # star[name,x,y]  = list of nth nearest stars ("how_many_stars")
    #                   ('name',distance in unit of nearest neighbour,
    #                           [projection on directions])
    how_many_stars = 5
    slownik={}
    for g in l:
        ll = l.copy()
        ll.remove(g)
        g_lista = find_dist(g,ll)
        naj_min = g_lista[0][1]
        l_m = [(i[0],i[1]/naj_min,i[2]) for i in g_lista[:how_many_stars]]
        slownik[(g[0],g[1],g[2])] = (l_m)
    # save to file if takes long    
    f = open(name_to_save, 'wb')
    pickle.dump(slownik,f)
    f.close()



def read_dict(file_name):
    f = open(file_name, 'rb')
    slownik = pickle.load(f)
    f.close()
    return slownik

def check_if_z_same(g1_l, g2_l):
    # check if two stars with assigned list of nearest stars with features are equal
    # epsilon - how different can be
    epsilon = 0.01
    # array with difference in assigned directions
    o = np.array([abs( np.array(g1_l[i][2]) - np.array(g2_l[i][2])) for i in range(len(g2_l))  ])
    # sum within projection
    k = np.sort(np.sum(o, axis = 1))
    # if 3 best gives difference smallest then epsilon return True
    # to be independent to scale /dist algorith won't work for low luminescens
    # if low luminescens better without /dist 
    if abs(np.sum(k[:3]))>epsilon:
        return False
    else:
        return True

def find_match(g,gl,s2):
    for kk,vv in s2.items():
        o = check_if_z_same(gl,vv)
        if o:
            print(g,kk)
            print("yupi yi aj")

if __name__ == "__main__":
    # prepare dicts
    for i in os.listdir("./"):
        if i.endswith(".out"):
            name = i
            print(name)
            l = my_file_read(name)
            do_one_file(l,name.replace(".out",".domi"))

    # load dicts
    l_slo = []
    for i in os.listdir("./"):
        if i.endswith(".domi"):
            print(i)
            l_slo.append(i)
    l_slownikow = [read_dict(i) for i in l_slo ]

    # chose which dict to take

    s1 = l_slownikow[0]
    s2 = l_slownikow[1]

    # print match
    for k,v in s1.items():
        find_match(k,v,s2)


    # if rotation project to direction choose according to direction to nearest star
    # probably calculate few nearest and choose the best (for small luminescens, invisible stars form picture to picture)

