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

#original = '-4*(-2*-(  -26*37)^0.5*-1+  12*(347-256   )^-0.5)^-7*23/-4'
def convert_minus_coefs(formula, operations):
    # Remove spaces
    formula = formula.replace(" ","")
    avail_ops = list(operations.keys())
    loop_flags1 = [op for op in avail_ops if op != '-']
    loop_flags1.append("(")
    loop_flags2 = avail_ops
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
    # This way, unlike out past methods we're strictly using index referencing to update formula
    # We could have done this more easily using a nested while-for structure updating formula on the go
    for old_index in all_negcoef_indices:
        # Since in the second loop we intend to update formula, indeces must be updated as well
        # new_index is the updated index of the minus coefs addressed by all_negcoef_indices
        new_index = old_index + index_update
        for n in np.arange(new_index + 1, len(formula)):
            if formula[n] == '(': left_arenthesis = True
            else: left_arenthesis = False
            if formula[n] in loop_flags2:
                var_after_neg_inx = n-1
                break
            elif n == len(formula) - 1:
                var_after_neg_inx = n
                break
        # Replace these minus coefs by (1-2)*
        seg1 = formula[:new_index]            # This returns '' for new_index = 0 so no worries 
        seg2 = formula[var_after_neg_inx+1:]   # +1 to skip over the -
        formula == seg1 +'-'+ seg2
        if left_arenthesis:
            formula = seg1 + "(1-2)*" +seg2
            index_update += len("(1-2)*") - 1  # -1 because we're trading 1 char '-' with (1-2)*
        else:
            formula = seg1 +  "((1-2)*"+formula[new_index+1:var_after_neg_inx+1]+')'   +seg2
            index_update += len("((1-2)*"+')') -1 # -1 because we're trading 1 char '-' with (1-2)*
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

# Algorithm: Pairs of parentheses whose immediate neighbouring characters are also pairs of parentheses are redundant:
#            So check to see if a certain '(...)' has anything OTHER THAN another '()' sandwiching them. If they do
#            then it'd be fine, otherwise get rid of the extra ones.
def denude_extra_parentheses(string, operations):
    avail_ops = list(operations.keys())
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
                if char == "(":
                    pair_n, rank = pair_index(string, n)
                    if rank == -1: raise OSError("The input formula is either missing parentheses or has extra pairs!")
                    no_op = True    # Suppose there's no operator in recipe[n:pair_n]
                    for op in operations:
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
    dic1 = {}
    n = 0
    for char in expression:
        if char == '(':
            pair_n, rank = pair_index(expression, n)
            dic1[expression[n:pair_n+1]] = rank
        n+=1
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
    # last_dic is meant to contain all the keys not available in ss
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
        step_dic['key'+str(n)] = evaluate(operations, operator, arg_L, arg_R, avail_lst, ss, step_dic)
        operators = operators[my_count_replaced:]
        n+=1
    return step_dic['key'+str(n-1)]

#                                           End Functions
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈
#◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈◈


def formula_func_symbolic(my_ss, my_recipe):
    operations = {"^": (lambda x,y: x**y), "/": (lambda x,y: x/y), "*": (lambda x,y: x*y), "+": (lambda x,y: x+y), "-": (lambda x,y: x-y)}
    avail_lst = list(my_ss.keys())
    
    my_recipe = my_recipe.replace(" ", "")
    my_recipe = denude_extra_parentheses(convert_sqrt(my_recipe), operations)
    my_recipe = convert_minus_coefs(my_recipe, operations)
    
    op = parse_parentheses(my_recipe)
    if len(op) > 0: op[my_recipe] = np.max(list(op.values())) + 1
    
    op1 = {}
    if len(op) > 0:
        for item in op:
            myrank = op[item]
            if myrank == 1:
                op1[item] = evaluate_rank1(item, operations, my_ss)
            else:
                # If rank is greater than 1: 1) Reduce item by replacing its constituents with previous keys in op1, naming the replaced segment with out+str(m)
                #                                   * Each time a part is replaced, that part get's recorded in a new dic with key out+str(m)
                #                            2) As before, the item might still contain numbers or "ss" variables. However, evaluate_rank1() takes in
                #                               on input dic of variables so in step 1, instead of creating a new dic, add new keys to ss and pass
                #                               this updated ss to evaluate_rank1()
                item_new = item
                m = 1
                for j in np.arange(len(op1)): # Going backwards: this is to replace everything replacable in item by jtems from previous rank
                    jtem = list(op1.keys())[-j-1]
                    if jtem in item:
                        item_new = item_new.replace(jtem,'out'+str(m))
                        # update ss
                        my_ss['out'+str(m)] = op1[jtem]
                        m+=1
                # Make sure 'out'+str(m) is indeed a key of ss: this is taken care of directly in evaluate_rank1()
                item_new_2 = item_new.replace('(',"")
                item_new_2 = item_new_2.replace(')',"")
                op1[item] = evaluate_rank1(item_new_2, operations, my_ss)
    else:
        op1[my_recipe] = evaluate_rank1(my_recipe, operations, my_ss)
    return {my_recipe:op1[my_recipe]}

# To test:
# recipe = '-4*(-2*-(  -26*37)^0.5*-1+  12*(347-256   )^-0.5)^-7*23/-4'
# ss = {'vy':[1,2,3]}
# ans = formula_func_symbolic(ss, recipe)
# ans[list(ans.keys())[0]] == (-4*(-2*-(  -26*37)**0.5*-1+  12*(347-256   )**-0.5)**-7*23/-4)
