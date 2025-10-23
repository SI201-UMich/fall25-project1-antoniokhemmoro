# Name: Antonio Khemmoro 
# Student ID: 71867697
# Email: khemmoro@umich.edu
# Collaborators: Matthew Khemmoro
# Collaborated equally on this project. Each wrote two distinct calculations:
# Antonio: calculate_avg_sales_by_category(superstore_data), calculate_percent_profitable(superstore_data)
# Matthew: calculate_avg_discount_by_region(superstore_data):, calculate_percent_discounted()
# Also, we both worked together on the shared components of the script:
# - _to_float(): for handling blanks
# - read_csv_file(): for loading and preprocessing the data
# - generate_report(): for formatting the output
# - main(): for orchestrating the program execution
# AI usage: Used ChatGPT to help handle null/NA values in numeric fields, debugging, 
# and assist with writing parts of the tougher calculations and functions.
import csv
# Load CSV Data (Collaborated together)
def read_csv_file(filename):
    data = [] 
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)  # reads each row as a dictionary
        for row in reader:
            # convert numeric strings to float for math later (NA-safe)
            row['Profit'] = _to_float(row.get('Profit'))
            row['Sales'] = _to_float(row.get('Sales'))
            row['Discount'] = _to_float(row.get('Discount'))
            row['Quantity'] = _to_float(row.get('Quantity'))
            # normalize strings we reference (avoid None)
            for k in ['Category', 'Segment', 'Ship Mode', 'Region', 'Country', 'Sub-Category', 'State']:
                row[k] = '' if row.get(k) is None else str(row.get(k)).strip()
            data.append(row)  # add the cleaned-up row to the list
    return data

# ANTONIO FUNCTION 1 (Average Sales by Category but only for rows in the 'Consumer' Segment)
def calculate_avg_sales_by_category(superstore_data):
    category_totals = {} # track total sales per category (Consumer segment only)
    category_counts = {} # track how many entries per category (Consumer segment only)

    for row in superstore_data:
        category = row['Category']
        sales = row['Sales']
        segment = row['Segment']
        if category and segment == 'Consumer' and sales is not None:  
            category_totals[category] = category_totals.get(category, 0.0) + sales
            category_counts[category] = category_counts.get(category, 0) + 1

    avg_sales = {} # average = total / count
    for cat in category_totals:
        count = category_counts[cat]
        if count > 0:
            avg_sales[cat] = round(category_totals[cat] / count, 2)

    return avg_sales # dictionary of average sales by category (Consumer only)

# ANTONIO FUNCTION 2 (Percent of orders with Profit > 0 among orders that have Quantity > 0 
# and are in specific Segments)
def calculate_percent_profitable(superstore_data):
    valid_orders = 0      # only rows with real quantity in chosen segments
    profitable_orders = 0 # among those count strictly positive profit
    for row in superstore_data:
        profit  = row['Profit']
        qty     = row['Quantity']
        segment = row['Segment']
        if segment not in {'Consumer', 'Corporate'}:
            continue
        # need a real quantity and profit value
        if qty is None or qty <= 0 or profit is None:
            continue
        valid_orders += 1
        if profit > 0:
            profitable_orders += 1
    # percent of qualifying orders with positive profit
    return round((profitable_orders / valid_orders) * 100, 2) if valid_orders > 0 else 0.0


# Add Matthew's Function calulations

# MATTHEW FUNCTION 1
# Average Discount by Region for rows in the United States.

def calculate_avg_discount_by_region(superstore_data):
    region_totals = {}  # track total discount by region (US only)
    region_counts = {}  # track how many entries per region (US only)

    for row in superstore_data:
        region = row['Region']
        country = row['Country']
        disc = row['Discount']
        if country == 'United States' and region != '' and disc is not None:
            region_totals[region] = region_totals.get(region, 0.0) + disc  # add discount to region total
            region_counts[region] = region_counts.get(region, 0) + 1       # add to count of rows for region

    avg_discount = {}
    for region in region_totals:
        count = region_counts[region]
        if count > 0:
            avg_discount[region] = round(region_totals[region] / count, 4)  # calculate average (discount is fractional)

    return avg_discount  # dictionary of average discount per region (US only)



# MATTHEW FUNCTION 2
#Calculates the percentage of discounted orders in CA, TX, NY, and FL for specific product types (Chairs, Phones, Binders, Paper)
def calculate_percent_discounted(superstore_data):
    valid = 0      # total qualifying orders
    discounted = 0 # qualifying orders with a discount

    for row in superstore_data:
        disc = row.get("Discount")
        state = row.get("State", "")
        subcat = row.get("Sub-Category", "")

        # only include orders from these states
        if state not in {"California", "Texas", "New York", "Florida"}:
            continue
        # only include these product types
        if subcat not in {"Chairs", "Phones", "Binders", "Paper"}:
            continue
        # skip if discount value is missing
        if disc is None:
            continue
        valid += 1
        if disc > 0:
            discounted += 1

    # return percent of qualifying orders with discount > 0
    return round((discounted / valid) * 100, 2) if valid > 0 else 0.0


# WRITE RESULTS TO FILE
def generate_report(avg_discount_by_region, percent_discounted, avg_sales_consumer, percent_profitable_qty_ship):
    with open("superstore_results.txt", "w", encoding='utf-8') as f:
        f.write("Matthew’s Calculations\n")
        f.write("Average Discount by Region (Country = United States):\n")
        for region, avg_disc in avg_discount_by_region.items():
            f.write(f"{region}: {avg_disc}\n")
        f.write("\nPercentage of Orders with Discount > 0 ")
        f.write("(States = CA, TX, NY, FL; Sub-Categories = Chairs, Phones, Binders, Paper): ")
        f.write(f"{percent_discounted}%\n\n")

        f.write("Antonio’s Calculations\n")
        f.write("Average Sales by Category (Segment = Consumer only):\n")
        for cat, sales in avg_sales_consumer.items():
            f.write(f"{cat}: ${sales}\n")
        f.write(f"\nPercentage of Orders with Profit > 0 (Segments = Consumer, Corporate; Quantity > 0): {percent_profitable_qty_ship}%\n")


def main():
    superstore_data = read_csv_file("SampleSuperstoreSample.csv")  # load the CSV file
    # Matthew 1
    avg_discount_by_region = calculate_avg_discount_by_region(superstore_data)  # average discount per region (US only)
    # Matthew 2
    percent_discounted = calculate_percent_discounted(superstore_data)  # percent of orders with discount > 0 (specific states + subcats)
    # Antonio 1
    avg_sales_consumer = calculate_avg_sales_by_category(superstore_data)  # average sales by category (Consumer only)
    # Antonio 2
    percent_profitable_qty_ship = calculate_percent_profitable(superstore_data)  # percent profitable with qty > 0 in segments {Consumer, Corporate}

    generate_report(avg_discount_by_region, percent_discounted, avg_sales_consumer, percent_profitable_qty_ship)  # write results to txt
if __name__ == "__main__":
    main()  