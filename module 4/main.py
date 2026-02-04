while True:
    user_input = input("enter a positive number:")

    if user_input.isnumeric():
        number = int(user_input)
        if number > 0:
            break

            print("invqlid input.please try again")

            print("you entered a valid positive number:", number)

            