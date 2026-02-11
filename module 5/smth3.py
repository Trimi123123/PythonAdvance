from email.message import Message

greeting = "hello"

def greet(name):

    global message

    message = f"hello,{greeting}, {name}"

print(message)

greet("bob")
print(message)








greet("alice")

