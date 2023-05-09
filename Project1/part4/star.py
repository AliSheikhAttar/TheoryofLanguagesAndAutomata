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
        
states_ad = open('C:\git\TheoryofLanguagesAndAutomata\Project1\TheoryofLanguagesAndAutomata\samples\phase4-sample\star\in\FA.json')
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


starting_node = find_node(starting_node_str)
fs = []
for s in fs_str:
    fs.append(find_node(s))

for s in fs:
    s.add_action("$", starting_node)

