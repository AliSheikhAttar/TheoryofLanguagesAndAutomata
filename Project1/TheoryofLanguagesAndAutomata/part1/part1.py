import json
from graphviz import Digraph

class Node :
    def __init__(self , n , alphabets):
        self.name = n
        self.actions = {'$' :[] ,}
        for alphabet in alphabets :
            self.actions[alphabet] = []
    def add_action(self , action , node):
        self.actions[action].append (node)

def find_node(str):
    for node in nodes :
        if node.name == str :
            return node
        
states_ad = open('C:\git\TLA01-Projects\TheoryofLanguagesAndAutomata\samples\phase1-sample\in\input1.json')
nfa = json.load(states_ad)
states = nfa['states']
states = states.replace("{", "").replace("}", "").replace("'", "").split(',')
alphabets = nfa['input_symbols']
alphabets = alphabets.replace("{", "").replace("}", "").replace("'", "").split(',')
fs_str = nfa['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')
nodes = []
starting_node_str = nfa['initial_state']
tans = nfa["transitions"]

for state in states :
    n = Node(state , alphabets)
    nodes.append(n)




for key,value in tans.items():
    start = find_node(key)
    for key1,value1 in value.items():
        ends = value1.replace("{", "").replace("}", "").replace("'", "").split(',')
        ends = [find_node(x) for x in ends]
        if(key1==""):   
            for end in ends:
                start.add_action("$",end)
        else:
            for end in ends:
                start.add_action(key1,end)
    


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

starting_node = find_node(starting_node_str)

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
output = open("C:\git\TLA01-Projects\TheoryofLanguagesAndAutomata\samples\phase1-sample\in\output1.json",'w')


convert(newstates[0]) 
print(newstates)
 

 