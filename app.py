import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from layouts.login import login_layout
from layouts.signup import signup_layout
from layouts.forgot_password import forgot_password_layout
from layouts.profile import profile_layout
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# URL Routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/signup':
        return signup_layout
    elif pathname == '/forgot-password':
        return forgot_password_layout
    elif pathname == '/profile':
        return profile_layout
    return login_layout


# Register all callbacks
register_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)
