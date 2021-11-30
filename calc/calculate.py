import re

def evaluate(input):
    try:
        expression = convert(input) # convert from infix to post fix notation
        answer = postfix_eval(expression) # to then evaluate that with a stack
    except Exception as e:
        return e
    else:
        return answer

def convert(input):
    op_stack = []
    res_stack = []
    i = 0
    while i < len(input):
        if input[i] == "(":
            op_stack.append(input[i])
            i = i + 1
        elif input[i] == ")":
            found_left_parens = False
            while len(op_stack) > 0 and not found_left_parens:
                op = op_stack.pop()
                if op == '(':
                    found_left_parens = True
                else:
                    res_stack.append(op)
            if not found_left_parens:
                raise SyntaxError("Bad Syntax")
            i = i + 1
        elif is_operation(input[i]):
            op1 = input[i]
            while len(op_stack) > 0:
                op2 = op_stack[-1]
                if op2 == '(' or operation_precedence(op1, op2) > 0:
                    break
                else:
                    res_stack.append(op_stack.pop())
            op_stack.append(op1)
            i = i + 1
        else: # is a number
            # regex for both integers and decimals
            match = re.search("-?([0-9]+\.?[0-9]*|\.[0-9]+)", input[i:])
            res_stack.append(match.group())
            i = i + match.span()[1]
    while len(op_stack) > 0:
        op = op_stack.pop()
        if op == '(':
            raise SyntaxError("Bad Syntax")
        res_stack.append(op)
    return res_stack

def postfix_eval(expression):
    stack = []
    for element in expression:
        if is_operation(element):
            try:
                b = stack.pop()
                a = stack.pop()
                stack.append(apply_operation(a, b, element))
            except ZeroDivisionError as zde:
                raise ZeroDivisionError("Divide by Zero")
            except Exception as e:
                raise SyntaxError("Bad Syntax")
        elif is_integer(element):
            stack.append(int(element))
        else:
            stack.append(float(element))
    return str(stack.pop())

def is_operation(char):
    return char in ['+','-','/','*']

def apply_operation(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else: #op == '/'
        return a / b

def operation_precedence(op1, op2):
    if op1 in ['+','-'] and op2 in ['/','*']:
        return -1
    elif op1 in ['/','*'] and op2 in ['+','-']:
        return 1
    else: # equal precedence
        return 0

def is_integer(num):
    integer_regex = r'^-?[0-9]+$'
    return re.match(integer_regex, num)
