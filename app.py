import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Load dataset
zara_df = pd.read_csv("C:/Users/jthun/Downloads/Zara Dashboard Data.csv")

# Preprocessing
zara_df['Revenue'] = zara_df['price'] * zara_df['Sales Volume']

# KPIs
total_items = len(zara_df)
avg_price = zara_df['price'].mean()
total_revenue = zara_df['Revenue'].sum()
total_units_sold = zara_df['Sales Volume'].sum()

# --- Promotion Visuals ---
promo_group = zara_df.groupby("Promotion_Flag").agg({
    "Sales Volume": ["mean", "sum"],
    "Revenue": ["mean", "sum"],
    "price": "count"
}).reset_index()
promo_group.columns = ["Promotion", "Avg Sales", "Total Sales", "Avg Revenue", "Total Revenue", "Total Items"]
promo_group["Promotion"] = promo_group["Promotion"].map({0: "No Promo", 1: "Promo"})

fig_promo_sales = px.bar(promo_group, x="Promotion", y="Avg Sales", title="Average Sales Volume by Promotion Status")
fig_promo_revenue = px.bar(promo_group, x="Promotion", y="Avg Revenue", title="Average Revenue by Promotion Status")
fig_promo_total = px.bar(promo_group, x="Promotion", y="Total Revenue", title="Total Revenue by Promotion Status")
fig_promo_items = px.bar(promo_group, x="Promotion", y="Total Items", title="Total Items by Promotion Status")

fig_terms_promo_sales = px.bar(
    zara_df.groupby(["terms", "Promotion_Flag"])["Sales Volume"].mean().reset_index().replace({"Promotion_Flag": {0: "No Promo", 1: "Promo"}}),
    x="terms", y="Sales Volume", color="Promotion_Flag", barmode="group",
    title="Average Sales Volume by Product Type and Promotion",
    labels={"Promotion_Flag": "Promotion"}
)
fig_terms_promo_sales.update_layout(xaxis_title="Product Type", yaxis_title="Avg Sales Volume", xaxis_tickangle=-45)

fig_terms_promo_revenue = px.bar(
    zara_df.groupby(["terms", "Promotion_Flag"])["Revenue"].mean().reset_index().replace({"Promotion_Flag": {0: "No Promo", 1: "Promo"}}),
    x="terms", y="Revenue", color="Promotion_Flag", barmode="group",
    title="Average Revenue by Product Type and Promotion",
    labels={"Promotion_Flag": "Promotion"}
)
fig_terms_promo_revenue.update_layout(xaxis_title="Product Type", yaxis_title="Avg Revenue", xaxis_tickangle=-45)

fig_terms_promo_total_revenue = px.bar(
    zara_df.groupby(["terms", "Promotion_Flag"])["Revenue"].sum().reset_index().replace({"Promotion_Flag": {0: "No Promo", 1: "Promo"}}),
    x="terms", y="Revenue", color="Promotion_Flag", barmode="group",
    title="Total Revenue by Product Type and Promotion",
    labels={"Promotion_Flag": "Promotion"}
)
fig_terms_promo_total_revenue.update_layout(xaxis_title="Product Type", yaxis_title="Total Revenue", xaxis_tickangle=-45)


# --- Seasonal Visuals ---
seasonal_group = zara_df.groupby("Seasonal_Flag").agg({
    "Sales Volume": ["mean", "sum"],
    "Revenue": ["mean", "sum"],
    "price": "count"
}).reset_index()
seasonal_group.columns = ["Seasonal", "Avg Sales", "Total Sales", "Avg Revenue", "Total Revenue", "Total Items"]
seasonal_group["Seasonal"] = seasonal_group["Seasonal"].map({0: "Non-Seasonal", 1: "Seasonal"})

fig_seasonal_sales = px.bar(seasonal_group, x="Seasonal", y="Avg Sales", title="Average Sales Volume by Season Status")
fig_seasonal_revenue = px.bar(seasonal_group, x="Seasonal", y="Avg Revenue", title="Average Revenue by Season Status")
fig_seasonal_total = px.bar(seasonal_group, x="Seasonal", y="Total Revenue", title="Total Revenue by Season Status")
fig_seasonal_items = px.bar(seasonal_group, x="Seasonal", y="Total Items", title="Total Items by Season Status")

