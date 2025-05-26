import dash
from dash import html, dcc, Input, Output, State
from utils import check_user, user_exists, add_user, reset_password

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(id='page-content')

# Login Page Layout
login_layout = html.Div([
    html.H2("Login"),
    dcc.Input(id='login-username', type='text', placeholder='Username'),
    dcc.Input(id='login-password', type='password', placeholder='Password'),
    html.Br(),
    html.A("Forgot Password?", href="/forgot-password"),
    html.Br(),
    html.Button("Login", id='login-button'),
    html.Div(id='login-output'),
    html.Br(),
    html.A("Sign Up", href="/signup")
])

# Signup Page Layout
signup_layout = html.Div([
    html.H2("Sign Up"),
    dcc.Input(id='signup-username', type='text', placeholder='Username'),
    dcc.Input(id='signup-password', type='password', placeholder='Password'),
    dcc.Input(id='signup-email', type='email', placeholder='Email'),
    dcc.Input(id='signup-code', type='text', placeholder='Code'),
    dcc.Input(id='signup-branch', type='text', placeholder='Branch'),
    html.Br(),
    html.Button("Sign Up", id='signup-button'),
    html.Div(id='signup-output'),
    html.Br(),
    html.A("Back to Login", href="/")
])

# Forgot Password Layout
forgot_layout = html.Div([
    html.H2("Reset Password"),
    dcc.Input(id='fp-username', type='text', placeholder='Username'),
    dcc.Input(id='fp-password', type='password', placeholder='New Password'),
    dcc.Input(id='fp-confirm-password', type='password', placeholder='Confirm New Password'),
    html.Br(),
    html.Button("Set New Password", id='fp-button'),
    html.Div(id='fp-output'),
    html.Br(),
    html.A("Back to Login", href="/")
])

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
        return forgot_layout
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
