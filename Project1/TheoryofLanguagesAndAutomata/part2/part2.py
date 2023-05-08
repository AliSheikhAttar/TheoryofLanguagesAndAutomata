import json
class Node :
    def __init__(self , n , alphabets):
        self.name = n
        self.actions = {}
        for alphabet in alphabets :
            self.actions[alphabet] = None
    def add_action(self , action , node):
        self.actions[action] = node

def find_node(str):
    for node in nodes :
        if node.name == str :
            return node
nodes = []

states_ad = open('C:\git\TLA01-Projects\TheoryofLanguagesAndAutomata\samples\phase2-sample\in\input1.json')
nfa = json.load(states_ad)
states = nfa['states']
states = states.replace("{", "").replace("}", "").replace("'", "").split(',')
alphabets = nfa['input_symbols']
alphabets = alphabets.replace("{", "").replace("}", "").replace("'", "").split(',')
fs = nfa['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')
nodes = []
starting_state_str = nfa['initial_state']
tans = nfa["transitions"]

for state in states :
    n = Node(state , alphabets)
    nodes.append(n)

for key,value in tans.items():
    start = find_node(key)
    for key1,value1 in value.items():
        end = value1.replace("{", "").replace("}", "").replace("'", "")
        end = find_node(end)
        if(key1==""): 
            start.add_action("$",end)
        else:
            start.add_action(key1,end)
    





final_i = []
notfinal_i = [1]
def reachable(list , current_state):
    for alphabet in alphabets:
        next_s = current_state.actions[alphabet]
        if next_s != [] and next_s not in list:
            list.append(next_s)
            if next_s in fs :
                final_i.append(list.index(next_s)+1)
            else :
                notfinal_i.append(list.index(next_s)+1)
            reachable(list, next_s)
    return list

#reachable nodes from initial state
starting_state = find_node(starting_state_str)
R_nodes = reachable([starting_state] , starting_state)

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
    sameness = True
    for j in range(1 , len(alphabets)+1):
        if row1[j].name != row2[j].name :
            sameness = False
    return sameness


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
count =0 
for item in result :
    if item != []:
        count += 1
print(count)
