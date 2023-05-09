import json
from graphviz import Digraph
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




# convert(newstates[0]) 
# print(newstates)
 

 

def convert2json_DFA(states, input_symbols, starting_node, fs):
    states_str = "{"
    input_symbols_str = "{"
    final_states_str = "{"
    for state in states:
        states_str += f"'{state.name}',"
    for input_symbol in input_symbols:
        input_symbols_str += f"'{input_symbol}',"
    for final_state in fs:
        final_states_str += f"'{final_state.name}',"
    items = [states_str, input_symbols_str, final_states_str]
    for i in range(len(items)):
        items[i] = items[i][:-1]
        items[i]+="}"
    transitions_str = {}
    for state in states:
        transitions_str[f"{state.name}"] = {}
        for input_symbol in input_symbols:
            if(len(state.actions[input_symbol])==0): 
                transitions_str[f"{state.name}"][f"{input_symbol}"] = "TRAP"
            else:
                transitions_str[f"{state.name}"][f"{input_symbol}"] = str(state.actions[input_symbol][0].name)

    dictionary = {"states":items[0], "input_symbol": items[1],
                 "transition":transitions_str,
                 "initial_state":str(starting_node.name), "final_states":items[2]}

    jsonFile = json.dumps(dictionary,indent=4)
    return jsonFile
     


def convert2json_NFA(states, input_symbols, starting_node, fs):
    states_str = "{"
    input_symbols_str = "{"
    final_states_str = "{"
    for state in states:
        states_str += f"'{state.name}',"
    for input_symbol in input_symbols:
        input_symbols_str += f"'{input_symbol}',"
    for final_state in fs:
        final_states_str += f"'{final_state.name}',"
    items = [states_str, input_symbols_str, final_states_str]
    for i in range(len(items)):
        items[i] = items[i][:-1]
        items[i]+="}"
    transitions_str = {}
    for state in states:
        transitions_str[f"{state.name}"] = {}
        for key,value in state.actions.items():
            if(key=="$"):
                alphabet = ""
            else:
                alphabet = key
            if(len(value)!=0): 
                transitions_str[f"{state.name}"][f"{alphabet}"] = "{"
                if(len(value)==1):
                    transitions_str[f"{state.name}"][f"{alphabet}"] += f"'{value[0].name}'"
                    transitions_str[f"{state.name}"][f"{alphabet}"] += "}"
                else:
                    for i in range(len(value)):
                        transitions_str[f"{state.name}"][f"{alphabet}"] += f"'{value[i].name}',"
                    transitions_str[f"{state.name}"][f"{alphabet}"] = transitions_str[f"{state.name}"][f"{alphabet}"][:-1]
                    transitions_str[f"{state.name}"][f"{alphabet}"] += "}"




    dictionary = {"states":items[0], "input_symbol": items[1],
                 "transition":transitions_str,
                 "initial_state":str(starting_node.name), "final_states":items[2]}

    jsonFile = json.dumps(dictionary,indent=4)
    return jsonFile



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
        else:
            toappend = Node1(alphabets)
            toappend.name1 = []
            toappend.name = "TRAP"
            ListOfnode.append(toappend)
    return ListOfnode

listofnode = listtonode(result)

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


lr = addactions(result,listofnode)

for node in listofnode:
    node.name1.sort(key=lambda x: int(x[1]))


for node in listofnode:
    node.changename()

fss = []
for i in range(len(listofnode)):
    for s in listofnode[i].name1:  
        if(find_node(s) in fs):
            fss.append(listofnode[i])
            break

starting_node = listofnode[0]
json1 = convert2json_DFA(listofnode,alphabets,starting_node,fss)
print(json1)
with open("output1.json", "w") as outfile:
    outfile.write(json1)
