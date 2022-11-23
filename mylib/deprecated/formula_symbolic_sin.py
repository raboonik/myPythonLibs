from required_pkgs import *
from sysFuncs import *
# Remeber: you're the one defining everything and requiring the user to use your language! But the language must be consistent everywhere across your package!
# Additionally, the language must not be dumb!


#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#                                           Functions
def pair_index(string, p1_indx):
    n = p1_indx + 1
    skip = 0
    rank = 0
    op_n = 0
    for char in string[p1_indx+1:]:
        if char == "(":
            rank += 1
            skip += 1
        elif char == ")":
            if skip == 0:
                break
            else:
                skip -= 1
        n+=1
    if n <= p1_indx:
        n = -1
        rank = -2
    return n, rank + 1

def sort_dic_with_rank(ranked_dic):
    strlst = [i for i in ranked_dic.keys()]
    sort_numlst = sorted(ranked_dic.values())
    out = {}
    for i in sort_numlst:
        for item in strlst:
            if ranked_dic[item] == i:
                out[item] = i
    return out

# With the following, we're setting the assumption that all degrees inside the trig funcs are to
# be input as degrees! If the user has a quantity that gives the degree in radian, then they must
# multiply that by 180/pi
def deg_to_rad(formula):
    formula = formula.replace(" ", "")
    list_of_trigs = ['sin', 'cos', 'tan']
    for func in list_of_trigs:
        func_len = len(func)
        formula_len = len(formula)
        # The following gives the index of the opening par '(' of all the func terms in formula
        all_func_indeces = [t for t in np.arange(func_len,formula_len) if formula[t-func_len:t] == func]
        # print([formula[t - func_len : t] for t in all_func_indeces]) # This should print all the func heads in formula 
        update_index = 0
        for old_index in all_func_indeces:
            new_index = old_index + update_index
            # print(formula[new_index -3 : new_index]) # This should print the function head 
            left_par_inx = new_index
            right_par_inx, rank = pair_index(formula,left_par_inx)
            seg1 = formula[:left_par_inx+1]
            seg2 = formula[right_par_inx +1 :]
            formula = seg1 + '(pi/180)*('+formula[left_par_inx + 1 : right_par_inx +1]+')' + seg2
            update_index += len('(pi/180)*('+')')
    return formula

