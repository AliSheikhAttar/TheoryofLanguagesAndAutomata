import json
from graphviz import Digraph



class Node :
    def __init__(self , n , alphabets):
        self.name = n
        self.actions = {'$' :[] ,}
        for alphabet in alphabets :
            self.actions[alphabet] = []
    def add_action(self , action , node):
        self.actions[action].append(node)


def find_node(str):
    for node in nodes :
        if node.name == str :
            return node


FA1_json = open('E:\Project1\TheoryofLanguagesAndAutomata\samples\phase4-sample\concat\in\FA1.json')
FA1 = json.load(FA1_json)

FA2_json = open('E:\Project1\TheoryofLanguagesAndAutomata\samples\phase4-sample\concat\in\FA1.json')
FA2 = json.load(FA2_json)

states1 = FA1['states']
states1 = states1.replace("{", "").replace("}", "").replace("'", "").split(',')
alphabets1 = FA1['input_symbols']
alphabets1 = alphabets1.replace("{", "").replace("}", "").replace("'", "").split(',')
fs1 = FA1['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')
nodes = []
starting_node_str1 = FA1['initial_state']
tans1 = FA1["transitions"]


states2 = FA2['states']
states2 = states2.replace("{", "").replace("}", "").replace("'", "").split(',')
alphabets2 = FA2['input_symbols']
alphabets2 = alphabets2.replace("{", "").replace("}", "").replace("'", "").split(',')
fs2 = FA2['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')
nodes1 = []
nodes2 = []
starting_node_str2 = FA2['initial_state']
tans2 = FA2["transitions"]



for state in states1 :
    n = Node(state , alphabets)
    nodes1.append(n)





for key,value in tans1.items():
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

starting_node1 = find_node(starting_node_str1)

for state in states2 :
    n = Node(state , alphabets)
    nodes2.append(n)





for key,value in tans2.items():
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


starting_node2 = find_node(starting_node_str2)


fs2.add_action("$",starting_node2)