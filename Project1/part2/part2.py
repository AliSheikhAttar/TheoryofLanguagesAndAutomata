import json, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath('auxiliaries.py'))
sys.path.append(os.path.dirname('C:\git\TheoryofLanguagesAndAutomata\Project1\\auxiliaries.py'))

from auxiliaries import *


final_i = []
notfinal_i = [1]
def reachable(list , current_state):
    for alphabet in alphabets:
        next_s = current_state.actions[alphabet][0]
        if next_s != [] and next_s not in list:
            list.append(next_s)
            if next_s in fs :
                final_i.append(list.index(next_s)+1) 
            else :
                notfinal_i.append(list.index(next_s)+1)
            reachable(list, next_s)
    return list

#reachable nodes from initial state
states_ad = 'C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase2-sample\in\input1.json'
alphabets, nodes, starting_state, fs = json2code(states_ad)

R_nodes = reachable([starting_state] , starting_state)
names = [x.name for x in R_nodes]

T1_rows = fs
T2_rows = [node for node in R_nodes if node not in fs]

#constructing tables 

def init_table(table , table_rows):
    for i in range(1 , len(table_rows)+1):
        table[i][0] = table_rows[i-1]
    for j in range(1 , len(alphabets)+1):
        table[0][j] = alphabets[j-1]


def make_table(table , table_rows):
    for i in range(1 , len(table_rows) + 1):
        for j in range(1 , len(alphabets)+1):
            table[i][j] = table[i][0].actions[table[0][j]]
            


def are_same(row1 , row2):
    for j in range(1 , len(alphabets)+1):
        if row1[j][0].name != row2[j][0].name :
            return False
    return True


def contains(list , node):
    for i in range (len(list)):
        if node in list[i]:
            return True
    return False

def are_equal(list1 , list2):
   for i in range(len(list2)):
    for j in range (len(list2[i])):
        if len(list1[i])!=len(list2[i]) or list1[i][j] != list2[i][j]:
            return False
    return True

def reduce_table(table , list , level):
    newlist = [[] for i in range(len(table))]
    index = 0
    for item in list :
        for i in range(len(item)):
            if not contains(newlist, item[i]):
                newlist[index].append(item[i])
                for k in range (i+1 , len(item)):
                    if are_same(table[item[i]], table[item[k]]):
                        newlist[index].append(item[k])
            else :
                continue
            index += 1
    
    if not are_equal(newlist , list) :
        for i in range(len(newlist)):
            for item in newlist[i] :
                table[item][0].name = f"g{level}{i}"
        return reduce_table(table, newlist , level+1)

    return newlist

T =[[0 for j in range (len(alphabets)+1) ] for i in range(len(R_nodes) +1) ]

init_table(T, R_nodes)

make_table(T, R_nodes)

for action in T1_rows :
    action.name =  "f0"
for action in T2_rows :
    action.name = "f1"
   
result = reduce_table(T, [notfinal_i, final_i], 0)

states = []
fs = []
namesofstates_l = []
namesofstates_s = []


for i in range(len(result)):
    if(len(result[i])==0):
        break
    else:
        newname = ""
        for j in range(len(result[i])):
            result[i].append(R_nodes[result[i][0]-1])
            newname+=names[result[i][0]-1]
            del result[i][0]
        for state in result[i]:
            state.name = newname
        states.append(result[i][0])
            


for final_index in final_i:#passing element in states for names changing
    fs.append(R_nodes[final_index-1])


starting_state = states[0]

json1 = convert2json(states,alphabets,starting_state,fs)

with open("OutputPart2.json", "w") as outfile:
    outfile.write(json1)