#original = '-4*(-2*-(  -26*37)^0.5*-1+  12*(347-256   )^-0.5)^-7*23/-4'
def convert_minus_coefs(formula, basic_operations, parenthesized_operations):
    # Remove spaces
    formula = formula.replace(" ","")
    avail_basic_ops = list(basic_operations.keys())
    avail_parenthesized_ops = list(parenthesized_operations.keys())
    first_char_parenthesized = list(set([item[0] for item in parenthesized_operations.keys()]))
    loop_flags1 = [op for op in avail_basic_ops if op != '-']
    loop_flags1.append("(")
    loop_flags2 = avail_basic_ops
    loop_flags2.append(")")
    loop_flags2.append("(")    # As an argument inside () can take a - coef: -(vx+vy)
    # Occasions where a minus sing can appear:
    # 1) When an operator is followed by -
    # 2) When a left paranthesis if followed by -
    all_neg_indices = [i for i in np.arange(len(formula)) if formula[i] == '-']
    all_negcoef_indices = [i for i in all_neg_indices if formula[i-1] in loop_flags1 or i == 0]
    # all_negcoef_indices contains the index of all the minus signs that appear as coefs
    var_after_neg_inx = 0
    index_update = 0
    extra_parentheses_lst = ['^','/']
    # This way, unlike out past methods we're strictly using index referencing to update formula
    # We could have done this more easily using a nested while-for structure updating formula on the go
    for old_index in all_negcoef_indices:
        # Since in the second loop we intend to update formula, indeces must be updated as well
        # new_index is the updated index of the minus coefs addressed by all_negcoef_indices
        new_index = old_index + index_update
        
        # We simply wanna replace all the neg signs in fomula with (1-2)* except for any operator with higher order priority than multiplication so '^' and '/':
        # 1) Power: a)40^-2 = 0.000625  --> We don't wanna have 40^(1-2)*2 = 0.05, we want 40^((1-2)*2)
        #           b) 40^-(2+4)
        #           c) 40^-sin(64)
        # 2) Division: 23/-4 = -5.75 --> We don't wanna have 23/(1-2)*4 = -92, we want 23/((1-2)*4)
        if formula[new_index-1] in extra_parentheses_lst: 
        # If this is true, then there's no way that new_index+1 reaches beyond len(formula):
            extra_parentheses_cond = True
            # Case b:
            if formula[new_index+1] == "(": var_after_neg_inx, rank = pair_index(formula,new_index+1)
            # Case c: Check if the char right after new_index matches the first letter of any of our func heads
            elif formula[new_index+1] in first_char_parenthesized:
                for func in avail_parenthesized_ops:  # sin(, cos( etc 
                    if new_index + 1 + len(func) < len(formula[new_index + 1:]):
                        if formula[new_index + 1: new_index + 1 + len(func)] == func:
                            var_after_neg_inx, rank = pair_index(formula,new_index + 1 + len(func) -1)
                        else: pass  # Try next func
                    else: pass  # Try next func: maybe next func has a shorter length
            # Case a:
            else:
                for n in np.arange(new_index + 1, len(formula)):
                    if formula[n] in avail_basic_ops:
                        var_after_neg_inx = n-1
                        break
                    elif n == len(formula) - 1:
                        var_after_neg_inx = n
                        break
        else:
            # Simply replace the '-' with (1-2)*
            extra_parentheses_cond = False
            var_after_neg_inx = new_index
        # Split formula into 2 segments before the '-' and after var_after_neg_inx, evaluating the mid part
        # based on extra_parentheses_cond:
        seg1 = formula[:new_index]            # This excludes the neg sing itself and returns '' for new_index = 0 so no worries 
        seg2 = formula[var_after_neg_inx+1:]   # +1 to skip over the -
        if extra_parentheses_cond:
            formula = seg1 +  "((1-2)*"+formula[new_index+1:var_after_neg_inx+1]+')'   +seg2
            index_update += len("((1-2)*"+')') -1 # -1 because we're trading 1 char '-' with (1-2)*
        else:
            formula = seg1 + "(1-2)*" +seg2
            index_update += len("(1-2)*") - 1  # -1 because we're trading 1 char '-' with (1-2)*
    return formula

def convert_sqrt(string):
    m = 0    # Failsafe iterator
    while "sqrt(" in string:
        sqrt_idx = string.index("sqrt(")
        temp = string[sqrt_idx + len("sqrt("):]
        sqrt_arg = temp[0:temp.index(")")]
        replacee = string[sqrt_idx : sqrt_idx + len("sqrt(") + len(sqrt_arg) + 1] # +1 to include ")"
        string = string.replace(replacee,"(("+sqrt_arg+")^0.5)")
        m+=1
        if m > 100:
            print("*Warning: While loop in convert_sqrt() saturated!")
            break
    return string

def find_parenthesized_funcs(string, parenthesized_ops):
    # We can convert these funcs to SPECIFIC keys! and add them to a dictionary. So here
    # we identify the specific terms involving these funcs and rank order them!
    avail_parenthesized_ops = list(parenthesized_ops.keys())
    out_dic = {}
    for func in avail_parenthesized_ops:
    # Adding the '(' in searching for the parenthesized funcs has the benefit that
    # it distinguishes between the actual func heads and possible similarly labeld variables 
        #print("func = ", func)
        linx = 1   
        for n in np.arange(len(func),len(string)):
            if string[n-len(func):n] == func:              # This way (n-1) will be the index of the opening pair '(' of func
                left_pair_inx = n-1
                func_start_inx = left_pair_inx - len(func) + 1
                right_pair_inx, rank = pair_index(string, left_pair_inx)
                key = string[func_start_inx:right_pair_inx+1]
                #print(string[func_start_inx:right_pair_inx+1])
                if key not in out_dic.keys(): out_dic[key] = rank
    return sort_dic_with_rank(out_dic)

