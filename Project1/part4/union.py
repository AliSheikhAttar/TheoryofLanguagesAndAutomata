import json, sys, os
from graphviz import Digraph

SCRIPT_DIR = os.path.dirname(os.path.abspath('auxiliaries.py'))
sys.path.append(os.path.dirname('C:\git\TheoryofLanguagesAndAutomata\Project1\\auxiliaries.py'))

from auxiliaries import *



states_ad1 = ('C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase4-sample\\union\in\FA1.json')

states_ad2 = ('C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase4-sample\\union\in\FA2.json')

alphabets1, nodes1, starting_node1, fs1 = json2code(states_ad1)
alphabets2, nodes2, starting_node2, fs2 = json2code(states_ad2)

nodes_no = len(nodes1) + len(nodes2)


alphabets1.extend(alphabets2)
alphabets = alphabets1
nodes1.extend(nodes2)
nodes = nodes1


new_starting_state = Node("q00", alphabets)
new_starting_state.add_action("$", starting_node1)
new_starting_state.add_action("$", starting_node2)
starting_node = new_starting_state


i = 0
for i in range(nodes_no):
    nodes[i].name = f"q{i}"

starting_node.name = f"q{i+1}"

nodes.append(starting_node)

fs1.extend(fs2)
fs = fs1

result = convert2json(nodes, alphabets, starting_node, fs)
with open("OutputPart4_union.json", "w") as outfile:
    outfile.write(result)
