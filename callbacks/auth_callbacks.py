from dash import Input, Output, State, dcc
from utils.user_utils import check_user, add_user, reset_password
import re


def register_auth_callbacks(app):
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

        if not re.fullmatch(r'^[A-Za-z0-9_]+$', username):
            return "Invalid username. Use only letters, numbers, and underscores."

        if len(password) < 10 or \
           not re.search(r'[A-Z]', password) or \
           not re.search(r'[a-z]', password) or \
           not re.search(r'\d', password) or \
           not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return "Password does not meet criteria."

        if add_user(username, password, email, code, branch):
            return "User signed up successfully!"
        else:
            return "Username already exists."

    @app.callback(
        Output('forgot-password-output', 'children'),
        Input('set-password-button', 'n_clicks'),
        State('forgot-username', 'value'),
        State('new-password', 'value'),
        State('confirm-password', 'value'),
        prevent_initial_call=True
    )
    def reset_user_password(n, username, new_password, confirm_password):
        if new_password != confirm_password:
            return "Passwords do not match."
        if reset_password(username, new_password):
            return "Password updated successfully!"
        return "Username not found."
