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
        "Update Expense",
        "Delete Expense",
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

elif menu == "Delete Expense":
    st.title("Delete Expense")

    data = load_json()

    if not data:
        st.warning("No Expense to Delete")
    else:
        df = pd.DataFrame(data)

        # Select ID
        selected_id = st.selectbox("Select Expense ID to Delete:", df["ID"])

        # Show details of selected expense (read-only)
        expense = df[df["ID"] == selected_id].iloc[0]

        st.subheader("Expense Details")
        st.write(f"**Amount:** ₹{expense['amount']}")
        st.write(f"**Category:** {expense['category']}")
        st.write(f"**Remarks:** {expense['remarks']}")
        st.write(f"**Date:** {expense['date']}")

        # Delete button
        if st.button("Delete Expense"):
            deleted_data = {
                "method": "delete",
                "ID": int(selected_id)
            }

            response = write_json(deleted_data)

            if response.get("status") == "success":
                st.success("Expense deleted successfully!!")
                st.rerun()
            else:
                st.error("Failed to delete expense.")




elif menu == "View Expense":
    st.title("All Expenses")
    data = load_json()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True)
    else:
        st.warning("No Expenses are added yet.")


elif menu == "Update Expense":
    st.title("Update Expense")
    data = load_json()

    if not data:
        st.warning("No Expense to Update")

    else:
        df = pd.DataFrame(data)

        selected_id = st.selectbox("Select Expense ID to Update:",  df["ID"])

        expense = df[df["ID"] ==selected_id].iloc[0]

        st.subheader("Edit Fields: ")

        new_amount = st.number_input("Amount",min_value=1, value = int(expense["amount"]))

        category = st.selectbox("Category", ALLOWED_CATEGORIES,index=ALLOWED_CATEGORIES.index(expense["category"]))

        new_remarks = st.text_input(
            "Remarks",
            value=expense["remarks"]
        )

        new_date = st.date_input(
            "Date",
            value=datetime.strptime(expense["date"], "%Y-%m-%d")
        )

        if st.button("Update Expense"):
            updated_data = {
                "method": "update",
                "ID": int(expense["ID"]),
                "amount": new_amount,
                "category": category,
                "remarks": new_remarks,
                "date": new_date.strftime("%Y-%m-%d")
            }

            response = write_json(updated_data)

            if response.get("status") == "success":
                st.success("Expense updated successfully!")
            else:
                st.error("Failed to update expense.")


elif menu == "Category Summary":
    st.title("Total Expense by Category")
    data = load_json()

    if data:
        df = pd.DataFrame(data)
        summary = df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(data=summary,x="category",y="amount",x_label="Category",y_label="Amount",color="#ffaa00")
        st.dataframe(summary, hide_index=True)

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
        st.dataframe(summary, hide_index=True)
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

    st.dataframe(df,hide_index=True)

elif menu == "Export CSV":
    st.title("Export All Expenses")

    data = load_json()
    df = pd.DataFrame(data)

    st.subheader("Preview")
    st.dataframe(df, hide_index= True)

    # # Create CSV
    csv = df.to_csv(index=False).encode('utf-8')

    # # Download button
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="expenses_export.csv",
        mime="text/csv"
    )