# Algorithm: Pairs of parentheses whose immediate neighbouring characters are also pairs of parentheses are redundant:
#            So check to see if a certain '(...)' has anything OTHER THAN another '()' sandwiching them. If they do
#            then it'd be fine, otherwise get rid of the extra ones.
def denude_extra_parentheses(string, basic_operations, parenthesized_operations):
    string = string.replace(" ","")
    avail_basic_ops = list(basic_operations.keys())
    last_char_parenthesized = list(set([item[-2] for item in parenthesized_operations.keys()]))
    m = 0    # Failsafe iterator
    # Since we want to update string everytime we get rid of a pair of "()", we need a while loop nesting a for loop
    while True:
        n=0
        break_while = True
        # If the entire thing is wrapped in parentheses: get rid of them
        # *Warning! You wanna use pair_index to find the pair and not
        #  simply check the first and last char: as a counter example to
        #  that consider recipe = (bx)*(rho)   
        if string[0] == "(" and (pair_index(string,0))[0] == len(string) - 1:
                string = string[1:-1]
                break_while = False
        else: 
            for char in string:
                if char == "(" and string[n-1] not in last_char_parenthesized:
                    pair_n, rank = pair_index(string, n)
                    if rank == -1: raise OSError("The input formula is either missing parentheses or has extra pairs!")
                    no_op = True    # Suppose there's no operator in recipe[n:pair_n]
                    for op in avail_basic_ops:
                        if op in string[n:pair_n]:
                            no_op = False
                            break
                    if no_op:
                        string = string.replace(string[n:pair_n+1], string[n+1:pair_n])
                        break_while = False
                        break
                    else:
                        pass
                    if n > 0 and pair_n < len(string) - 1:
                        if string[n-1] == '(' and string[pair_n + 1] == ")":
                            string = string.replace(string[n-1:pair_n+ 1], string[n:pair_n])
                            break_while = False
                            break
                n+=1
        if m > 100:
            print("*Warning: While loop in denude_extra_parentheses() saturated!")
            break
        elif break_while: break 
        m+=1
    return string

# Get parenthesized bits and their ranks
def parse_parentheses(expression):
    dic = {}
    n = 0
    for char in expression:
        if char == '(':
            pair_n, rank = pair_index(expression, n)
            dic[expression[n:pair_n+1]] = rank
        n+=1
    out = sort_dic_with_rank(dic)
    return out

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
    # last_dic is meant to contain all the keys not available in ss
    # print("\n")
    # print("arg1 = ", arg1)
    # print("operator = ", operator)
    # print("arg2 = ", arg2)
    # print("ss = ", ss)
    # print("last_dic = ", last_dic)
    # print("isnumber(arg1) = ", isnumber(arg1))
    # print("isnumber(arg2) = ", isnumber(arg2))
    # print("isvar(arg1,lst) = ", isvar(arg1,lst))
    # print("isvar(arg2,lst) = ", isvar(arg2,lst))
    # print("isexpression(arg1, lst) = ", isexpression(arg1, lst))
    # print("isexpression(arg2, lst) = ", isexpression(arg2, lst))
    
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
    #print("out = ",out)
    return out

#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#                                           Unparenthized terms:

def sort_operators(refrence_dic, operator_lst):     
    out = [item for item in operator_lst]
    lst_len = len(out)
    m = 0    # Failsafe iterator
    while True:
        n = 0
        break_while = True
        for item in out:
            if n+1 < lst_len:
                if refrence_dic[item] > refrence_dic[out[n+1]]:
                    out[n] = out[n+1]
                    out[n + 1] = item
                    break_while = False
                    break
            n+=1
        if break_while: break
        if m > 100: 
            print("*Warning: While loop in sort_operators() saturated!")
            break
        m+=1
    return out

