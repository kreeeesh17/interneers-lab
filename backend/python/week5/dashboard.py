import streamlit as st
import pandas as pd
from week4.db_connection import initialize_mongo
from week4.models import Product, ProductCategory
from decimal import Decimal


initialize_mongo()


# page settings
st.set_page_config(page_title="Week 5 Inventory Dashboard", layout="wide")
st.title("Week 5: Interactive Data Tools")
st.write("Streamlit dashboard connected directly to MongoDB using MongoEngine")


# helpers
def get_all_categories():
    return list(ProductCategory.objects().order_by("title"))


def fetch_products(selected_category_id=None):
    if selected_category_id is None:
        products = Product.objects()
    else:
        products = Product.objects(category=selected_category_id)

    rows = []

    for product in products:
        rows.append({
            "ID": product.id,
            "Name": product.name,
            "Description": product.description,
            "Price": product.price,
            "Brand": product.brand,
            "Quantity": product.quantity,
            "Category": product.category.title
        })

    return pd.DataFrame(rows)


# creating sidebar category filter
st.sidebar.header("Filter Inventory")

all_category = get_all_categories()
# creating dictionary where all maps to none so that no conflict arises
category_options = {"All": None}

for category in all_category:
    category_options[category.title] = category.id

selected_category_title = st.sidebar.selectbox(
    "Select Product Category", list(category_options.keys()))

selected_category_id = category_options[selected_category_title]


# showing inventory table for current id
@st.fragment
def inventory_table(category_id):
    st.subheader("Current Inventory")
    df = fetch_products(category_id)
    if df.empty:
        st.info("No products found in this category")
    else:
        st.dataframe(df, use_container_width=True)
    return df


# showing stock alert
@st.fragment
def stock_alert(df):
    st.subheader("Stock Alert")
    if not df.empty:
        low_stock_row = []
        for index, row in df.iterrows():
            if row["Quantity"] < 5:
                low_stock_row.append(row)
        low_stock_df = pd.DataFrame(low_stock_row)

        if not low_stock_df.empty:
            st.error("Some products are running low in stock")
            st.dataframe(low_stock_df, use_container_width=True)
        else:
            st.success("No products are running low in stock")
    else:
        st.info("No products found in this category")


df = inventory_table(selected_category_id)
stock_alert(df)
