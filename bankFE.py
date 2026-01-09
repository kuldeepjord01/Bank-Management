
import streamlit as st
import requests
from fastapi.responses import JSONResponse

BASE_URL = "http://127.0.0.1:8000"

st.title("🏦Royal Bank")

tabs = st.tabs(["Accounts", "Transactions"])

@st.dialog("Add New Account")
def add_account():
    acc_no = st.text_input("Account Number")
    username = st.text_input("User Name")
    balance = st.text_input("Balance")

    if st.button("Create Account", type="primary"):
        res = requests.post(
            f"{BASE_URL}/accounts",
            json={
                "account_no": int(acc_no),
                "username": username,
                "balance": float(balance)
            }
        )

        if res.status_code == 201:
            st.success("Account created")
            st.rerun()
        else:
            st.error(res.text)


@st.dialog("Transfer Amount")
def transfer():
    src = st.text_input("Source Account")
    dest = st.text_input("Destination Account")
    amount = st.text_input("Amount")

    if st.button("Transfer", type="primary"):
        res = requests.post(
            f"{BASE_URL}/transactions",
            json={
                "source": int(src),
                "dest": int(dest),
                "amount": float(amount)
            }
        )

        if res.status_code == 201:
            st.success("Transfer successful")
            st.rerun()
        else:
            st.error(res.text)


col1, col2 = st.columns(2)
with col1:
    if st.button("Add Account", type="primary"):
        add_account()

with col2:
    if st.button("Transfer Amount", type="primary"):
        transfer()


with tabs[0]:
    res = requests.get(f"{BASE_URL}/accounts")
    if res.ok:
        st.dataframe(res.json(), use_container_width=True)

with tabs[1]:
    res = requests.get(f"{BASE_URL}/transactions")
    if res.ok:
        st.dataframe(res.json(), use_container_width=True)