def get_args(string, op_inx, op_lst, iteration):
    string_out = ''
    cond_L = True
    cond_R = True
    for i in np.arange(len(string)):
        if cond_R:
            if string[op_inx + i + 1] in op_lst:
                arg_R = string[op_inx + 1 : op_inx + i + 1]
                cond_R = False
            elif (op_inx + i + 1) == len(string) - 1:
                arg_R = string[op_inx + 1 : op_inx + i + 2]
                cond_R = False
        if cond_L:
            if string[op_inx - i - 1] in op_lst or (op_inx - i) == 0:
                arg_L = string[op_inx - i : op_inx]
                cond_L = False
    string_out = string.replace(arg_L+string[op_inx]+arg_R,'key'+str(iteration))
    # You wanna record the number of times the substring got replaced
    count_replaced = string_out.count('key'+str(iteration))
    return string_out, count_replaced, arg_L, arg_R

def evaluate_rank1(my_item, operations, ss):
    avail_lst = list(ss.keys())
    op_lst = list(operations.keys())
    #if my_item[0]+my_item[-1] == "()": my_item = my_item[1:-1]
    if my_item[0] == "(" and (pair_index(my_item,0))[0] == len(my_item) - 1: my_item = my_item[1:-1]
    operators = [i for i in my_item if i in op_lst]
    # Fix the order of operators
    operators = sort_operators(({op_lst[i]:i+1 for i in np.arange(len(op_lst))}),operators)
    step_dic = {}
    n = 1
    while len(operators) > 0:
        operator = operators[0]
        op_inx = my_item.index(operator)
        # count_replaced is the number of times a substring was replaced by 'key' + str(m) in get_args().
        # If count_replaced > 1 then operators must be updated
        my_item, my_count_replaced, arg_L, arg_R = get_args(my_item, op_inx, operators, n)
        #print("my_item = ", my_item)
        #print("\n")
        step_dic['key'+str(n)] = evaluate(operations, operator, arg_L, arg_R, avail_lst, ss, step_dic)
        operators = operators[my_count_replaced:]
        n+=1
    return step_dic['key'+str(n-1)]

#                                           End Functions
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈


# We aim to do regular arithmetics as well as evaluating parenthesized functions such as trigonometric funcs
# This means we have to separate lines of work: 
#                   1) Identify parenthesized funcs, evaluate them, and replace them with unique keys in formula
#                   2) Use the new recipe with all the parenthesized funcs replaced with unique keys and their respective
#                      values all stord in an updated ss dict to evaluate the rest of the terms in formula
# The point is to have a separate function that takes care of regular arithmetics so we can pass the arguments of
# parenthesized funcs to this function!
def basic_arithmetics(my_ss, my_recipe, basic_operations):
    avail_lst = list(my_ss.keys())
    
    op = parse_parentheses(my_recipe)
    if len(op) > 0: op[my_recipe] = np.max(list(op.values())) + 1
    
    out_dic = {}
    if len(op) > 0:
        for item in op:
            myrank = op[item]
            if myrank == 1:
                out_dic[item] = evaluate_rank1(item, basic_operations, my_ss)
            else:
                # If rank is greater than 1: 1) Reduce item by replacing its constituents with previous keys in out_dic, naming the replaced segment with out+str(m)
                #                                   * Each time a part is replaced, that part get's recorded in a new dic with key out+str(m)
                #                            2) As before, the item might still contain numbers or "ss" variables. However, evaluate_rank1() takes in
                #                               on input dic of variables so in step 1, instead of creating a new dic, add new keys to ss and pass
                #                               this updated ss to evaluate_rank1()
                item_new = item
                m = 1
                for j in np.arange(len(out_dic)): # Going backwards: this is to replace everything replacable in item by jtems from previous rank
                    jtem = list(out_dic.keys())[-j-1]
                    if jtem in item:
                        item_new = item_new.replace(jtem,'out'+str(m))
                        # update ss
                        my_ss['out'+str(m)] = out_dic[jtem]
                        m+=1
                # Make sure 'out'+str(m) is indeed a key of ss: this is taken care of directly in evaluate_rank1()
                item_new_2 = item_new.replace('(',"")
                item_new_2 = item_new_2.replace(')',"")
                out_dic[item] = evaluate_rank1(item_new_2, basic_operations, my_ss)
    else:
        out_dic[my_recipe] = evaluate_rank1(my_recipe, basic_operations, my_ss)
    return {my_recipe:out_dic[my_recipe]}


