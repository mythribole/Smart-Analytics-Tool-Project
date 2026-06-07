import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smart Analytics Tool", layout="wide")

st.title("Smart Analytics Tool")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.header("Dataset Preview")
    st.dataframe(df.head())

    st.header("Dataset Shape")
    st.write(df.shape)

    st.header("Column Names")
    st.write(df.columns.tolist())

    st.header("Missing Values")
    st.dataframe(df.isnull().sum())

    st.header("Statistical Summary")
    st.dataframe(df.describe())

    numeric_columns = df.select_dtypes(include="number").columns

    if len(numeric_columns) > 0:

        st.header("Visualization")

        selected_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Histogram", "Box Plot", "Bar Chart"]
        )

        if chart_type == "Histogram":

            fig = px.histogram(
                df,
                x=selected_column,
                title=f"Histogram of {selected_column}"
            )

        elif chart_type == "Box Plot":

            fig = px.box(
                df,
                y=selected_column,
                title=f"Box Plot of {selected_column}"
            )

        else:

            counts = (
                df[selected_column]
                .value_counts()
                .head(10)
                .reset_index()
            )

            counts.columns = [selected_column, "Count"]

            fig = px.bar(
                counts,
                x=selected_column,
                y="Count",
                title=f"Bar Chart of {selected_column}"
            )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No numeric columns found.")

else:
    st.info("Please upload a CSV file.")