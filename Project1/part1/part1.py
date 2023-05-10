import json, sys, os
from graphviz import Digraph

SCRIPT_DIR = os.path.dirname(os.path.abspath('auxiliaries.py'))
sys.path.append(os.path.dirname('C:\git\TheoryofLanguagesAndAutomata\Project1\\auxiliaries.py'))

from auxiliaries import *

class Node1 :
    def __init__(self, alphabets):
        self.name1 = []
        self.name = ""
        self.actions = {'$' :[] ,}
        for alphabet in alphabets :
            self.actions[alphabet] = []
    def add_action(self , action , node):
        self.actions[action].append (node)
    def add_name(self, name):
        self.name1.append(name)
    def changename(self):
        self.name1.sort(key=lambda x: int(x[1]))
        for n in self.name1:
            self.name += n



def repeatd(arr):
    result = []
    for item in arr :
        if item not in result and item != [] :
            result.append(item)

    return result

def e_closure(result):
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



def listtonode(result):
    ListOfnode = []
    for i in range(len(result)):
        if (len(result[i])!=0):
            node2append = Node1(alphabets=alphabets)
            for j in range(len(result[i])):
                if(not result[i][j].name in node2append.name):
                    node2append.add_name(result[i][j].name)
            ListOfnode.append(node2append)
        else:
            toappend = Node1(alphabets)
            toappend.name1 = []
            toappend.name = "TRAP"
            ListOfnode.append(toappend)
    return ListOfnode




def find_node2(namelist,nodes):
    for node in nodes :
        if node.name1 == namelist :
            return node
        
def addactions(result,listofnodes):  
    for i in range(len(result)):
        names = []
        for a in alphabets:
            state2go = []
            for j in range(len(result[i])):
                if(result[i][j].name not in names): 
                    names.append(result[i][j].name)
                if (len(result[i][j].actions[a])!=0):
                    for k in range(len(result[i][j].actions[a])):
                        state2go.append(result[i][j].actions[a][k].name)
            findstate = find_node2(state2go,listofnodes)
            here_node = find_node2(names,listofnodes)
            here_node.add_action(a,findstate)




address = 'C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase1-sample\in\input1.json'
alphabets, nodes, starting_node, fs = json2code(address)
newstates = [Start(starting_node)]
convert(newstates[0])
result = newstates
listofnode = listtonode(result)
lr = addactions(result,listofnode)

for node in listofnode:
    node.name1.sort(key=lambda x: int(x[1]))


for node in listofnode:
    node.changename()

fss = []
for i in range(len(listofnode)):
    for s in listofnode[i].name1:  
        if(find_node(s,nodes) in fs):
            fss.append(listofnode[i])
            break

starting_node = listofnode[0]
json1 = convert2json_DFA(listofnode,alphabets,starting_node,fss)

with open("output1.json", "w") as outfile:
    outfile.write(json1)
