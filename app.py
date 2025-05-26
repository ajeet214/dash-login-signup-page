import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from utils import check_user, user_exists, add_user, reset_password

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div(id='page-content')

# Login Page Layout
login_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Login", className="text-center mb-4"),

                    dbc.Input(id='login-username', placeholder="Username", type="text", className="mb-3"),
                    dbc.Input(id='login-password', placeholder="Password", type="password", className="mb-2"),

                    html.Div([
                        html.A("Forgot Password?", href="/forgot-password", className="text-decoration-none")
                    ], className="mb-3 text-end"),

                    dbc.Button("Login", id='login-button', color="primary", className="w-100 mb-3"),

                    html.Div(id='login-output', className="text-danger text-center mb-2"),

                    html.Div([
                        html.Span("Don't have an account? "),
                        html.A("Sign Up", href="/signup", className="text-decoration-none")
                    ], className="text-center")
                ])
            ], className="shadow p-4")
        ], width=4)
    ], justify="center", align="center", className="vh-100")
], fluid=True)


# Signup Page Layout
signup_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Sign Up", className="text-center mb-4"),

                    dbc.Input(id='signup-username', placeholder="Username", type="text", className="mb-3"),
                    dbc.Input(id='signup-password', placeholder="Password", type="password", className="mb-3"),
                    dbc.Input(id='signup-email', placeholder="Email", type="email", className="mb-3"),
                    dbc.Input(id='signup-code', placeholder="Code", type="text", className="mb-3"),
                    dbc.Input(id='signup-branch', placeholder="Branch", type="text", className="mb-4"),

                    dbc.Button("Sign Up", id='signup-button', color="success", className="w-100 mb-3"),

                    html.Div(id='signup-output', className="text-danger text-center mb-2"),

                    html.Div([
                        html.Span("Already have an account? "),
                        html.A("Login", href="/", className="text-decoration-none")
                    ], className="text-center")
                ])
            ], className="shadow p-4")
        ], width=4)
    ], justify="center", align="center", className="vh-100")
], fluid=True)

# Forgot Password Layout
forgot_password_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Reset Password", className="text-center mb-4"),

                    dbc.Input(id='reset-username', placeholder="Username", type="text", className="mb-3"),
                    dbc.Input(id='reset-new-password', placeholder="New Password", type="password", className="mb-3"),
                    dbc.Input(id='reset-confirm-password', placeholder="Confirm New Password", type="password", className="mb-4"),

                    dbc.Button("Set New Password", id='reset-button', color="warning", className="w-100 mb-3"),

                    html.Div(id='reset-output', className="text-danger text-center mb-2"),

                    html.Div([
                        html.A("Back to Login", href="/", className="text-decoration-none")
                    ], className="text-center")
                ])
            ], className="shadow p-4")
        ], width=4)
    ], justify="center", align="center", className="vh-100")
], fluid=True)

# Profile Layout (To be defined later)
profile_layout = html.Div([
    html.H2("Welcome to your profile page!"),
    html.A("Logout", href="/")
])

# Routing Callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def display_page(pathname):
    if pathname == '/signup':
        return signup_layout
    elif pathname == '/forgot-password':
        return forgot_password_layout
    elif pathname == '/profile':
        return profile_layout
    return login_layout

# Login Callback
@app.callback(
    Output('login-output', 'children'),
    Input('login-button', 'n_clicks'),
    State('login-username', 'value'),
    State('login-password', 'value'),
    prevent_initial_call=True
)
def login_user(n, username, password):
    if check_user(username, password):
        return dcc.Location(pathname='/profile', id='login-redirect')
    return "User does not exist or incorrect credentials."

# Signup Callback
@app.callback(
    Output('signup-output', 'children'),
    Input('signup-button', 'n_clicks'),
    State('signup-username', 'value'),
    State('signup-password', 'value'),
    State('signup-email', 'value'),
    State('signup-code', 'value'),
    State('signup-branch', 'value'),
    prevent_initial_call=True
)
def signup_user(n, username, password, email, code, branch):
    if not username or not password:
        return "Username and Password required."
    if add_user(username, password, email, code, branch):
        return "User registered successfully!"
    return "Username already exists."

# Forgot Password Callback
@app.callback(
    Output('fp-output', 'children'),
    Input('fp-button', 'n_clicks'),
    State('fp-username', 'value'),
    State('fp-password', 'value'),
    State('fp-confirm-password', 'value'),
    prevent_initial_call=True
)
def reset_user_password(n, username, new_password, confirm_password):
    if new_password != confirm_password:
        return "Passwords do not match."
    if reset_password(username, new_password):
        return "Password updated successfully!"
    return "Username not found."


# URL Routing Component
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run(debug=True)
