# Name: Antonio Khemmoro 
# Student ID: 71867697
# Email: khemmoro@umich.edu 


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
