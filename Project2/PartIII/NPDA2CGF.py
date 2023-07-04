import random

# Initialize

Transitions = []
Stack       = []
grammar     = {}
Start_variable = [] # to pass by reference

# Inputs

States = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
Alphabets = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
Stack_alphabets = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
Finals = input().replace('{', '').replace('}', '').replace(' ', '').split(',')
NumberOftransitions = int(input())

for i in range(NumberOftransitions):
    Transitions.append(input().replace('(', '').replace(')', '').replace(' ', '').split(','))

w = input()

# Modification PDA

## Unique final state
def unique_final_state():

    if(len(Finals)==1):
        new_f_name = 'qf'
        for Transition in Transitions:
            if(Transition[0] == Finals[0]):
                Transition[0] = new_f_name
            if(Transition[-1] == Finals[0]):
                Transition[-1] = new_f_name
        
        for i in range(len(States)):
            if(States[i] == Finals[0]):
                States[i] = new_f_name
                break   
        
    else:
    #naming the new states
        q_counter = len(States)-len(Finals)
        Final = 'qf'
        new_state = 'qN' 

        States.append(new_state)

        for f in Finals:
            Transitions.append([f,'#','#','#',new_state])

        for f in Finals:
            new_f_name = 'q' + str(q_counter)
            for Transition in Transitions:
                if(Transition[0] == f):
                    Transition[0] = new_f_name
                if(Transition[-1] == f):
                    Transition[-1] = new_f_name
            
            for i in range(len(States)):
                if(States[i] == f):
                    States[i] = new_f_name
                    break
            
            q_counter += 1
        




        for alphabet in [alphabet for alphabet in Stack_alphabets if(alphabet!='$')]: #except the $
            Transitions.append([new_state,'#',alphabet,'#',new_state])

        Transitions.append([new_state,'#','$','#',Final])

        q_counter = len(States)-1
        new_state_new_name = 'q' + str(q_counter)
        
        for Transition in Transitions:
            if(Transition[0] == new_state):
                Transition[0] = new_state_new_name
            if(Transition[-1] == new_state):
                Transition[-1] = new_state_new_name

                
        for i in range(len(States)):     
            if(States[i] == new_state):
                States[i] = new_state_new_name
                break  



        States.append(Final)

## convert the lambda pop

def lambda_pop():
    to_remove_transitions = []
    Transitions_len = len(Transitions)       
    for i in range(Transitions_len): # no need to check the appended transitions since they satisfy the constraint
        if(Transitions[i][2] == '#'):
            for alphabet in [x for x in Stack_alphabets if(x!='$')]: #except the $
                if(Transitions[i][3] != '#'):
                    Transitions.append([Transitions[i][0], Transitions[i][1], alphabet, Transitions[i][3] + alphabet, Transitions[i][-1]])
                else:
                    Transitions.append([Transitions[i][0], Transitions[i][1], alphabet, alphabet, Transitions[i][-1]])
            to_remove_transitions.append(Transitions[i])
    
    
    for item in to_remove_transitions:
        Transitions.remove(item)

## Convert the push elements with Length one
def length1_push_elements():
    Transitions_len = len(Transitions)
    to_remove_transitions = []
    for i in range(Transitions_len): # no need to check the appended transitions since they satisfy the constraint
        if(len(Transitions[i][3]) == 1 and Transitions[i][3] != '#'):
            q_counter = len(States)-1
            new_q = 'q' + str(q_counter)
            States.append(new_q)
            alphabet = random.choice([alpha for alpha in Stack_alphabets if (alpha != '$')])
            Transitions.append([Transitions[i][0], Transitions[i][1], Transitions[i][2], alphabet + Transitions[i][2], new_q])
            Transitions.append([new_q, '#', alphabet, '#', Transitions[i][-1]])
            to_remove_transitions.append(Transitions[i])
    

    for item in to_remove_transitions:
        Transitions.remove(item)

