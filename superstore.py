import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('superstore_dataset2011-2015.csv', encoding="ISO-8859-1")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Research Questions", "Hypothesis", "Analysis", "Conclusions", "Recommendations"])

# Main page
if page == "Overview":
    st.title("Overview")
    st.markdown("""
         This dashboard analyzes sales and profit data to identify insights for improving business performance. Our goals include:
        - Identifying the most profitable product categories and regions.
        - Optimizing product offerings and strategies.
        - Understanding seasonal trends to enhance sales planning.
        - Evaluating the impact of different shipping methods on returns.
        - Analyzing weekday vs. weekend performance to tailor marketing efforts.
        - Comparing sales and profit contributions by customer segments.
        - Assessing performance across product sub-categories to identify areas for improvement.
        - Investigating specific sub-categories, like Tables, to uncover reasons for losses.
    """)

elif page == "Research Questions":
    st.title("Research Questions")
    st.markdown("""
        Our research focuses on the following questions:
        - Which product categories have the highest profit margins?
        - How do sales vary by region and month?
        - What is the return rate for same-day shipping?
        - How do sales and profit vary by day of the week?
        - Which segment generates more sales and profit?
        - Do all product sub-categories generate positive results?
        - What causes losses in specific sub-categories like Tables?
    """)

elif page == "Hypothesis":
    st.title("Hypothesis")
    st.markdown("""
        We formulated the following hypothesis:
        1. Technology products have the highest profit margin.
        2. The East region has the highest sales.
        3. Sales peak in certain months.
        4. Same-day shipping has the lowest return rate.
        5. Weekday profits are higher than weekends.
        6. Consumer segment generates more sales but corporate segment yields higher profits.
        7. All product sub-categories generate positive results.
    """)

