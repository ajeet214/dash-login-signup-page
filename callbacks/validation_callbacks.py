from dash import Input, Output
import re


def register_validation_callbacks(app):
    @app.callback(
        Output('signup-username-error', 'children'),
        Output('signup-password-error', 'children'),
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
