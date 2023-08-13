import streamlit as st
import plotly.express as px
import pandas as pd 



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
col =['company', 'sector', 'region', 'branch', 'doctype', 'pos_id',
       'invoiceno', 'invoicedate', 'cashierno', 'customerno', 'totalvalue',
       'payedvalue', 'discounts', 'app_version', 'invoice_day',
       'invoice_day_name', 'invoice_month', 'invoice_month_name',
       'invoice_year', 'sales', 'returns', 'has_discount']
df = pd.read_csv('sal_invoices2.csv')
#st.dataframe(df)

# ---- SIDEBAR ----
st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: #EE82EE	 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.header("Data Filtration:")

day = st.sidebar.multiselect(
    "Select the Day:",
    options=df["invoice_day_name"].unique(),
    default=df["invoice_day_name"].unique()
)

month = st.sidebar.multiselect(
    "Select the Month:",
    options=df["invoice_month_name"].unique(),
    default=df["invoice_month_name"].unique()
)

year = st.sidebar.multiselect(
    "Select the Year:",
    options=df["invoice_year"].unique(),
    default=df["invoice_year"].unique()
)


df_selection = df.query( "invoice_year == @year & invoice_month_name == @month & invoice_day_name == @day " )

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["totalvalue"].sum())

st.subheader("Total Sales:")
st.subheader(f"EGP {total_sales:,}")


st.markdown("""---""")


# SALES BY point of sale [BAR CHART]
sales_by_pos = (
    df_selection.groupby(by=["pos_id"]).mean()[["totalvalue"]].sort_values(by="totalvalue")
)


fig_sales_by_pos = px.bar(sales_by_pos, x="totalvalue" , y=sales_by_pos.index ,
             color_discrete_sequence=["#0083B8"] * len(sales_by_pos) ,
             orientation="h",
             title="<b>Overall Sales Revenue by POS</b>")

fig_sales_by_pos.update_layout(xaxis_tickangle=-90)
fig_sales_by_pos.update_xaxes(title='Sales Revenue')
fig_sales_by_pos.update_yaxes(title='Point Of Sale')
fig_sales_by_pos.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_sales_by_pos, use_container_width=True)


st.markdown("""---""")


# SALES and Return BY cashier number [BAR CHART]
sales_by_cashier = (
    df_selection.groupby(by=["cashierno"]).mean()[["sales"]] )

x_values = sales_by_cashier.index.tolist()
fig_sales_by_cash = px.bar( x=x_values, y=sales_by_cashier['sales'],
             title="<b>Overall Sales Revenue by Cashier</b>",
    color_discrete_sequence=['#FF00FF']* len(sales_by_cashier) , template="plotly_white" )


fig_sales_by_cash.update_layout(
    xaxis=dict(
        type="category",
        categoryarray=x_values,
        title="Cashier"
    ),
    yaxis=dict(title="Sales"),
)
fig_sales_by_cash.update_layout( plot_bgcolor="rgba(0,0,0,0)", yaxis=(dict(showgrid=False)) )



###
returns_by_cashier = (
    df_selection.groupby(by=["cashierno"]).mean()[["returns"]] )
x2_values = returns_by_cashier.index.tolist()
fig_returns_by_cash = px.bar( x=x2_values, y=returns_by_cashier['returns'],
             title="<b>Overall Returns by Cashier</b>",
    color_discrete_sequence=['#FF00FF']* len(returns_by_cashier) , template="plotly_white" )


fig_returns_by_cash.update_layout(
    xaxis=dict(
        type="category",
        categoryarray=x2_values,
        title="Cashier"
    ),
    yaxis=dict(title="Sales"),
)
fig_returns_by_cash.update_layout( plot_bgcolor="rgba(0,0,0,0)", yaxis=(dict(showgrid=False)) )


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_sales_by_cash, use_container_width=True)
right_column.plotly_chart(fig_returns_by_cash, use_container_width=True)

st.markdown("""---""")

#  Point Of Sale that offer more Discounts [PIE-CHART]
discount_df = (df_selection[df_selection['has_discount'] == 'yes'])
discount_counts = discount_df['pos_id'].value_counts()

fig_pos_discount = px.pie(names=discount_counts.index, values=discount_counts.values,title='<b>Certain Point Of Sales  have more discounts</b> ')
st.plotly_chart(fig_pos_discount, use_container_width=True)

st.markdown("""---""")

app_versions = (
    df_selection.groupby(by=["app_version"]).mean()[["totalvalue"]])


fig_sales_app_versions = px.bar(app_versions, x="totalvalue" , y=app_versions.index ,
             color_discrete_sequence=["#0083B8"] * len(app_versions) ,
             orientation="h",
             title="<b>The Sales Revenue For Each Application Version </b>")


fig_sales_app_versions.update_xaxes(title='Sales Revenue')
fig_sales_app_versions.update_yaxes(title='App Version')
fig_sales_app_versions.update_layout(
    plot_bgcolor="rgba(0,0,0,0)" 
    )
st.plotly_chart(fig_sales_app_versions, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