elif page == "Analysis":
    st.title("Analysis")

    hypothesis = st.selectbox("Select a hypothesis to test:", [
        "Technology products have the highest profit margin.",
        "The East region has the highest sales.",
        "Sales peak in certain months.",
        "Same-day shipping has the lowest return rate.",
        "Weekday profits are higher than weekends.",
        "Consumer segment generates more sales but corporate segment yields higher profits.",
        "All product sub-categories generate positive results.",
        "Finding the Reason for Losses in the Tables Sub Category"
    ])

    if hypothesis == "Technology products have the highest profit margin.":
        cat_profit = data.groupby('Category')['Profit'].sum()
        fig, ax = plt.subplots()
        sns.barplot(x=cat_profit.index, y=cat_profit.values, palette="coolwarm", ax=ax)
        ax.set_title('Total Profit by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Total Profit')
        st.pyplot(fig)
        st.markdown("**Conclusion:** Supported. Technology products have the highest profit margin.")

    elif hypothesis == "The East region has the highest sales.":
        reg_sales = data.groupby('Region')['Sales'].sum()
        fig, ax = plt.subplots()
        sns.barplot(x=reg_sales.index, y=reg_sales.values, palette="coolwarm", ax=ax)
        ax.set_title('Total Sales by Region')
        ax.set_xlabel('Region')
        ax.set_ylabel('Total Sales')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        st.markdown("**Conclusion:** Not supported. The Central region has the highest sales.")

    elif hypothesis == "Sales peak in certain months.":
        data['Order Month'] = pd.DatetimeIndex(data['Order Date']).month
        month_sales = data.groupby('Order Month')['Sales'].sum()
        fig, ax = plt.subplots()
        sns.lineplot(x=month_sales.index, y=month_sales.values, ax=ax)
        ax.set_title('Total Sales by Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Sales')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        st.markdown("**Conclusion:** Supported. Sales peak in November and December.")

    elif hypothesis == "Same-day shipping has the lowest return rate.":
        total_orders_by_shipping_mode = data.groupby('Ship Mode').size()
        returned_orders_by_shipping_mode = data[data['Profit'] < 0].groupby('Ship Mode').size()
        return_percentage_by_shipping_mode = (returned_orders_by_shipping_mode / total_orders_by_shipping_mode) * 100
        fig, ax = plt.subplots()
        sns.barplot(x=return_percentage_by_shipping_mode.index, y=return_percentage_by_shipping_mode.values, palette="coolwarm", ax=ax)
        ax.set_title('Return Percentage by Shipping Mode')
        ax.set_xlabel('Shipping Mode')
        ax.set_ylabel('Return Percentage')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        st.markdown("**Conclusion:** Supported. Same-day shipping has the lowest return rate.")
        
        
    elif hypothesis == "Weekday profits are higher than weekends.":
        data['Order Day'] = pd.DatetimeIndex(data['Order Date']).day_name()
        day_profit = data.groupby('Order Day')['Profit'].sum()
        fig, ax = plt.subplots()
        sns.barplot(x=day_profit.index, y=day_profit.values, palette="coolwarm", ax=ax)
        ax.set_title('Total Profit by Day of the Week')
        ax.set_xlabel('Day of the Week')
        ax.set_ylabel('Total Profit')
        st.pyplot(fig)
        st.markdown("**Conclusion:** Supported. Weekday profits are higher than weekends.")

    elif hypothesis == "Consumer segment generates more sales but corporate segment yields higher profits.":
        segment_sales = data.groupby('Segment')['Sales'].sum()
        fig, ax = plt.subplots()
        segment_sales.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title("Total Sales by Segment")
        ax.set_xlabel("Segment")
        ax.set_ylabel("Total Sales")
        st.pyplot(fig)

        segment_profit = data.groupby('Segment')['Profit'].sum()
        fig, ax = plt.subplots()
        segment_profit.plot(kind='bar', color='lightgreen', ax=ax)
        ax.set_title("Total Profit by Segment")
        ax.set_xlabel("Segment")
        ax.set_ylabel("Total Profit")
        st.pyplot(fig)
        st.markdown("**Conclusion:** Not Supported. Consumer segment generates more sales, and more profits as well")

    elif hypothesis == "All product sub-categories generate positive results.":
        sub_cat_sales = data.groupby('Sub-Category')['Sales'].sum()
        fig, ax = plt.subplots()
        sub_cat_sales.plot(kind='bar', figsize=(12, 6), color='coral', ax=ax)
        ax.set_title("Total Sales by Sub-Category")
        ax.set_xlabel("Sub-Category")
        ax.set_ylabel("Total Sales")
        ax.set_xticklabels(sub_cat_sales.index, rotation=90)
        st.pyplot(fig)

        sub_cat_profit = data.groupby('Sub-Category')['Profit'].sum()
        fig, ax = plt.subplots()
        sub_cat_profit.plot(kind='bar', figsize=(12, 6), color='teal', ax=ax)
        ax.set_title("Total Profit by Sub-Category")
        ax.set_xlabel("Sub-Category")
        ax.set_ylabel("Total Profit")
        ax.set_xticklabels(sub_cat_profit.index, rotation=90)
        st.pyplot(fig)
        st.markdown("**Conclusion:** Partially Supported. All product sub-categories except tables generate positive results.")

    elif hypothesis == "Finding the Reason for Losses in the Tables Sub Category":
        tables_data = data[data['Sub-Category'] == 'Tables']
        
        fig, ax = plt.subplots()
        tables_data['Profit'].plot(kind='hist', bins=30, color='red', ax=ax)
        ax.set_title("Profit Distribution for Tables")
        ax.set_xlabel("Profit")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        sns.scatterplot(x='Discount', y='Profit', data=tables_data, palette='coolwarm', ax=ax)
        ax.set_title("Discount vs Profit for Tables")
        ax.set_xlabel("Discount (in %)")
        ax.set_ylabel("Profit")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        sns.scatterplot(x='Shipping Cost', y='Profit', data=tables_data, palette='coolwarm', ax=ax)
        ax.set_title("Shipping Cost vs Profit for Tables")
        ax.set_xlabel("Shipping Cost")
        ax.set_ylabel("Profit")
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='Discount', y='Profit', size='Shipping Cost', data=tables_data, palette='coolwarm', sizes=(20, 200), ax=ax)
        ax.set_title("Discount and Shipping Cost vs Profit for Tables")
        ax.set_xlabel("Discount (in %)")
        ax.set_ylabel("Profit")
        st.pyplot(fig)
        st.markdown("**Conclusion:** Losses in the Tables sub-category are influenced by high discounts and shipping costs.")

elif page == "Conclusions":
    st.title("Conclusions")
    st.markdown("""
        Based on our analysis, we draw the following conclusions:
        - Technology products are the most profitable category.
        - The Central region leads in total sales.
        - Sales peak during November and December.
        - Same-day shipping has the lowest return rate.
        - Weekday profits surpass weekend profits.
        - Consumer segment generates higher sales, but Corporate segment yields more profit.
        - All product sub-categories generate positive results.
        - Losses in the Tables sub-category are due to high discounts and shipping costs.
    """)

elif page == "Recommendations":
    st.title("Recommendations")
    st.markdown("""
        To improve business performance, we recommend:
        - Focus on promoting technology products to maximize profits.
        - Allocate more resources to the Central region to sustain high sales.
        - Prepare for peak sales in November and December with adequate inventory and staffing.
        - Encourage same-day shipping to minimize returns.
        - Strategize to boost weekend sales and profits.
        - Leverage the profitability of the Corporate segment by offering tailored solutions.
        - Monitor sub-categories like Tables for high discounts and shipping costs, and adjust strategies accordingly.
    """)
