from dash import html
import dash_bootstrap_components as dbc

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