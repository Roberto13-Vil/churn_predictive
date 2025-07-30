import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Churn", layout="wide")

# Simulador de navegación por etapas usando session_state
if "stage_index" not in st.session_state:
    st.session_state.stage_index = 0

stages = ["📊 Overview", "❗Dissatisfaction", "📞 Frequency", "🌟 Importance"]

# Botones de navegación
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button("⬅️ Anterior") and st.session_state.stage_index > 0:
        st.session_state.stage_index -= 1
with col_nav3:
    if st.button("Siguiente ➡️") and st.session_state.stage_index < len(stages) - 1:
        st.session_state.stage_index += 1

stage = stages[st.session_state.stage_index]

st.markdown(f"<h2 style='text-align: center;'>{stage}</h2>", unsafe_allow_html=True)
st.divider()

df = pd.read_csv('Data/viz_ready.csv')

# Contenido de cada etapa
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
        st.metric("% Churn", f"{churned / total * 100:.2f}%")

elif stage == "❗Dissatisfaction":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg = df.groupby('has_churned')['failed_call_count'].mean()
        st.metric("Avg Failed Calls (Churn)", f"{avg.get('Churn', 0):.1f}")
    with col2:
        high_failed = df[df['failed_call_count'] > 5]
        perc = (high_failed['has_churned'] == 'Churn').mean() * 100
        st.metric("% Churn w/ >5 Failed Calls", f"{perc:.1f}%")
    with col3:
        complaints = df[df['submitted_complaint'] == 'Yes']
        st.metric("Total Complaints", len(complaints))
    with col4:
        churned_complaints = complaints[complaints['has_churned'] == 'Churn']
        percent = len(churned_complaints) / len(complaints) * 100 if len(complaints) > 0 else 0
        st.metric("% Complaints Churned", f"{percent:.1f}%")
    colA, colB = st.columns(2)
    with colA:
        fig = px.histogram(df, x='failed_call_count', color='has_churned', barmode='overlay',
                           title="Failed Calls Distribution",
                           color_discrete_map={"Churn": "red", "No Churn": "blue"}, opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)
    with colB:
        fig = px.histogram(df, x='submitted_complaint', color='has_churned', barmode='group',
                           title="Complaint Submissions",
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
        st.metric("% Churn w/ <5 SMS", f"{churn_low:.1f}%")
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
                           title="Months as Customer",
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
