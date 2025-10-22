# Name: Antonio Khemmoro 
# Student ID: 71867697
# Email: khemmoro@umich.edu 

import csv
# Load CSV Data (Collaborated together)
def read_csv_file(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # reads each row as a dictionary
        for row in reader:
            # convert numeric strings to float for math later
            row['Profit'] = float(row['Profit'])
            row['Sales'] = float(row['Sales'])
            row['Discount'] = float(row['Discount'])
            data.append(row)  # add the cleaned-up row to the list
    return data

# ANTONIO FUNCTION 1 
def calculate_avg_sales_by_category(superstore_data):
    category_totals = {} # track total sales per category
    category_counts = {} # track how many entries per category

    for row in superstore_data:
        category = row['Category']
        sales = row['Sales']
        category_totals[category] = category_totals.get(category, 0) + sales
        category_counts[category] = category_counts.get(category, 0) + 1

    avg_sales = {} # average = total / count
    for cat in category_totals:
        avg_sales[cat] = round(category_totals[cat] / category_counts[cat], 2)

    return avg_sales # dictionary of average sales by category

# ANTONIO FUNCTION 2
def calculate_percent_profitable(superstore_data):
    total_orders = len(superstore_data)
    profitable_orders = sum(1 for row in superstore_data if row['Profit'] > 0)  # only count positive profit
    return round((profitable_orders / total_orders) * 100, 2)  # percent of profitable orders

# Add Matthew's Function calulations

# MATTHEW FUNCTION 1
def calculate_avg_profit_by_region(superstore_data):
    region_totals = {}  # track total profit by region
    region_counts = {}  # track how many entries per region

    for row in superstore_data:
        region = row['Region']
        profit = row['Profit']
        region_totals[region] = region_totals.get(region, 0) + profit  # add profit to region total
        region_counts[region] = region_counts.get(region, 0) + 1       # add to count of rows for region

    avg_profit = {}
    for region in region_totals:
        avg_profit[region] = round(region_totals[region] / region_counts[region], 2)  # calculate average

    return avg_profit  # dictionary of average profit per region


# MATTHEW FUNCTION 2
def calculate_percent_discounted(superstore_data):
    total_orders = len(superstore_data)  # count how many rows total
    discounted_orders = sum(1 for row in superstore_data if row['Discount'] > 0)  # count how many had a discount
    return round((discounted_orders / total_orders) * 100, 2)  # percent of orders with discount

# WRITE RESULTS TO FILE
def generate_report(avg_profit, percent_discounted, avg_sales, percent_profitable):
    with open("superstore_results.txt", "w") as f:
        f.write("Matthew’s Calculations\n")
        f.write("Average Profit by Region:\n")
        for region, profit in avg_profit.items():
            f.write(f"{region}: ${profit}\n")
        f.write(f"\nPercentage of Orders with Discount > 0: {percent_discounted}%\n\n")

        f.write("Antonio’s Calculations\n")
        f.write("Average Sales by Category:\n")
        for cat, sales in avg_sales.items():
            f.write(f"{cat}: ${sales}\n")
        f.write(f"\nPercentage of Orders with Profit > 0: {percent_profitable}%\n")
