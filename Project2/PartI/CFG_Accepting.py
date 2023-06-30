n = int(input())
grammar = {}
for i in range(n):
    production = input().split('->')
    Lvariable = production[0].replace('<', '').replace('>', '').replace(' ', '')
    Rvariables = production[1].replace('<', '').replace('>', '').replace(' ', '').split('|')
    grammar[Lvariable] = Rvariables


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
    


print(grammar)
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

print(grammar)
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

print(grammar)
#converting to chomsky
##two variables on the right
counterT = 0
counterV = 0
counter1 = 0
state = True
to_add = None
keys = []    
for key,_ in grammar.items(): #no need to check keys appended
    keys.append(key) 
for key in keys:
    for i in range(len(grammar[key])):
        if(len(grammar[key][i])>2):
            to_add = grammar[key][i][1:len(grammar[key][i])]
            grammar[key][i] = grammar[key][i][0]+ 'V' + str(counterV)
            for i in range(len(to_add)-2):
                grammar['V' + str(counterV)] = [to_add[0]+ 'V' + str(counterV+1)]
                counterV += 1
            grammar['V' + str(counterV)] = [to_add[-2] + to_add[-1]]
            counterV+=1


print(grammar)
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
                        grammar[key][i] = grammar[key][i][0:j] + 'T' + str(counterT) + grammar[key][i][j+1::]
                    else:
                        grammar[key][i] = 'T' + str(counterT) + grammar[key][i][1::]
                    grammar['T' + str(counterT)] = [terminal]
                    counterT += 1


print(grammar)

#CYK