# Additional Seasonal Visuals by Category
seasonal_category_sales = zara_df.groupby(["terms", "Seasonal_Flag"])["Sales Volume"].mean().reset_index()
seasonal_category_sales["Seasonal_Flag"] = seasonal_category_sales["Seasonal_Flag"].map({0: "Non-Seasonal", 1: "Seasonal"})

fig_terms_seasonal_sales = px.bar(
    seasonal_category_sales, x="terms", y="Sales Volume", color="Seasonal_Flag",
    barmode="group", title="Average Sales Volume by Product Type and Seasonal Status",
    labels={"terms": "Product Type", "Sales Volume": "Avg Sales Volume", "Seasonal_Flag": "Seasonal Status"},
    template="plotly_white"
)
fig_terms_seasonal_sales.update_layout(
    title_font=dict(size=16, family="Arial", color="black"),
    legend_title_text="Seasonal Status",
    xaxis_tickangle=-45
)

seasonal_category_revenue = zara_df.groupby(["terms", "Seasonal_Flag"])["Revenue"].mean().reset_index()
seasonal_category_revenue["Seasonal_Flag"] = seasonal_category_revenue["Seasonal_Flag"].map({0: "Non-Seasonal", 1: "Seasonal"})

fig_terms_seasonal_revenue = px.bar(
    seasonal_category_revenue, x="terms", y="Revenue", color="Seasonal_Flag",
    barmode="group", title="Average Revenue by Product Type and Seasonal Status",
    labels={"terms": "Product Type", "Revenue": "Avg Revenue", "Seasonal_Flag": "Seasonal Status"},
    template="plotly_white"
)
fig_terms_seasonal_revenue.update_layout(
    title_font=dict(size=16, family="Arial", color="black"),
    legend_title_text="Seasonal Status",
    xaxis_tickangle=-45
)


seasonal_total_revenue = zara_df.groupby(["terms", "Seasonal_Flag"])["Revenue"].sum().reset_index()
seasonal_total_revenue["Seasonal_Flag"] = seasonal_total_revenue["Seasonal_Flag"].map({0: "Non-Seasonal", 1: "Seasonal"})

fig_terms_seasonal_total_revenue = px.bar(
    seasonal_total_revenue, x="terms", y="Revenue", color="Seasonal_Flag",
    barmode="group", title="Total Revenue by Product Type and Seasonal Status",
    labels={"terms": "Product Type", "Revenue": "Total Revenue", "Seasonal_Flag": "Seasonal Status"},
    template="plotly_white"
)
fig_terms_seasonal_total_revenue.update_layout(
    title_font=dict(size=16, family="Arial", color="black"),
    legend_title_text="Seasonal Status",
    xaxis_tickangle=-45
)


# --- Product Position Visuals ---
pos_avg_sales = zara_df.groupby("Product Position")["Sales Volume"].mean().reset_index()
fig_pos_avg_sales = px.bar(pos_avg_sales, x="Product Position", y="Sales Volume", title="Average Sales Volume by Product Position")

pos_total_items = zara_df.groupby("Product Position").size().reset_index(name="Total Items")
fig_pos_total_items = px.bar(pos_total_items, x="Product Position", y="Total Items", title="Total Items by Product Position")

pos_avg_revenue = zara_df.groupby("Product Position")["Revenue"].mean().reset_index()
fig_pos_avg_revenue = px.bar(pos_avg_revenue, x="Product Position", y="Revenue", title="Average Revenue by Product Position")

pos_total_revenue = zara_df.groupby("Product Position")["Revenue"].sum().reset_index()
fig_pos_total_revenue = px.bar(pos_total_revenue, x="Product Position", y="Revenue", title="Total Revenue by Product Position")

# --- Category Breakdown ---
category_items = zara_df.groupby("terms").size().reset_index(name="Total Items")
fig_category_items = px.bar(category_items, x="terms", y="Total Items", title="Total Items by Category")

category_avg_revenue = zara_df.groupby("terms")["Revenue"].mean().reset_index()
fig_category_avg_revenue = px.bar(category_avg_revenue, x="terms", y="Revenue", title="Average Revenue by Category")