# WARNING: Instead of having explicit pass by value and pass by reference semantics, python has pass by name. 
# You are essentially always passing the object itself, and the object's mutability determines whether or not 
# it can be modified. Lists and Dicts are mutable objects. Numbers, Strings, and Tuples are not.
def evaluate_parenthesized(parenthesized_dic, myss, parenthesized_operations, basic_operations):
    out_dic = {}
    avail_parenthesized_ops = list(parenthesized_operations.keys())
    # i = -1
    # i += 1
    # item = list(parenthesized_dic.keys())[i]
    for item in parenthesized_dic:
        arg = item[item.index('(')+1:-1]
        parenthesized_arg = any([item in arg for item in avail_parenthesized_ops])
        outermost_func = item[:item.index('(')+1] # +1 to include the '('
        # Since we already multiplied all the arguments of trig funcs with (pi/180), the minimum possible rank would be 2
        if not parenthesized_arg:
            out_dic[item] = parenthesized_operations[outermost_func](basic_arithmetics(dict(myss), arg, basic_operations)[arg])
        else:
            arg_new = arg
            m = 1
            for j in np.arange(len(out_dic)):
                jtem = list(out_dic.keys())[-j-1]
                if jtem in arg:
                    # update ss
                    myss['parenthesized'+str(m)] = out_dic[jtem]
                    #print(list(myss.keys()))
                    arg_new = arg_new.replace(jtem, 'parenthesized'+str(m))
                    m+=1
            out_dic[item] = parenthesized_operations[outermost_func](basic_arithmetics(dict(myss), arg_new, basic_operations)[arg_new])
    return out_dic

def formula_func_symbolic(myss, formula):
    parenthesized_operations = {"sin(": lambda x:np.sin(x), "cos(": lambda x:np.cos(x), "tan(": lambda x:np.tan(x)}
    basic_operations = {"^": (lambda x,y: x**y), "/": (lambda x,y: x/y), "*": (lambda x,y: x*y), "+": (lambda x,y: x+y), "-": (lambda x,y: x-y)}
    
    final_formula = formula.replace(" ", "")
    final_formula = deg_to_rad(final_formula)
    final_formula = convert_minus_coefs(final_formula, basic_operations,parenthesized_operations)
    final_formula = denude_extra_parentheses(convert_sqrt(final_formula),basic_operations, parenthesized_operations)
    
    parenthesized_funcs_cond = [t in final_formula for t in parenthesized_operations.keys()]
    
    # Add all the constants!
    final_formula = final_formula.replace('(pi/180)','piDiv')
    final_formula = final_formula.replace('(1-2)','negOne')
    myss['pi'] = np.pi
    myss['piDiv'] = np.pi/180.
    myss['negOne'] = -1
    
    
    if any(parenthesized_funcs_cond):
        # Get the parenthesized terms: the output dic has no repetitive key so you can
        # freely replace the keys in formula with unique expressions. This dic needs to
        # be evalated using a separate function!
        parenthesized_dic = find_parenthesized_funcs(final_formula, parenthesized_operations)
        parenthesized_ss = evaluate_parenthesized(parenthesized_dic, dict(myss), parenthesized_operations, basic_operations)
        # In replacing the items of formula by the keys in parenthesized_ss we wanna reverse the keylist
        # so the highest ranks are replaced first!
        keylst = list(reversed(parenthesized_ss.keys()))
        m = 1
        for key in keylst:
            final_formula = final_formula.replace(key, 'final'+str(m))
            myss['final'+str(m)] = parenthesized_ss[key]
            m+=1
        final_dic = basic_arithmetics(dict(myss), final_formula,basic_operations)
        del(myss)
        return {formula: final_dic[final_formula]}
    else:
        return basic_arithmetics(dict(myss), final_formula,basic_operations)

