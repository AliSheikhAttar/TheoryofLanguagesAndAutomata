import json
from graphviz import Digraph
from auxiliaries import *



class Node1 :
    def __init__(self, alphabets):
        self.name = []
        self.actions = {'$' :[] ,}
        for alphabet in alphabets :
            self.actions[alphabet] = []
    def add_action(self , action , node):
        self.actions[action].append (node)
    def add_name(self, name):
        self.name.append(name)




def repeatd(arr):
    result = []
    for item in arr :
        if item not in result and item != [] :
            result.append(item)

    return result

def e_closure(state , result):
    for s in result :
        e = s.actions["$"]
        if e == [] or e in result :
            continue
        result.extend(s.actions["$"])
    return result

def Is_Equal(array1 , array2):
    if len(array1)!= len( array2):
        return False

    for item in array1 :
        if item not in array2 :
            return False
    return True

def Start(start):
    newstates = [start]
    e_c = start.actions["$"]
    if len(e_c) != 0 :
        newstates.extend(e_c)
        for s in e_c :
            newstates.extend(Start(s))
    return repeatd(newstates)


newstates = [Start(starting_node)]
def convert( states):
    for alphabet in alphabets :
        newstate = []
        for state in states :
            newstate.extend(state.actions[alphabet])
            newstate.extend(e_closure(state , newstate))
        newstate = repeatd(newstate)
        rep =False
        for k in newstates:
            if Is_Equal(k , newstate) :
                rep = True
                break
        if not rep:
            d = newstate
            newstates.append(d)
            convert(newstate)


result = newstates
def listtonode(result):
    ListOfnode = []
    for i in range(len(result)):
        if (len(result[i])!=0):
            node2append = Node1(alphabets=alphabets)
            for j in range(len(result[i])):
                if(not result[i][j].name in node2append.name):
                    node2append.add_name(result[i][j].name)
            ListOfnode.append(node2append)
    return ListOfnode

listofnode = listtonode(result)

def find_node2(namelist,nodes):
    for node in nodes :
        if node.name == namelist :
            return node
        
def addactions(result,listofnodes):
    resultlist = []
    for i in range(len(result)):
        node2findname = []
        for a in alphabets:
            for j in range(len(result[i])):
                if(not result[i][j].name in node2findname):
                    node2findname.append(result[i][j].name)
                    if (len(result[i][j].actions[a])!=0):
                        state2go = []
                        for k in range(len(result[i][j].actions[a])):
                            state2go.append(result[i][j].actions[a][k].name)
                        findstate = find_node2(state2go,listofnodes)
                        findstate.add_action(a,state2go)
            resultlist.append(findstate)
    return resultlist

lr =addactions(result,listofnode)

