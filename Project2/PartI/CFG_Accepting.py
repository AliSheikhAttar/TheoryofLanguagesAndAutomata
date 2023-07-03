n = int(input())
grammar = {}
variables = []

class variable:
    def __init__(self, s, is_terminal, is_initial = False):
        self.name = s
        self.is_terminal = is_terminal
        self.is_initial = is_initial

def search_var(var):
    for item in variables:
        if(item.name == var):
            return item
    return None


def search_var_byname(name):
    for item in variables:
        if(item.name == name):
            return item

def find_initial():
    for key,_ in grammar.items():
        if(key.is_initial):
            return key

def included(item, in_list):
    for x in in_list:
        if(x == item and x[0] == item[0]):
            return True

for i in range(n):
    production = input().split('->')
    Lvariable = production[0].replace('<', '').replace('>', '').replace(' ', '')
    Rvariables = production[1].replace('<', '').replace('>', '').replace(' ', '').split('|')
    res = search_var(Lvariable)
    if(res == None):
        variables.append(variable(Lvariable,False))
        grammar[search_var(Lvariable)] = []
        
    else:
        grammar[search_var(Lvariable)] = []
    
   
    for var in Rvariables:
        x = []
        for char in var:
            res = search_var(char)
            if(res != None):
                x.append(search_var(char))
            else:
                if(65<=ord(char)<=90):
                    y = variable(char, False)
                    x.append(y)
                else:
                    y = variable(char, True)
                    x.append(y)  
                variables.append(y)

        grammar[search_var(Lvariable)].append(x)

    if(i==0):
        search_var(Lvariable).is_initial = True



w = input()

#Simplification
def Simplification():
    #removing Nullable variables
    nullable_variable = None
    to_delete = None
    state = True
    lam = search_var('#')
    while(state):
        state = False
        for key, value in grammar.items():
            for var in value:
                if(lam) in var:
                    state = True
                    var.remove(lam)
                    for _, value1 in grammar.items():
                        state1 = False
                        for val in value1:
                            if(key in val):
                                state1 = True
                                new_val = val.copy()
                                new_val.remove(key)
                                value1.append(new_val)
                                break




 
    state = True
    while(state):
        state = False
        for key, value in grammar.items():
            if((value)==0):
                del grammar[key]
                state = True
                break
            else:
                for val in value:
                    if(len(val)==0):
                        value.remove(val)
                        state = True
                        break
            if(state):
                break
            
        


    if(len(grammar) == 0):
        return False
    #removing unit-productions
    state = True
    while(state):
        state = False
        for key,value in grammar.items():
            for val in value:
                if(len(val)==1 and not val[0].is_terminal):
                    state = True
                    value.remove(val)
                    if(val[0] in grammar):
                        for val1 in grammar[val[0]]:
                            if(val1 not in value):
                                value.append(val1)
                    break

    while(state):
        state = False
        for key, value in grammar.items():
            if((value)==0):
                del grammar[key]
                state = True
                break


    if(len(grammar) == 0):
        return False
    #removing useless variables
    ##not producing terminals
    producing_terminals = []
    state = True
    tocontinue = True
    while(tocontinue):
        tocontinue = False
        for key, value in grammar.items():
            for val in value:
                x = [(char.is_terminal or char in producing_terminals) for char in val ] 
                if((False not in x ) and (key not in producing_terminals)):
                    producing_terminals.append(key)
                    tocontinue = True
                    break


    notproducing_terminals = [var for var in variables if(not var.is_terminal and (var not in producing_terminals))]
    for notproducing_terminal in notproducing_terminals:
        if(notproducing_terminal in grammar):
            del grammar[notproducing_terminal]
            variables.remove(notproducing_terminal)

        for key,value in grammar.items():
            grammar[key] = list(filter(lambda x: notproducing_terminal not in x,value))


    if(len(grammar) == 0):
        return False
    ##not reachable
    state = True
    while(state):
        state = False
        for var in variables:
            if(not var.is_terminal and var not in grammar):
                state = True
                for key, value in grammar.items():
                    grammar[key] = list(filter(lambda x: var not in x,value))
                variables.remove(var)
                break
    

    reachables = [find_initial()]
    counter = 0
    while(counter<len(reachables)):
        for val in grammar[reachables[counter]]:
            for char in val:
                if(not char.is_terminal and char not in reachables):
                    reachables.append(char)        
        counter+=1
       
    state = True
    while(state):
        state = False
        for var1 in variables:
            if(var1 not in reachables and not var1.is_terminal):
                state = True
                if(var1 in grammar):
                    del grammar[var1]
        
                for key, value in grammar.items():
                    grammar[key] = list(filter(lambda x: var1 not in x,value))
                variables.remove(var1)
                break

    if(len(grammar) == 0):
        return False
    
    return True