## Convert the push elements with Length more than two
def Length2more_push_elements():
    Transitions_len = len(Transitions)
    to_remove_transitions = []
    for i in range(Transitions_len): # no need to check the appended transitions since they satisfy the constraint
        if(len(Transitions[i][3]) > 2):
            restofpush = Transitions[i][3]
            q_counter = len(States)-1
            new_q = 'q' + str(q_counter)
            States.append(new_q)
            Transitions.append([Transitions[i][0], Transitions[i][1], Transitions[i][2], restofpush[-2] + restofpush[-1], new_q])
            restofpush = restofpush[:len(restofpush)-2]
            while(len(restofpush)>1):
                q_counter+= 1
                next_new_q = 'q' + str(q_counter)
                States.append(next_new_q)
                for alphabet in [x for x in Stack_alphabets if(x!='$')]: #except the $
                    Transitions.append([new_q, '#', alphabet, restofpush[-1] + alphabet, next_new_q])
                restofpush = restofpush[:len(restofpush)-1]
                new_q = next_new_q

            for alphabet in [x for x in Stack_alphabets if(x!='$')]: #except the $
                Transitions.append([new_q, '#', alphabet, restofpush[-1] + alphabet, Transitions[i][-1]])
            
            restofpush = ""
            to_remove_transitions.append(Transitions[i])        


    for item in to_remove_transitions:
        Transitions.remove(item)

# Create CFG
def Create_CFG():
    Start_variable.append('q0' + ',' + '$' + ',' + 'qf')
    for Transition in Transitions:
        if(Transition[3] == '#'):   ## Lambda-push transitions
            new_var = Transition[0]+ ','+ Transition[2]+ ','+Transition[-1]
            if(new_var not in grammar):
                grammar[new_var] = []
            grammar[new_var].append([Transition[1]])

        else:   ## Two-char transitions
            for state1 in States:
                for state2 in States:
                    new_var =Transition[0]+ ',' + Transition[2] + ','+ state1
                    if(new_var not in grammar):
                        grammar[new_var] = []
                    grammar[new_var].append([Transition[1],Transition[-1]+ ','+ Transition[3][0]+ ','+ state2,state2+ ','+ Transition[3][1]+ ','+ state1])
            
    

# Print Grammar
def Print_Grammar_double_production():
    for key in grammar.keys():
        key_str  = '(' + '<' + key.split(',')[0] + '>' + key.split(',')[1] + '<' + key.split(',')[2] + '>' + ')'
        c = 0
        val_str = ''
        for i in range(len(grammar[key])):
            val_str += grammar[key][i][0]
            if(len(grammar[key][i]) != 1) :
                for k in range(1, 3):
                    val_str += '(' + '<' + grammar[key][i][k].split(',')[0] + '>' + grammar[key][i][k].split(',')[1] + '<' + grammar[key][i][k].split(',')[2] + '>' + ')'
            val_str += ' | '
            c += 1
            if(c==2):
                val_str = val_str[:len(val_str)-2]  # remove the last ' | ' added
                print(key_str + '  --->  ' + val_str)
                val_str = ''
                c = 0
        if(val_str != ''):
            val_str = val_str[:len(val_str)-2]  # remove the last ' | ' added
            print(key_str + '  --->  ' + val_str)
            val_str = ''
            c = 0

def Print_Grammar_single_production():

    for key in grammar.keys():
        key_str  = '(' + '<' + key.split(',')[0] + '>' + key.split(',')[1] + '<' + key.split(',')[2] + '>' + ')'
        val_str = ''
        for i in range(len(grammar[key])):
            val_str += grammar[key][i][0]
            if(len(grammar[key][i]) != 1) :
                for k in range(1, 3):
                    val_str += '(' + '<' + grammar[key][i][k].split(',')[0] + '>' + grammar[key][i][k].split(',')[1] + '<' + grammar[key][i][k].split(',')[2] + '>' + ')'
            print(key_str + '  --->  ' + val_str)
            val_str = ''
            c = 0            
             
# Converting PDA to CFG
unique_final_state()
lambda_pop()
length1_push_elements()
Length2more_push_elements()
Create_CFG()
# Either way:
print("Grammar : ")
Print_Grammar_double_production()
# Print_Grammar_single_production()