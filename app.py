import re
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
            html.Img(src='/assets/logo.png', className="logo-img"),  # Add logo
            dbc.Card([
                dbc.CardBody([
                    html.H3("Login", className="text-center mb-4"),

                    dbc.Input(id='login-username', placeholder="Username", type="text", className="mb-2"),
                    dbc.Input(id='login-password', placeholder="Password", type="password", className="mb-2"),

                    html.Div(html.A("Forgot Password?", href="/forgot-password"), className="text-end mb-2"),

                    dbc.Button("Login", id='login-button', color="primary", className="w-100 mb-3"),
                    html.Div(id='login-output', className="text-danger text-center mb-2"),

                    html.Div([
                        html.Span("Don't have an account? "),
                        html.A("Sign Up", href="/signup", className="text-decoration-none")
                    ], className="text-center")
                ])
            ], className="shadow p-4 card-center")
        ], width=4)
    ], justify="center", align="center", className="vh-100")
], fluid=True)


# Signup Page Layout
signup_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src='/assets/logo.png', className="logo-img"),  # Logo
            dbc.Card([
                dbc.CardBody([
                    html.H3("Sign Up", className="text-center mb-4"),

                    dbc.Input(id='signup-username', placeholder="Username", type="text", className="mb-2"),
                    html.Div(id='signup-username-error', className="text-danger mb-2", style={"fontSize": "0.9rem"}),

                    dbc.Input(id='signup-password', placeholder="Password", type="password", className="mb-2"),
                    html.Div(id='signup-password-error', className="text-danger mb-2", style={"fontSize": "0.9rem"}),

                    dbc.Input(id='signup-email', placeholder="Email", type="email", className="mb-2"),
                    dbc.Input(id='signup-code', placeholder="Code", type="text", className="mb-2"),
                    dbc.Input(id='signup-branch', placeholder="Branch", type="text", className="mb-3"),

                    dbc.Button("Sign Up", id='signup-button', color="success", className="w-100 mb-3", disabled=True),
                    html.Div(id='signup-output', className="text-danger text-center mb-2"),

                    html.Div([
                        html.Span("Already have an account? "),
                        html.A("Login", href="/", className="text-decoration-none")
                    ], className="text-center")
                ])
            ], className="shadow p-4 card-center")
        ], width=4)
    ], justify="center", align="center", className="vh-100")
], fluid=True)

# Forgot Password Layout
forgot_password_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src='/assets/logo.png', className="logo-img"),  # Logo
            dbc.Card([
                dbc.CardBody([
                    html.H3("Reset Password", className="text-center mb-4"),

                    dbc.Input(id='forgot-username', placeholder="Username", type="text", className="mb-2"),

                    dbc.Input(id='new-password', placeholder="New Password", type="password", className="mb-2"),
                    html.Div(id='new-password-error', className="text-danger mb-2", style={"fontSize": "0.9rem"}),

                    dbc.Input(id='confirm-password', placeholder="Confirm Password", type="password", className="mb-2"),
                    html.Div(id='confirm-password-error', className="text-danger mb-2", style={"fontSize": "0.9rem"}),

                    dbc.Button("Set New Password", id='set-password-button', color="primary", className="w-100 mb-3", disabled=True),

                    html.Div(id='forgot-password-output', className="text-danger text-center mb-2"),

                    html.Div([
                        html.Span("Back to "),
                        html.A("Login", href="/", className="text-decoration-none")
                    ], className="text-center")
                ])
            ], className="shadow p-4 card-center")
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
def signup_user(n_clicks, username, password, email, code, branch):
    if not all([username, password, email, code, branch]):
        return "All fields are required."

    # Username validation
    if not re.fullmatch(r'^[A-Za-z0-9_]+$', username):
        return "Invalid username. Use only letters, numbers, and underscores."

    # Password validation
    if len(password) < 10:
        return "Password must be at least 10 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password must include at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password must include at least one lowercase letter."
    if not re.search(r'\d', password):
        return "Password must include at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must include at least one special character."

    if add_user(username, password, email, code, branch):
        return "User signed up successfully!"
    else:
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


@app.callback(
    Output('username-error', 'children'),
    Output('password-error', 'children'),
    Output('signup-button', 'disabled'),
    Input('signup-username', 'value'),
    Input('signup-password', 'value'),
    Input('signup-email', 'value'),
    Input('signup-code', 'value'),
    Input('signup-branch', 'value'),
)
def validate_signup_inputs(username, password, email, code, branch):
    username_error = ""
    password_error = ""
    disable_button = True

    if not all([username, password, email, code, branch]):
        return username_error, password_error, True

    # Validate username
    if not re.fullmatch(r'^[A-Za-z0-9_]+$', username):
        username_error = "Only letters, numbers, and underscores allowed."

    # Validate password
    if len(password) < 10:
        password_error = "Password must be at least 10 characters long."
    elif not re.search(r'[A-Z]', password):
        password_error = "Include at least one uppercase letter."
    elif not re.search(r'[a-z]', password):
        password_error = "Include at least one lowercase letter."
    elif not re.search(r'\d', password):
        password_error = "Include at least one number."
    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        password_error = "Include at least one special character."

    # If there are no error messages
    if not username_error and not password_error:
        disable_button = False

    return username_error, password_error, disable_button


@app.callback(
    Output('new-password-error', 'children'),
    Output('confirm-password-error', 'children'),
    Output('set-password-button', 'disabled'),
    Input('new-password', 'value'),
    Input('confirm-password', 'value')
)
def validate_forgot_password_fields(new_pwd, confirm_pwd):
    new_pwd_error = ""
    confirm_pwd_error = ""
    disable_button = True

    if not new_pwd or not confirm_pwd:
        return new_pwd_error, confirm_pwd_error, True

    # Password validation logic
    if len(new_pwd) < 10:
        new_pwd_error = "Must be at least 10 characters long."
    elif not re.search(r'[A-Z]', new_pwd):
        new_pwd_error = "Include at least one uppercase letter."
    elif not re.search(r'[a-z]', new_pwd):
        new_pwd_error = "Include at least one lowercase letter."
    elif not re.search(r'\d', new_pwd):
        new_pwd_error = "Include at least one number."
    elif not re.search(r'[!@#$%^&*(),.?\":{}|<>]', new_pwd):
        new_pwd_error = "Include at least one special character."

    # Confirm password validation
    if new_pwd != confirm_pwd:
        confirm_pwd_error = "Passwords do not match."

    if not new_pwd_error and not confirm_pwd_error:
        disable_button = False

    return new_pwd_error, confirm_pwd_error, disable_button


# URL Routing Component
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

if __name__ == '__main__':
    app.run(debug=True)
