import streamlit as st
from main_final import ALLOWED_CATEGORIES, Month_Name, load_json, write_json
from datetime import datetime
import pandas as pd

st.header("💰My Expense Tracker")
st.subheader("Welcome to my personal Expense Tracker")

st.sidebar.title("Expense Tracker Menu")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Add Expense",
        "View Expense",
        "Export CSV",
        "Filter Data",
        "Category Summary",
        "Month Summary"
     ]
)

if menu == "Add Expense":
    st.title("Add New Expense")
    amount = st.number_input("Amount", min_value= 1)
    category = st.selectbox("Category", ALLOWED_CATEGORIES)
    remarks = st.text_input("Remarks")

    if st.button("Add Expense"):
        new_expense = {
            "amount" : amount,
            "category" : category,
            "remarks" : remarks,
            "date" : datetime.now().strftime("%Y-%m-%d")
        }
        
        response = write_json(new_expense)

        if response["message"] == 'Expense already exists':
            st.warning("Expense Already Added.")
        else:
            st.success("Expense Added Successfully!!")

elif menu == "View Expense":
    st.title("All Expenses")
    data = load_json()
    if data:
        st.table(data)
    else:
        st.warning("No Expenses are added yet.")


elif menu == "Category Summary":
    st.title("Total Expense by Category")
    data = load_json()

    if data:
        df = pd.DataFrame(data)
        summary = df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(data=summary,x="category",y="amount",x_label="Category",y_label="Amount",color="#ffaa00")
        st.table(summary)
    else:
        st.warning("No Data Available")

elif menu == "Month Summary":
    st.title("Total Expense by Months")
    data = load_json()

    if data:
        df = pd.DataFrame(data)
        df["month_name"] = df["date"].apply(
            lambda x: Month_Name[int(x.split("-")[1])-1]
        )
        summary = df.groupby("month_name")["amount"].sum().reset_index()
        st.bar_chart(data=summary,x="month_name",y="amount",x_label="Months",y_label="Amount",color="#ffaa00")
        st.table(summary)
    else:
        st.warning("No Data Available")


#for single select
# elif menu == "Filter Data":
#     st.title("Filter Expenses")
#     filter_type = st.radio("Filter by ",["Category","Month","Both"])
#     data = load_json()

#     df = pd.DataFrame(data)
#     if filter_type == "Month" or filter_type == "Both":
#         choose_month = st.selectbox("Select Month",Month_Name)
#         df["month_name"] = df["date"].apply(
#             lambda x: Month_Name[int(x.split("-")[1])-1]
#         )
#         df = df[df["month_name"]==choose_month]

#     if filter_type == "Category" or filter_type == "Both":
#         choose_category = st.selectbox("Select Category", ALLOWED_CATEGORIES)
#         df = df[df["category"] == choose_category]

#     st.table(df)


elif menu == "Filter Data":
    st.title("Filter Expenses")
    data = load_json()
    df = pd.DataFrame(data)
    df["month_name"] = df["date"].apply(
            lambda x: Month_Name[int(x.split("-")[1])-1]
        )
    
    selected_months = st.multiselect("Select months", Month_Name)
    if selected_months:
        df = df[df["month_name"].isin(selected_months)]
    selected_categories = st.multiselect("Select Categories", ALLOWED_CATEGORIES)
    if selected_categories:
        df = df[df["category"].isin(selected_categories)]

    st.table(df)

elif menu == "Export CSV":
    st.title("Export All Expenses")

    data = load_json()
    df = pd.DataFrame(data)

    st.subheader("Preview")
    st.dataframe(df)

    # # Create CSV
    csv = df.to_csv(index=False).encode('utf-8')

    # # Download button
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="expenses_export.csv",
        mime="text/csv"
    )
