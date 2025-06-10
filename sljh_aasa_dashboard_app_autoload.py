
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SLJH AASA Dashboard", layout="wide")

# Header
st.markdown("## Show Low Junior High AASA Performance Dashboard")
st.markdown("**Are we reaching our vision?**")
st.markdown("*At SLJH, 100% of students will be proficient or higher in relation to state standards by the end of 8th grade.*")
st.markdown("---")

# Load default data from repo
df = pd.read_csv("ShowLow_JH_AASA_2022_2025_Clean.csv")

# Melt into long format
df_melted = df.melt(
    id_vars=["Grade", "Subject", "Year"],
    value_vars=["Level 1", "Level 2", "Level 3", "Level 4"],
    var_name="Performance Level",
    value_name="Percentage"
)

label_map = {
    "Level 1": "Minimally Proficient",
    "Level 2": "Partially Proficient",
    "Level 3": "Proficient",
    "Level 4": "Highly Proficient"
}
color_map = {
    "Minimally Proficient": "red",
    "Partially Proficient": "orange",
    "Proficient": "green",
    "Highly Proficient": "blue"
}
df_melted["Performance Label"] = df_melted["Performance Level"].map(label_map)

# Sidebar filters
st.sidebar.header("Filter the Data")
selected_years = st.sidebar.multiselect("Select Year(s)", sorted(df_melted["Year"].unique()), default=sorted(df_melted["Year"].unique()))
selected_grades = st.sidebar.multiselect("Select Grade(s)", sorted(df_melted["Grade"].unique()), default=sorted(df_melted["Grade"].unique()))
selected_subjects = st.sidebar.multiselect("Select Subject(s)", sorted(df_melted["Subject"].unique()), default=sorted(df_melted["Subject"].unique()))

# Apply filters
filtered_df = df_melted[
    (df_melted["Year"].isin(selected_years)) &
    (df_melted["Grade"].isin(selected_grades)) &
    (df_melted["Subject"].isin(selected_subjects))
]

# Stacked bar chart
st.subheader("Performance Level Distribution (Stacked Bar)")
bar_fig = px.bar(
    filtered_df,
    x="Year",
    y="Percentage",
    color="Performance Label",
    barmode="stack",
    facet_col="Subject",
    facet_row="Grade",
    color_discrete_map=color_map,
    labels={"Percentage": "Percent of Students"},
    height=600
)
st.plotly_chart(bar_fig, use_container_width=True)

# Line chart
st.subheader("Performance Trend Over Time (Line Chart)")
line_fig = px.line(
    filtered_df,
    x="Year",
    y="Percentage",
    color="Performance Label",
    facet_col="Subject",
    facet_row="Grade",
    markers=True,
    color_discrete_map=color_map,
    height=600
)
st.plotly_chart(line_fig, use_container_width=True)
