from dash import html
import dash_bootstrap_components as dbc

# Profile Layout (To be defined later)
profile_layout = html.Div([
    html.H2("Welcome to your profile page!"),
    html.A("Logout", href="/")
])
