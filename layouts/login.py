from dash import html
import dash_bootstrap_components as dbc

# Login Page Layout
login_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Img(src='/assets/logo.png', className="logo-img"),
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
