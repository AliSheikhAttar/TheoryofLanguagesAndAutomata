n = int(input())
grammar = {}
for i in range(n):
    production = input().split('->')
    Lvariable = production[0].replace('<', '').replace('>', '').replace(' ', '')
    Rvariables = production[1].replace('<', '').replace('>', '').replace(' ', '').split('|')
    grammar[Lvariable] = Rvariables

w = input()

#removing Nullable variables
nullable_variable = None
to_delete = None
state = True
while(state):
    state = False
    for key,value in grammar.items():
        if('#' in value):
            state = True
            value.remove('#')
            nullable_variable = key
            if(len(value)==0):
                to_delete = key
            for _, value1 in grammar.items():
                for val in value1:
                    if(nullable_variable in val):
                        value1.append(val.replace(nullable_variable, '#'))

    if(to_delete!= None):
        del grammar[to_delete]
        to_delete = None

for key,_ in grammar.items():
    grammar[key] = list(dict.fromkeys(grammar[key]))
    for i in range(len(grammar[key])):
        if('#' in grammar[key][i]):
            grammar[key][i]  = grammar[key][i] .replace('#','')
    



#removing unit-productions
unit_production_L = None
unit_production_R = None
to_delete = None
state = True
while(state):
    state = False
    for key,value in grammar.items():
        for val in value:
            if(len(val)==1 and ord(val)<=90):
                state = True
                unit_production_L = key
                unit_production_R = val
                value.remove(val)
                if(len(value)==0):
                    to_delete = key
                for key1, value1 in grammar.items():
                    if(key1 == unit_production_R):
                        value.extend(value1)
                        value = list(dict.fromkeys(value))
                        break

    if(to_delete!= None):
        del grammar[to_delete]
        to_delete = None

for key,_ in grammar.items():
    grammar[key] = list(dict.fromkeys(grammar[key]))


#removing useless variables
##not reachable
reachables = ['S']
counter = 0
while(counter<len(reachables)):
    new_reachables = grammar[reachables[counter]]
    for product in new_reachables:
        for char in product:
            if(ord(char)<=90 and char not in reachables):
                reachables.append(char)
    counter += 1

to_delete = None
while(len(grammar)!=len(reachables)):
    for key,_ in grammar.items():
        if(key not in reachables):
            to_delete = key
            break

    del grammar[to_delete]
    for key,value in grammar.items():
        for val in value:
            if(to_delete in val):
                value.remove(val)


##not producing terminals
producing_terminals = []
state = True
tocontinue = True
while(tocontinue):
    tocontinue = False
    for key, value in grammar.items():
        for val in value:
            x = [True for char in val if(char in producing_terminals)]
            if((len(x)!=0 and False not in x  or len(val)==1 and ord(val)>=97) and key not in producing_terminals):
                producing_terminals.append(key)
                tocontinue = True
                break

to_delete = None
to_remove = []
while(len(grammar)!=len(producing_terminals)):
    for key,_ in grammar.items():
        if(key not in producing_terminals):
            to_delete = key
            break

    del grammar[to_delete]
    for key,value in grammar.items():
        for val in value:
            if(to_delete in val):
                to_remove.append(val)
        for item in to_remove:
            value.remove(item)
        to_remove = []


#converting to chomsky
##two variables on the right
counter = 0
state = True
to_add = None
keys = []    
for key,_ in grammar.items(): #no need to check keys appended
    keys.append(key) 
for key in keys:
    for i in range(len(grammar[key])):
        if(len(grammar[key][i])>2):
            to_add = grammar[key][i][1:len(grammar[key][i])]
            grammar[key][i] = grammar[key][i][0]+ 'T' + str(counter)
            for i in range(len(to_add)-2):
                grammar['T' + str(counter)] = [to_add[0]+ 'T' + str(counter+1)]
                counter += 1
            grammar['T' + str(counter)] = [to_add[-2] + to_add[-1]]
            counter+=1



##only one terminal right
state = True 
terminal = None 
keys = []
for key,_ in grammar.items(): #no need to check keys appended
    keys.append(key)  
for key in keys:
    for i in range(len(grammar[key])):
        if(len(grammar[key][i])>=2):
            x = [k for k in range(len(grammar[key][i])) if(ord(grammar[key][i][k])>=97)]
            if(len(x)!=0):
                for o in range(len(x)):
                    x[o] += o
                for j in (x):
                    terminal = grammar[key][i][j]
                    if(j!=0):
                        grammar[key][i] = grammar[key][i][0:j] + 'T' + str(counter) + grammar[key][i][j+1::]
                    else:
                        grammar[key][i] = 'T' + str(counter) + grammar[key][i][1::]
                    grammar['T' + str(counter)] = [terminal]
                    counter += 1




#CYK
to_delete_keys = []
CYK_Matrix = [ [[] for j in range(len(w)- i)] for i in range(len(w))]
CYK_Matrix[0] = [[x] for x in w]
for j in range(len(CYK_Matrix[0])):
    for key, value in grammar.items():
        if(CYK_Matrix[0][j][0] in value):
            CYK_Matrix[0][j].append(key)

    del CYK_Matrix[0][j][0]

# Deleting terminal productions since they wont be checked
for key,value in grammar.items():
    for val in value:
        if(len(val)==1 and ord(val)>= 97):
            grammar[key].remove(val)

    if(len(value)==0):
        to_delete_keys.append(key)

for item in to_delete_keys:
    del grammar[item]

#CYK Filling
for i in range(1,len(w)):
    for j in range(len(CYK_Matrix[i])):
        for key, value in grammar.items():
            for k in range(len(CYK_Matrix[i-1][j])):
                for t in range(len(CYK_Matrix[0][i])):
                    if((CYK_Matrix[i-1][j][k] + CYK_Matrix[0][i][t]) in value):
                        if(key not in CYK_Matrix[i][j]):
                            CYK_Matrix[i][j].append(key)
            for k1 in range(len(CYK_Matrix[i-1][j+1])):
                for t1 in range(len(CYK_Matrix[0][j])):
                    if((CYK_Matrix[0][j][t1] + CYK_Matrix[i-1][j+1][k1]) in value):
                        if(key not in CYK_Matrix[i][j]):
                            CYK_Matrix[i][j].append(key)
#Acceptance
if('S' in CYK_Matrix[-1][-1]):
    print("Accepted")
else:
    print("Rejected")