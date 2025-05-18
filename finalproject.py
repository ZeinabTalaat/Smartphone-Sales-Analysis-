import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


file_path = r"C:\Users\Rawan\Documents\smartphone_sales_dataset.csv"
df = pd.read_csv(file_path)
print("🔍 Preview of data:")
print(df.head())

print("\nℹ Initial Data Info:")
df.info()

print("\n! Missing Values:")
print(df.isnull().sum())

text_columns = ['Brand', 'OS']
for col in text_columns:
    df[col] = df[col].astype(str).str.strip().str.lower()
# حذف الصفوف التي تحتوي على قيم مفقودة
df.dropna(inplace=True)

# التأكد من أن التقييم بين 1 و 5
df = df[df['Rating'].between(1, 5)]

# التأكد من أن القيم الرقمية موجبة
numeric_cols = ['RAM_GB', 'Storage_GB', 'Screen_Size', 'Price_USD', 
                'Battery_mAh', 'Quantity_Sold', 'Sales_Revenue', 'Profit']
for col in numeric_cols:
    df = df[df[col] > 0]

Q1 = df['Price_USD'].quantile(0.25)
Q3 = df['Price_USD'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['Price_USD'] >= Q1 - 1.5 * IQR) & (df['Price_USD'] <= Q3 + 1.5 * IQR)]

# إعادة تعيين الفهرس
df.reset_index(drop=True, inplace=True)

# فحص نهائي
print("\n✅ Cleaned Data Summary:")
print(df.describe())

print("\n📋 Final Data Info:")
df.info()

total_revenue = df['Sales_Revenue'].sum()
print("✅ Total Sales Revenue: $", total_revenue)

# إجمالي الربح
total_profit = df['Profit'].sum()
print("✅ Total Profit: $", total_profit)


units_sold_per_brand = df.groupby('Brand')['Quantity_Sold'].sum().sort_values(ascending=False)
print("✅ Number of units sold per Brand:\n", units_sold_per_brand)

avg_price_per_brand = df.groupby('Brand')['Price_USD'].mean()
print("✅ Average price per Brand:\n", avg_price_per_brand)

top_rated_phone = df.loc[df['Rating'].idxmax()]
print("✅ Top-rated phone:\n", top_rated_phone[['Phone_ID', 'Brand', 'Rating']])

avg_rating_per_os = df.groupby('OS')['Rating'].mean()
print("✅ Average rating per OS:\n", avg_rating_per_os)

most_profitable_phones = df[['Phone_ID', 'Brand', 'Profit']].sort_values(by='Profit', ascending=False)
print("✅ Most profitable phones:\n", most_profitable_phones.head())

df['Profit_Per_Unit'] = df['Profit'] / df['Quantity_Sold']
avg_profit_per_unit = df['Profit_Per_Unit'].mean()
print("✅ Average profit per unit sold: $", avg_profit_per_unit)


comparison = df.groupby('OS').agg({'Sales_Revenue': 'sum', 'Profit': 'sum', 'Quantity_Sold': 'sum'})
print("✅ Comparison of Android vs iOS:\n", comparison)

correlation_ram_sales = df['RAM_GB'].corr(df['Quantity_Sold'])
print("✅ Correlation between RAM and Sales:", correlation_ram_sales)

#VISULAIZATION

sales_by_brand = df.groupby ("Brand")["Sales_Revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(10 , 6))
plt.bar(sales_by_brand.index, sales_by_brand.values, color="#7CB9E8")
plt.xlabel("Brand")
plt.ylabel("Revenue")
plt.title("Total Revenue")
plt.show()

# Phones sold per Brand
plt.figure(figsize=(10 , 6))
plt.bar(units_sold_per_brand .index, units_sold_per_brand.values, color="#6699CC")
plt.xlabel("Brand")
plt.ylabel("Sales")
plt.title("Total Sales")
plt.show()

# Profits per Brand
profits_by_brand = df.groupby ("Brand")["Profit"].sum().sort_values(ascending=False)
plt.figure(figsize=(10 , 6))
plt.bar(profits_by_brand.index, profits_by_brand.values, color="#5D8AA8")
plt.xlabel("Brand")
plt.ylabel("Profit")
plt.title("Total Profits")
plt.show()

#Correlation Between RAM_GB and Quantity sold
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df,
    x="RAM_GB",
    y="Quantity_Sold",
    color="#4A90E2",  
    s=40              
)
plt.title("Relationship between RAM and Quantity Sold")
plt.xlabel("RAM (GB)")
plt.ylabel("Quantity Sold")
plt.show()

#Correlation between Battery size and sales
correlation_battery_sales = df['Battery_mAh'].corr(df['Quantity_Sold'])
plt.figure(figsize=(10,6))
scatter = plt.scatter(
    df['Battery_mAh'],             
    df['Quantity_Sold'],          
    c=df['Price_USD'],                 
    s=50,           
    cmap='ocean',                                        
    edgecolors='white'
              
)
plt.title("Relationship between Battery and Quantity Sold")
plt.xlabel("Battery (mAH)")
plt.ylabel("Quantity Sold")
plt.colorbar(scatter, label="Price_USD")
plt.tight_layout()
plt .show()

#OS Average Rating 
plt.figure(figsize=(10 , 6))
colors = ['#7CB9E8', '#6699CC']  
plt.pie(avg_rating_per_os , labels=['IOS' , 'Andoroid'] , autopct ='%1.1f%%'  , startangle=90 , colors=colors) 
plt.axis('equal')
plt.title("Average Rating Per OS")
plt.show()

# correlation between Price and Qantity Sold

sns.lmplot(
                data=df,
                x='Price_USD', 
                y='Quantity_Sold', 
                height=5,
                aspect=1.5,
                scatter_kws={'alpha':0.5, 'color': '#76ABDF'},
                line_kws={'color': '#003399'}
                )
plt.title("Correlation between price and sales")
plt.xlabel("Price (USD)")
plt.ylabel("Quantity Sold")
plt.show()

# Comparison between iOS and Android 

#Profit
profit_per_os = df.groupby('OS')['Profit'].sum()
plt.figure(figsize=(8, 5))
colors = ['#5072A7', '#5D8AA8']  
profit_per_os.plot(kind='bar', color=colors , width=0.3)
plt.title('Comparison of Profit: Android vs iOS')
plt.xlabel('Operating System')
plt.ylabel('Total Profit')
plt.tight_layout()
plt.show()

#Sales Revenue
revenue_per_os = df.groupby('OS')['Sales_Revenue'].sum()
plt.figure(figsize=(8, 5))
colors = ['#5072A7', '#5D8AA8']  
profit_per_os.plot(kind='bar', color=colors, width=0.3 )
plt.title('Comparison of Sales Revenue : Android vs iOS')
plt.xlabel('Operating System')
plt.ylabel('Sales Revenue')
plt.tight_layout()
plt.show()

#Quantity Sold
revenue_per_os = df.groupby('OS')['Quantity_Sold'].sum()
plt.figure(figsize=(8, 5))
colors = ['#5072A7', '#5D8AA8']  
profit_per_os.plot(kind='bar', color=colors, width=0.3 )
plt.title('Comparison of Sales  : Android vs iOS')
plt.xlabel('Operating System')
plt.ylabel('Sales ')
plt.tight_layout()
plt.show()