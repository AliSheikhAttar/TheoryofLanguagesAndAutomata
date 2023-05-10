import json, sys, os
from graphviz import Digraph
SCRIPT_DIR = os.path.dirname(os.path.abspath('auxiliaries.py'))
sys.path.append(os.path.dirname('C:\git\TheoryofLanguagesAndAutomata\Project1\\auxiliaries.py'))

from auxiliaries import *




states_ad1 = ('C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase4-sample\concat\in\FA1.json')

states_ad2 = ('C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase4-sample\concat\in\FA2.json')

alphabets1, nodes1, starting_node1, fs1 = json2code(states_ad1)
alphabets2, nodes2, starting_node2, fs2 = json2code(states_ad2)


for fs in fs1:
    fs.add_action("$",starting_node2)


nodes1_no = len(nodes1)

counter4name = nodes1_no
for i in range(len(nodes2)):
    nodes2[i].name = f"q{counter4name}"
    counter4name+=1


alphabets1.extend(alphabets2)
alphabets = alphabets1
nodes1.extend(nodes2)
nodes = nodes1
starting_node = starting_node1
fs = fs2

result = convert2json_NFA(nodes, alphabets, starting_node, fs)
with open("output2.json", "w") as outfile:
    outfile.write(result)