# --- Price Segmentation ---
zara_df['price'] = pd.to_numeric(zara_df['price'], errors='coerce')
zara_df['Sales Volume'] = pd.to_numeric(zara_df['Sales Volume'], errors='coerce')
lower_bound = 7.99
bin1_upper = 150.00
bin2_upper = 300.00
max_bin = round(zara_df['price'].max())
bins = [lower_bound, bin1_upper, bin2_upper, max_bin]
labels = [f"${lower_bound:.2f} - ${bin1_upper:.2f}", f"${bin1_upper:.2f} - ${bin2_upper:.2f}", f"${bin2_upper:.2f} - ${max_bin:.0f}"]
zara_df['Price_Bin'] = pd.cut(zara_df['price'], bins=bins, right=True, include_lowest=True, labels=labels)

price_avg_sales = zara_df.groupby('Price_Bin', observed=True)["Sales Volume"].mean().reset_index()
fig_price_avg_sales = px.bar(price_avg_sales, x="Price_Bin", y="Sales Volume", title="Average Sales Volume by Price Range")

price_total_revenue = zara_df.groupby('Price_Bin', observed=True)["Revenue"].sum().reset_index()
fig_price_total_revenue = px.bar(price_total_revenue, x="Price_Bin", y="Revenue", title="Total Revenue by Price Range")

price_total_items = zara_df.groupby('Price_Bin', observed=True).size().reset_index(name='Total Items')
fig_price_total_items = px.bar(price_total_items, x="Price_Bin", y="Total Items", title="Total Items by Price Range")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H1("Zara Product Analytics Dashboard", style={"textAlign": "center", "fontWeight": "bold", "marginBottom": "20px"}),

        html.P(
            "This dashboard analyzes Zara product sales across different categories, promotions, seasonal trends, and pricing. "
            "It provides KPIs, performance visuals, and actionable insights to guide merchandising and marketing strategies.",
            style={"textAlign": "center", "fontSize": "16px", "marginBottom": "30px"}
        ),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Total Items", className="bg-dark text-white"),
                dbc.CardBody(html.H4(f"{total_items:,}", className="card-text text-center"))
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Average Price", className="bg-dark text-white"),
                dbc.CardBody(html.H4(f"${avg_price:.2f}", className="card-text text-center"))
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Total Revenue", className="bg-dark text-white"),
                dbc.CardBody(html.H4(f"${total_revenue:,.0f}", className="card-text text-center"))
            ]), width=3),
            dbc.Col(dbc.Card([
                dbc.CardHeader("Total Units Sold", className="bg-dark text-white"),
                dbc.CardBody(html.H4(f"{int(total_units_sold):,}", className="card-text text-center"))
            ]), width=3)
        ], className="mb-5"),
    ], className="container"),

    html.Div([
        html.H3("Promotion Insights", className="mt-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_promo_sales), width=6),
            dbc.Col(dcc.Graph(figure=fig_promo_revenue), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_promo_total), width=6),
            dbc.Col(dcc.Graph(figure=fig_promo_items), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_terms_promo_sales), width=8),
            dbc.Col(dcc.Graph(figure=fig_terms_promo_revenue), width=8),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_terms_promo_total_revenue), width=8),
        ]),

        html.H3("Seasonal Insights", className="mt-5"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_seasonal_sales), width=6),
            dbc.Col(dcc.Graph(figure=fig_seasonal_revenue), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_seasonal_total), width=6),
            dbc.Col(dcc.Graph(figure=fig_seasonal_items), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_terms_seasonal_sales), width=8),
            dbc.Col(dcc.Graph(figure=fig_terms_seasonal_revenue), width=8),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_terms_seasonal_total_revenue), width=8),
        ]),

        html.H3("Product Position Insights", className="mt-5"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_pos_avg_sales), width=6),
            dbc.Col(dcc.Graph(figure=fig_pos_total_items), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_pos_avg_revenue), width=6),
            dbc.Col(dcc.Graph(figure=fig_pos_total_revenue), width=6),
        ]),

        html.H3("Category Breakdown", className="mt-5"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_category_items), width=6),
            dbc.Col(dcc.Graph(figure=fig_category_avg_revenue), width=6),
        ]),

        html.H3("Price Range Analysis", className="mt-5"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_price_avg_sales), width=6),
            dbc.Col(dcc.Graph(figure=fig_price_total_revenue), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_price_total_items), width=6),
        ]),
    ], style={"padding": "0px 30px"})
])
if __name__=='__main__':
    app.run(debug=True)