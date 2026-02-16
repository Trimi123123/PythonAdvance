

fruits = {
    "apple": 5,
    "banna": 7,
    "orange": 3

}

try:
    print(fruits["cherry"])
except KeyError:
    print("the key doesnt exist")

    