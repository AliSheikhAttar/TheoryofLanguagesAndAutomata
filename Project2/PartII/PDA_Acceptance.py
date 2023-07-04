# Initialize

TransDic = {}

ans = False



class Node:
    def __init__(self, name, state, stack, parent):
        self.name = name
        self.state = state
        self.stack = stack
        self.children = []
        self.parent = parent
    def add_child(self, child_name, child_state, result_stack):
        self.children.append(Node(child_name, child_state, result_stack, parent=self))

def is_possible_transition(transition, node):
    state = True
    if(w[node.name] != transition[1] and transition[1] != "#"):
        return False

    if(transition[2] != node.stack[-1] and transition[2] != "#"):
        return False
    
    return True

def included(node, list):
    for var in list:
        if(var.name == node.name and var.stack == name.stack and var.state == name.state):
            return True
    return False

    
# Inputs

States = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
Alphabets = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
stackAlphabets = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
FinalStates = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
CountOfTrans = int(input())
tm = CountOfTrans**3
tm2=0
ListOfTrans = []
initial_state = States[0]
for i in range(CountOfTrans):
    Transition = (input().replace('(', '').replace(')', '').replace(' ', '').split(','))
    if(Transition[0] not in TransDic):
        TransDic[Transition[0]] = []
    TransDic[Transition[0]].append(Transition)

w = input()

def make_tree():
    root = Node(0,initial_state, ['$'], None)
    frontier = [root]
    while(len(frontier)!=0):
        root = frontier[0]
        del frontier[0]
        if(root.state in FinalStates):
            return True
            for node in frontier:
                if(node.state in FinalStates):
                    return True
            return False
        for tran in TransDic[root.state]:
            if(is_possible_transition(tran, root)):
                child_stack = root.stack.copy()
                if(tran[2]!="#"):
                    child_stack[-1]
                for j in range(len(tran[3])-1, -1, -1):
                    if(tran[3][j] != "#"):
                        child_stack.append(tran[3][j])
                if(tran[1] == "#"):
                    root.add_child(root.name, tran[-1], child_stack)
                else:
                    root.add_child(root.name+1, tran[-1], child_stack)
                if(included(root.children[-1],frontier)):
                    return False
                frontier.append(root.children[-1])
    return False



result = make_tree()
if(result):
    print("Accepted")
else:
    print("Rejected")