
# def main():
#     st.title("hello world")
#
#     st.button("click me")
#
#
# if __name__ == "__main__":
#     main()


import streamlit as st

# if st.button("Click me "):
#     st.write("Button clicked")
#
# st.checkbox("Check me ")
#
# if st.checkbox("check to show some text"):
#     st.write("some text")
#
# user_input = st.text_input("Enter text", value="Sample text")
# st.write("You entered: ", user_input)
#
# age = st.number_input("Enter age: ", min_value=0, max_value=100)
# st.write(f"Your age is: {age}")

st.title("Calculator")

num1 = st.number_input("Enter first number:")
operator = st.selectbox("Choose operation:", ["+", "-"])
num2 = st.number_input("Enter second number:")


if st.button("Calculate"):
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2

    st.write("Result:", result)