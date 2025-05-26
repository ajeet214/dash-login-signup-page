from dash import html
import dash_bootstrap_components as dbc

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