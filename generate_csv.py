import pandas as pd
import numpy as np

def generate_advanced_data():
    """
    Generates a mock dataset for the Inventory AI Dashboard.
    Includes advanced metrics for forecasting like Average Daily Sales and Lead Time.
    """
    print("⏳ Generating Advanced Inventory Data...")
    
    n_products = 500 
    np.random.seed(99) # Set seed for reproducibility (ensures data is consistent)

    # 1. Create Main Data Structure
    data = {
        'SKU': [f'ITEM-{i:04d}' for i in range(n_products)],
        'Category': np.random.choice(['Electronics', 'Fashion', 'Home', 'Beauty', 'Toys'], n_products),
        'Stock_Qty': np.random.randint(0, 300, n_products),             # Current stock level
        'Days_Since_Last_Sale': np.random.randint(0, 365, n_products),  # Days since the item was last sold
        'Cost_Price': np.random.uniform(50, 2000, n_products).round(2), # Unit cost
        'Lead_Time_Days': np.random.randint(7, 45, n_products),         # Time required to restock (in days)
    }

    df = pd.DataFrame(data)

    # 2. Calculate Selling Price
    # Simulating a profit margin between 30% and 80%
    df['Current_Price'] = (df['Cost_Price'] * np.random.uniform(1.3, 1.8, n_products)).round(2)

    # 3. Generate 'Average Daily Sales' Logic
    # We create a correlation: 
    # - If an item hasn't sold in a long time, its daily sales rate should be low.
    # - If an item sold recently, its daily sales rate should be high.
    def generate_sales_rate(row):
        if row['Days_Since_Last_Sale'] > 60:
            return np.random.uniform(0, 0.5)  # Dead Stock: Very low sales rate
        elif row['Days_Since_Last_Sale'] < 10:
            return np.random.uniform(2, 10)   # Hot Item: High sales rate
        else:
            return np.random.uniform(0.5, 3)  # Normal Item: Moderate sales rate
            
    df['Avg_Daily_Sales'] = df.apply(generate_sales_rate, axis=1).round(1)

    # 4. Export to CSV
    filename = 'inventory_data.csv'
    df.to_csv(filename, index=False)
    
    print(f"✅ Successfully created '{filename}' with {n_products} items!")
    print(f"   - Included Columns: {list(df.columns)}")

if __name__ == "__main__":
    generate_advanced_data()