# Name: Antonio Khemmoro test
# Student ID: 12345678
# Email: khemmoro@umich.edu 

def calculate_avg_sales_by_category(superstore_data):
    category_totals = {}
    category_counts = {}

    for row in superstore_data:
        category = row['Category']
        sales = row['Sales']
        category_totals[category] = category_totals.get(category, 0) + sales
        category_counts[category] = category_counts.get(category, 0) + 1

    avg_sales = {}
    for cat in category_totals:
        avg_sales[cat] = round(category_totals[cat] / category_counts[cat], 2)

    return avg_sales
