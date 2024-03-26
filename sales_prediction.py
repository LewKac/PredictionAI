import pandas
import numpy
import sys

from sklearn.svm import LinearSVR   
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

shops_file = pandas.read_csv("shops.csv")
items_file = pandas.read_csv("items.csv")
categories_file = pandas.read_csv("item_categories.csv")
sales_file = pandas.read_csv("sales_train.csv")
test_file = pandas.read_csv("test.csv")




original_stdout = sys.stdout # Save a reference to the original standard output

monthly_sales = []


#print("\nPlease enter shop number or enter -1 to select all shops: ")
#shop_id = int(input())

# print("\nPlease enter item number or enter -1 to select all items: ")
# item_id = int(input())

amount_items = len(test_file.index) - 1
print(amount_items)

items = []
shops = []

for i, row in test_file.iterrows():
    items.append(row['item_id'])
    shops.append(row['shop_id'])




#if (shop_id != -1):
#    sales_file = sales_file[sales_file['shop_id'] == shop_id]

# if (item_id != -1):
#    sales_file = sales_file[sales_file['item_id'] == item_id]

print(sales_file)

    
# Create a list with total sales amounts per month for each observed
print("\nPlease enter the month you want to predict (0-11): ")
month_num = int(input())
if month_num > 11:
    raise ValueError


with open('predicted_sales.csv', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print('item_id, item_cnt_month')
    sys.stdout = original_stdout # Reset the standard output to its original value

for i in range (amount_items):
    sales_file_copy = sales_file[sales_file['item_id'] == items[i]]
    sales_file_copy = sales_file_copy[sales_file_copy['shop_id'] == shops[i]]
    sales_file_copy = sales_file_copy[sales_file_copy['date_block_num'] % 12 == month_num] 

    current_month = -1
    sales_per_month = {}
    for j, row in sales_file_copy.iterrows():
        #print(row['date_block_num'])
        if current_month < row['date_block_num']:
            current_month = row['date_block_num']
            sales_per_month[current_month] = 0
        sales_per_month[current_month] += row['item_cnt_day']

    x = []
    for j in range(len(sales_per_month)):
        x.append(month_num)

    x = numpy.array(x).reshape(-1, 1)

    y = []
    for j in sales_per_month:
        y.append(sales_per_month[j])

    y = numpy.array(y)

   # print ("X: " + str(x))
    #print ("Y: " + str(y))
    # The model

    #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=4)

    try:
        model = MLPRegressor(max_iter = 100000)
        model.fit(x, y)
        prediction = model.predict(x)
    except ValueError:
        prediction = [0]

    #print ("\nPredicted amount of sales: " + str(prediction[0]))
    #sum = 0

    #print("Average: " + str(sum/len(y)))
    #print ("\nAmount of iters: " + str(model.n_iter_))
    #print(i)

    print("Shop number: " + str(shops[i]) + ", item number: " + str(items[i]) + ". Prediction: " + str(prediction[0]))

    with open('predicted_sales.csv', 'a') as f:
        sys.stdout = f # Change the standard output to the file we created.
        print(str(i) + ',' + str(prediction[0]))
        sys.stdout = original_stdout # Reset the standard output to its original value