# del(ss)
# ss = {'vy':[0,1,2]}
# out= formula_func_symbolic(dict(ss), formula)
# To test:
# recipe = '-4*(-2*-(  -26*37)^0.5*-1+  12*(347-256   )^-0.5)^-7*23/-4'
# ss = {'vy':[1,2,3]}
# ans = formula_func_symbolic(ss, recipe)
# ans[list(ans.keys())[0]] == (-4*(-2*-(  -26*37)**0.5*-1+  12*(347-256   )**-0.5)**-7*23/-4)

# recipe = '-4*(-2*-(  -26*sin(-4)*37)^0.5*-1+  tan(347-256*-15)*12*(347-256   )^-0.5)^-7*23/-4'
# ss = {'vy':[1,2,3]}
# ans = formula_func_symbolic(ss, recipe)
# ans[list(ans.keys())[0]] == -4*(-2*-(  -26*np.sin(-4*np.pi/180)*37)**0.5*-1+  np.tan((347-256*-15)*np.pi/180)*12*(347-256   )**-0.5)**-7*23/-4

# original = '-40^20/-sin(90)^-sin(90)*(-2*-(-26*-sin(-4)*37)+sin(90)^-0.5*-1+tan(347*sin(90)-cos(256+cos(-80))^4*-15)*12*(347-256)^-0.5)^-7*23/-4'  
# formula = original
# eval(((((formula.replace('^','**').replace('sin','np.sin')).replace('cos','np.cos'))).replace('tan','np.tan')).replace('pi','np.pi'))
# eval(str(-40**20/-np.sin(90*np.pi/180)**-np.sin(90*np.pi/180)*(-2*-(-26*-np.sin(-4*np.pi/180)*37) + np.sin(90*np.pi/180)**-0.5*-1+
#       np.tan((347*np.sin(90*np.pi/180)-np.cos((256+np.cos(-80*np.pi/180))*np.pi/180)**4*-15)*np.pi/180)*12*(347-256)**-0.5)**-7*23/-4))


# del(ss)
# vy = np.reshape(np.arange(2*4*3),[2,4,3])
# rho0 = np.reshape(np.arange(2*4*3)*0.37,[2,4,3])
# rho = 1.3*np.reshape(np.arange(2*4*3)*0.37,[2,4,3])
# vz = (vy*1.37)**3.3
# bx = rho0*vy
# by = pow(rho0,0.33)
# ss={}
# ss['vy']=vy
# ss['vz']=vz
# ss['rho0']=rho0
# ss['rho']=rho
# ss['bx']=bx
# ss['by']=by
# out= formula_func_symbolic(dict(ss), formula)
# original = '4*(2*-vy + bx*(sin(30*cos(60))*rho0 + rho*-4*(-2*-(  -26*37)^0.5*-1+  12*(347-256   )^-0.5)^-7*23/-4)^0.5)-7*vz/4/337 '
# formula = original
# dif = out[list(out.keys())[0]] - (4*(2*-vy + bx*(np.sin((30*np.cos(60*np.pi/180))*np.pi/180)*rho0 + rho*-4*(-2*-(  -26*37)**0.5*-1+  12*(347-256   )**-0.5)**-7*23/-4)**0.5)-7*vz/4/337)
