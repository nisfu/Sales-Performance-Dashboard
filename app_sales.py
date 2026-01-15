import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Sales Dashboard", layout="wide")
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'data_penjualan.csv')

# --- LOAD DATA ---
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df['Tgl'] = pd.to_datetime(df['Tgl'])
else:
    st.error(f"File tidak ditemukan di: {csv_path}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("Filter Data")
kategori = st.sidebar.multiselect(
    "Pilih Kategori:",
    options=df['Kategori'].unique(),
    default=df['Kategori'].unique()
)

df_selection = df.query("Kategori == @kategori")

# --- MAIN PAGE ---
st.title("📊 Sales Performance Dashboard")
st.markdown("##")

# TOP KPI's (Ringkasan Angka)
total_sales = int(df_selection['Penjualan'].sum())
average_sale = int(df_selection['Penjualan'].mean())

col1, col2 = st.columns(2)
with col1:
    st.subheader("Total Penjualan:")
    st.subheader(f"Rp {total_sales:,}")
with col2:
    st.subheader("Rata-rata Penjualan:")
    st.subheader(f"Rp {average_sale:,}")

st.markdown("---")

# GRAFIK 1: Penjualan Berdasarkan Kategori (Bar Chart)
# --- UPDATE KODE GRAFIK 1 ---
# Tambahkan numeric_only=True agar kolom tanggal tidak ikut dijumlahkan
sales_by_category = df_selection.groupby(by=['Kategori']).sum(numeric_only=True)[['Penjualan']].sort_values(by='Penjualan')

fig_product_sales = px.bar(
    sales_by_category,
    x='Penjualan',
    y=sales_by_category.index,
    orientation='h',
    title="<b>Penjualan Berdasarkan Kategori</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_category),
    template="plotly_white",
)

# --- UPDATE KODE GRAFIK 2 --- Tren Penjualan per Bulan (Line Chart)
# Lakukan hal yang sama untuk tren waktu
sales_by_date = df_selection.groupby(by=['Tgl']).sum(numeric_only=True)[['Penjualan']]

fig_line = px.line(
    sales_by_date,
    x=sales_by_date.index,
    y='Penjualan',
    title="<b>Tren Penjualan Waktu ke Waktu</b>",
    template="plotly_white",
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_line, use_container_width=True)