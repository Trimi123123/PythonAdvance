def add(x , y):
    return x+ y

def operate(operation,x,y):
    return operation(x,y)

result_sum = operate(add  ,3, 5)

print("result of 3+5:", result_sum)

