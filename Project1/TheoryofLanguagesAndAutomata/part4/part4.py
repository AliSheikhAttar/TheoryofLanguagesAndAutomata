import json
from graphviz import Digraph



class Node :
    def __init__(self , n, alphabets):
        self.name = n
        self.actions = {'$' :[] ,}
        for alphabet in alphabets :
            self.actions[alphabet] = []
    def add_action(self , action , node):
        self.actions[action].append(node)


def find_node(str,nodes):
    for node in nodes :
        if node.name == str :
            return node


FA1_json = open('C:\git\TheoryofLanguagesAndAutomata\Project1\TheoryofLanguagesAndAutomata\samples\phase4-sample\concat\in\FA1.json')
FA1 = json.load(FA1_json)

FA2_json = open('C:\git\TheoryofLanguagesAndAutomata\Project1\TheoryofLanguagesAndAutomata\samples\phase4-sample\concat\in\FA2.json')
FA2 = json.load(FA2_json)

states1 = FA1['states']
states1 = states1.replace("{", "").replace("}", "").replace("'", "").split(',')
alphabets1 = FA1['input_symbols']
alphabets1 = alphabets1.replace("{", "").replace("}", "").replace("'", "").split(',')
fs1_str = FA1['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')


nodes = []
starting_node_str1 = FA1['initial_state']
tans1 = FA1["transitions"]


states2 = FA2['states']
states2 = states2.replace("{", "").replace("}", "").replace("'", "").split(',')
alphabets2 = FA2['input_symbols']
alphabets2 = alphabets2.replace("{", "").replace("}", "").replace("'", "").split(',')
fs2_str = FA2['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')
nodes1 = []
nodes2 = []
starting_node_str2 = FA2['initial_state']
tans2 = FA2["transitions"]

alphabets = alphabets1


for state in states1 :
    n = Node(state,alphabets1)
    nodes1.append(n)





for key,value in tans1.items():
    start = find_node(key,nodes1)
    for key1,value1 in value.items():
        ends = value1.replace("{", "").replace("}", "").replace("'", "").split(',')
        ends = [find_node(x,nodes1) for x in ends]
        if(key1==""):   
            for end in ends:
                start.add_action("$",end)
        else:
            for end in ends:
                start.add_action(key1,end)

starting_node1 = find_node(starting_node_str1,nodes1)
fs1 = []
for fs in fs1:
    fs1.append(find_node(fs, nodes1))


for state in states2 :
    n = Node(state,alphabets2)
    nodes2.append(n)





for key,value in tans2.items():
    start = find_node(key,nodes2)
    for key1,value1 in value.items():
        ends = value1.replace("{", "").replace("}", "").replace("'", "").split(',')
        ends = [find_node(x,nodes2) for x in ends]
        if(key1==""):   
            for end in ends:
                start.add_action("$",end)
        else:
            for end in ends:
                start.add_action(key1,end)


starting_node2 = find_node(starting_node_str2,nodes2)
fs2 = []
for fs in fs2:
    fs2.append(find_node(fs, nodes2))


for fs in fs1:
    fs.add_action("$",starting_node2)


nodes1_no = len(nodes1)

counter4name = nodes1_no-1
for i in range(len(nodes2)):
    nodes2[i].name = f"q{counter4name}"
    counter4name+=1


alphabets = alphabets1.extend(alphabets2)
nodes = nodes1.extend(nodes2)
starting_node = starting_node1
fs = fs2