#converting to chomsky
def convert2chomsky():
    ##two variables on the right
    counter = 0
    state = True
    to_add = None
    keys = [] 
    new_value = []   
    for key,_ in grammar.items(): #no need to check keys appended
        keys.append(key) 
    for key in keys:
        for i in range(len(grammar[key])):
            if(len(grammar[key][i])>2):
                vg = (variable('T' + str(counter), False))
                variables.append(vg)
                j1 = 1
                for j in range(1,len(grammar[key][i])-2):
                    v1 = (variable('T' + str(counter), False))
                    grammar[variables[-1]] = [[grammar[key][i][j],  v1]]
                    variables.append(v1)
                    counter+=1
                    j1 += 1
                
                grammar[variables[-1]] = [[grammar[key][i][j1], grammar[key][i][j1+1]]]
                grammar[key][i] = [grammar[key][i][0], search_var_byname('T' + str(counter-j1+1))]
                counter+=1
                





    ##only one terminal right
    keys = []
    for key,_ in grammar.items(): #no need to check keys appended
        keys.append(key)  
    for key in keys:
        for i in range(len(grammar[key])):
            if(len(grammar[key][i])==2):
                x = [k for k in range(len(grammar[key][i])) if(grammar[key][i][k].is_terminal)]
                if(len(x)!=0):
                    for j in (x):
                        vg = variable('T' + str(counter),False)
                        grammar[vg] = [[grammar[key][i][j]]]
                        grammar[key][i][j] = vg  
                        variables.append(vg)
                        counter += 1



#CYK



def CYK_Matrix():
    to_delete_keys = []
    CYK_Matrix = [ [[] for j in range(len(w)- i)] for i in range(len(w)) ]
    CYK_Matrix[0] = [[x] for x in w]
    for j in range(len(CYK_Matrix[0])):
        for key, value in grammar.items():
            if([search_var_byname(CYK_Matrix[0][j][0])] in value):
                CYK_Matrix[0][j].append(key)

        del CYK_Matrix[0][j][0]

    # Deleting terminal productions since they won't be checked
    state = True
    while(state):
        state = False
        for key,value in grammar.items():
            for val in value:
                if(len(val)==1 and val[0].is_terminal):
                    state = True
                    grammar[key].remove(val)

            if(len(value)==0):
                del grammar[key]
                break


    #CYK Filling
    for i in range(1,len(w)):
        for j in range(len(CYK_Matrix[i])):
            for key, value in grammar.items():
                for z in range(1,i+1):
                    for k in range(len(CYK_Matrix[i-z][j])):
                        for t in range(len(CYK_Matrix[z-1][i+j-z+1])):
                            if(included([CYK_Matrix[i-z][j][k], CYK_Matrix[z-1][i+j-z+1][t]],value)):
                                if(key not in CYK_Matrix[i][j]):
                                    CYK_Matrix[i][j].append(key)

    return CYK_Matrix

CYK = None
stateofgrammar = Simplification()
if(stateofgrammar):
    convert2chomsky()
    CYK = CYK_Matrix()
else:
    print("Rejected")
#Acceptance
if(stateofgrammar):
    if(find_initial() in CYK[-1][-1]):
        print("Accepted")
    else:
        print("Rejected")