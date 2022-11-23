import numpy as np
# Remeber: you're the one defining everything and requiring the user to use your language! But the language must be consistent everywhere across your package!
# Additionally, the language must not be dumb!

# Not necessary, but if you need to sort a list of strings with respect to a list of numbers
def permute(numlst,strlst):
    dic = {}
    for i in numlst:
        dic[str(i)] = strlst[numlst.index(i)]
    sort_numlst = sorted(numlst)
    out = []
    for i in sort_numlst:
        out.append(dic[str(i)])
    return out

def pair_index(string, p1_indx): 
    rank=0                       
    k=0
    index = 0
    for i in np.arange(p1_indx+1, len(string)):
        if string[i] == '(': rank+=1
        if rank+k == 0 and string[i] == ')':
            index = i
            break
        if string[i] == ')': k-=1
    return index, rank+1

def parse_expression(expression):
    dic1 = {}
    for i in np.arange(len(expression)):
        if expression[i] == '(':
            j = i - 1
            while expression[j] not in '(,' and j != -1:
                j-=1
            pair_n, rank = pair_index(expression, i)
            dic1[expression[j+1:pair_n+1]] = rank
    
    strlst = [i for i in dic1.keys()]
    sort_numlst = sorted(dic1.values())
    dic2 = {}
    for i in sort_numlst:
        for item in strlst:
            if dic1[item] == i:
                dic2[item] = i
    return dic2


def isnumber(inp):
    try:
        np.float(inp)
        cond=1
    except:
        cond = 0
    return cond    


def isvar(inp, lst):
    if inp in lst:
        return 1
    else:
        return 0


def isexpression(inp, lst):
    if not isvar(inp, lst) and not isnumber(inp):
        return 1
    else:
        return 0

def evaluate(ops, operator, arg1, arg2, lst, ss, last_dic=None):
    if isnumber(arg1) and isnumber(arg2):
        out = ops[operator](eval(arg1),eval(arg2))
    elif isnumber(arg1) and isvar(arg2, lst):
        out = ops[operator](eval(arg1),ss[arg2])
    elif isvar(arg1, lst) and isnumber(arg2):
        out = ops[operator](ss[arg1], eval(arg2))
    elif isvar(arg1, lst) and isvar(arg2, lst):
        out = ops[operator](ss[arg1], ss[arg2])
    elif isexpression(arg1, lst) and isnumber(arg2):
        out = ops[operator](last_dic[arg1], eval(arg2))
    elif isexpression(arg2, lst) and isnumber(arg1):
        out = ops[operator](eval(arg1), last_dic[arg2])
    elif isexpression(arg1, lst) and isvar(arg2,lst):
        out = ops[operator](last_dic[arg1], ss[arg2])
    elif isexpression(arg2, lst) and isvar(arg1,lst):
        out = ops[operator](ss[arg1], last_dic[arg2])
    else:
        out = ops[operator](last_dic[arg1], last_dic[arg2])
    return out
        


def formula_func(ss, recipe):
    operations = {"plus": (lambda x,y: x+y), "minus": (lambda x,y: x-y), "div": (lambda x,y: x/y),\
                  "pow": (lambda x,y: x**y), "times": (lambda x,y: x*y), "sqrt": (lambda x,y: np.sqrt(x))}
    ls = ['bx','by','bz','vx','vy','vz','te','rho','pe','etot', 'eint','pelectron', 'pml_b', 'pml_t', 'qtot',\
                  'valf','vlong','vfast','fmag_z','fmag_alf_z','beta','omega', 'bx0','by0','bz0','te0','rho0','pe0']
                  
    # Parse the operations in recipe: The method below automatically makes
    # same-ranked members independent of each other
    # Ex: recipe = 'times(div(pow(vy,6),div(1,2)),pow(times(rho,6),div(1,2)))' produces the following dic
    # {'pow(vy,6)': 1, 'div(1,2)': 1, 'times(rho,6)': 1, 'div(pow(vy,6),div(1,2))': 3, 'pow(times(rho,6),div(1,2))': 3, 'times(div(pow(vy,6),div(1,2)),pow(times(rho,6),div(1,2)))': 7}
    # THERE'S ALWAYS GONNA BE AT LEAST ONE RANK1 TERM
    
    # This will separate out all the operations in growing order of rank
    op = parse_expression(recipe)
    lst = [i for i in op.keys()]
    ss_out = dict()
    for item_ss in ss:
        op1 = {}
        for item in op:
            myrank = op[item]
            operator = item[0:item.index('(')]
            if myrank == 1:
                arg1 = item[item.index('(')+1:item.index(',')]
                arg2 = item[item.index(',')+1:item.index(')')]
                op1[item] = evaluate(operations, operator, arg1, arg2, ls, ss[item_ss], None)
            else:
                item_new = item
                dic_new = {}
                m = 1
                for j in np.arange(len(op1)): # This is to replace everything replacable in item by jtems from all previous ranks
                    jtem = list(op1.keys())[-j-1]
                    if jtem in item:
                        item_new = item_new.replace(jtem,'out'+str(m))
                        dic_new['out'+str(m)] = op1[jtem]
                        m+=1
                arg1 = item_new[item_new.index('(')+1:item_new.index(',')]
                arg2 = item_new[item_new.index(',')+1:-1]
                op1[item] = evaluate(operations, operator, arg1, arg2, ls, ss[item_ss], dic_new)
        ss_out[item_ss] = {recipe: op1[recipe]}
        del(op1)
            
            
    return ss_out





        
        
