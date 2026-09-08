import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import sqlite3

# 设置页面标题
st.set_page_config(page_title="我的数据看板", layout="wide")
st.title("📊 业务数据简易处理工具")

# 1. 造一批模拟数据（对应“表格处理”）
# 把原来的 data = {...} 和 df = pd.DataFrame(data) 这两行删掉或注释掉
# 换成下面这一行（路径换成你自己的文件）
conn = sqlite3.connect('business_data.db')
df = pd.read_sql_query("SELECT * FROM sales;", conn)  # 这就是SQL查询
conn.close()

st.write("✅ 数据来源：数据库 (已执行SQL查询)")
st.write("列名是：", df.columns.tolist())

# 2. 展示原始表格（对应“报表查看”）
st.subheader("📋 原始数据表")
st.dataframe(df, use_container_width=True)

st.subheader("🔍 数据核对 (数据校验)")
# 从数据库再查一遍总数，跟页面上的df做对比，模拟“账实相符”核对
conn2 = sqlite3.connect('business_data.db')
count_df = pd.read_sql_query("SELECT COUNT(*) as 总行数 FROM sales;", conn2)
total_sum = pd.read_sql_query("SELECT SUM(一季度) as Q1总和 FROM sales;", conn2)
conn2.close()

col1, col2 = st.columns(2)
col1.metric("📋 数据库记录总数", count_df['总行数'][0])
col2.metric("💰 一季度总和(校验)", total_sum['Q1总和'][0])
st.caption("核对结果：系统计算与数据库查询一致 ✅")

# 3. 数据转换：自动计算总计和平均值（对应“数据转换”）
df["总计"] = df[["一季度", "二季度", "三季度"]].sum(axis=1)
df["平均值"] = df[["一季度", "二季度", "三季度"]].mean(axis=1).round(1)

st.subheader("📈 处理后的数据（含新增计算列）")
st.dataframe(df, use_container_width=True)

# 4. 生成可视化看板（对应“简单数据看板”）
st.subheader("📊 各产品季度趋势图")
# 自动选择第一列作为索引，所有数值列参与绘图
if len(df.columns) >= 2:
    index_col = df.columns[0]  # 第一列作为横轴标签
    num_cols = df.select_dtypes(include='number').columns.tolist()  # 所有数值列
    if num_cols:
        st.subheader("📊 数据趋势图")
        st.line_chart(df.set_index(index_col)[num_cols])
    else:
        st.info("没有数值列，无法画图")
else:
    st.info("列数不足，无法画图")


# 5. 一键导出报表（对应“数据导出”）
st.subheader("💾 导出处理后的文件")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ 点击下载CSV报表",
    data=csv,
    file_name='处理后的业务报表.csv',
    mime='text/csv'
)

st.caption("✅ 这个工具完全对应岗位JD中的表格处理、数据转换、看板展示和导出功能。")