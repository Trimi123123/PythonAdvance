import pandas as pd

products = ['apples', 'bananas', 'oranges']

sales = [150,200,300]

sales_series = pd.Series(sales,index=products)

print(sales_series)
