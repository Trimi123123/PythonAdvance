try:
    num1 = float(input("Enter 1st number: "))
    num2 = float(input("Enter 2nd number: "))
    op = input("Enter op (+, -, *, /): ")

    if op == "+":
        result = num1 + num2
    elif op == "-":
        result = num1 - num2
    elif op == "*":
        result = num1 * num2
    elif op == "/":
        result = num1 / num2
    else:
        raise ValueError("Invalid operation")

    print("Result:", result)

except ZeroDivisionError:
    print("Cannot divide by zero.")
except ValueError:
    print("Invalid input.")
finally:
    print("Program ended.")
