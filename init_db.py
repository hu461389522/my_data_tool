import sqlite3
import pandas as pd

# 1. 读取你的Excel
df = pd.read_excel(r"C:\Users\Administrator\Desktop\test.xlsx")

# 2. 连接数据库（如果没有会自动创建）
conn = sqlite3.connect('business_data.db')

# 3. 把DataFrame存成数据库表（表名叫 sales）
df.to_sql('sales', conn, if_exists='replace', index=False)

conn.close()
print("✅ 数据已成功导入数据库！")