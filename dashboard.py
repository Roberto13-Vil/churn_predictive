import streamlit as st
import pandas as pd
import plotly.express as px
from utils import predict_churn

st.set_page_config(page_title="Churn Dashboard", layout="wide")

if "stage_index" not in st.session_state:
    st.session_state.stage_index = 0

stages = ["📊 Overview", "❗Dissatisfaction", "📞 Frequency", "🌟 Importance", "📈 Evaluation Neuronal Network", "🧠 Churn Prediction"]

col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button("⬅️ Previous"):
        if st.session_state.stage_index > 0:
            st.session_state.stage_index -= 1
        else:
            st.session_state.stage_index = len(stages) - 1

with col_nav3:
    if st.button("Next ➡️"):
        if st.session_state.stage_index < len(stages) - 1:
            st.session_state.stage_index += 1
        else:
            st.session_state.stage_index = 0

stage = stages[st.session_state.stage_index]

st.markdown(f"<h2 style='text-align: center;'>{stage}</h2>", unsafe_allow_html=True)
st.divider()

df = pd.read_csv('Data/viz_ready.csv')

if stage == "📊 Overview":
    col1, col2 = st.columns([1.5, 1])
    with col1:
        count_churn = df['has_churned'].value_counts().reset_index()
        count_churn.columns = ['class', 'count']
        fig = px.pie(
            count_churn,
            names='class',
            values='count',
            color='class',
            color_discrete_map={'Churn': "red", 'No Churn': "blue"},
            hole=0.4,
            opacity=0.6
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        total = len(df)
        churned = df[df['has_churned'] == 'Churn'].shape[0]
        st.metric("Total Clients", total)
        st.metric("Churn Clients", churned)
        st.metric("Churn Rate", f"{churned / total * 100:.2f}%")

elif stage == "❗Dissatisfaction":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg = df.groupby('has_churned')['failed_call_count'].mean()
        st.metric("Avg Failed Calls (Churn)", f"{avg.get('Churn', 0):.1f}")
    with col2:
        high_failed = df[df['failed_call_count'] > 5]
        perc = (high_failed['has_churned'] == 'Churn').mean() * 100
        st.metric("Churn % ( >5 Failed Calls)", f"{perc:.1f}%")
    with col3:
        complaints = df[df['submitted_complaint'] == 'Yes']
        st.metric("Total Complaints", len(complaints))
    with col4:
        churned_complaints = complaints[complaints['has_churned'] == 'Churn']
        percent = len(churned_complaints) / len(complaints) * 100 if len(complaints) > 0 else 0
        st.metric("Complaint Churn %", f"{percent:.1f}%")
    colA, colB = st.columns(2)
    with colA:
        fig = px.histogram(df, x='failed_call_count', color='has_churned', barmode='overlay',
                           title="Failed Call Distribution",
                           color_discrete_map={"Churn": "red", "No Churn": "blue"}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        fig = px.histogram(df, x='submitted_complaint', color='has_churned', barmode='group',
                           title="Complaints Distribution",
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

elif stage == "📞 Frequency":
    colA, colB, colC = st.columns(3)
    with colA:
        avg = df.groupby('has_churned')['call_count'].mean()
        st.metric("Avg Call Count (Churn)", f"{avg.get('Churn', 0):.1f}")
        fig = px.histogram(df, x='call_count', color='has_churned', barmode='overlay',
                           title='Call Count',
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        low_sms = df[df['sms_count'] < 5]
        churn_low = (low_sms['has_churned'] == 'Churn').mean() * 100
        st.metric("Churn % ( <5 SMS)", f"{churn_low:.1f}%")
        fig = px.histogram(df, x='sms_count', color='has_churned', barmode='overlay',
                           title='SMS Count',
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
    with colC:
        contacts = df.groupby('has_churned')['unique_contacts_called'].mean()
        st.metric("Avg Unique Contacts (Churn)", f"{contacts.get('Churn', 0):.1f}")
        fig = px.histogram(df, x='unique_contacts_called', color='has_churned', barmode='overlay',
                           title='Unique Contacts Called',
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

elif stage == "🌟 Importance":
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x="months_as_customer", color="has_churned", barmode='overlay',
                           title="Customer Tenure (Months)",
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
        fig = px.histogram(df, x='customer_value', color="has_churned", barmode='overlay',
                           title='Customer Value',
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="billing_level", color="has_churned", barmode='group',
                           title="Billing Level",
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
        fig = px.histogram(df, x="plan_type", color="has_churned", barmode='group',
                           title="Plan Type",
                           color_discrete_map={"Churn": 'red', "No Churn": 'blue'}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

elif stage == "📈 Evaluation Neuronal Network":
    df_eval = pd.read_csv("Outputs/Tables/evaluation_model.csv")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_eval)
    with col2:
        st.image("Outputs/Figures/confusion_matrix.png")

elif stage == '🧠 Churn Prediction':
    col1, col2 = st.columns(2)

    with col1:
        failed_call_count = st.number_input("❌ Failed Call Count", min_value=0, step=1)
        submitted_complaint = st.selectbox("📩 Submitted Complaint?", ["No", "Yes"])
        months_as_customer = st.number_input("📅 Months as Customer", min_value=0, step=1)
        billing_level = st.selectbox("💰 Billing Level", [
            "Very Low", "Low", "Mid-Low", "Medium", "Mid-High", "High",
            "High+", "Very High", "Premium", "VIP"
        ])
        call_count = st.number_input("📞 Call Count", min_value=0, step=1)

    with col2:
        sms_count = st.number_input("💬 SMS Count", min_value=0, step=1)
        plan_type = st.selectbox("📶 Plan Type", ["Pay as you go", "Contractual"])
        account_status = st.selectbox("⚙️ Account Status", ["Active", "No Active"])
        age = st.number_input("🎂 Age", min_value=10, max_value=100, step=1)
        customer_value = st.slider("⭐ Customer Value", min_value=0, max_value=2175, step=1)

    billing_level_map = {
        "Very Low" : 0, "Low" : 1, "Mid-Low" : 2, "Medium" : 3, "Mid-High" : 4,
        "High" : 5, "High+" : 6, "Very High" : 7, "Premium" : 8, "VIP" : 9
    }

    input_data = {
        "failed_call_count": [failed_call_count],
        "submitted_complaint": [1 if submitted_complaint == "Yes" else 0],
        "months_as_customer": [months_as_customer],
        "billing_level": [billing_level_map[billing_level]],
        "call_count": [call_count],
        "sms_count": [sms_count],
        "plan_type": [0 if plan_type == 'Pay as you go' else 1],
        "account_status": [1 if account_status == "No Active" else 0],
        "age": [age],
        "customer_value": [customer_value]
    }

    df_user = pd.DataFrame(input_data)
    
    prob, pred = predict_churn(df_user)

    if st.button("📊 Show Client Data and Prediction"):
        st.subheader("📄 Client Information")
        st.dataframe(df_user)

        st.subheader("🔮 Churn Prediction")
        st.metric(label="Is this customer likely to churn?", value="Yes" if pred else "No")

        if pred:
            st.error("⚠️ This customer is at **high risk of churn**.")
        else:
            st.success("✅ This customer is at **low risk of churn**.")

