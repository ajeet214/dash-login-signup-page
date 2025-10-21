from dash import Dash, html, dash_table, Input, Output, State

app = Dash(__name__)

app.layout = html.Div([
    html.Button("Copy table", id="copy_btn"),
    html.Div(id="message_copy", style={"color": "green"}),
    dash_table.DataTable(
        id="sales_table",
        columns=[{"name": c, "id": c} for c in ["Department", "Sales", "Weight"]],
        data=[
            {"Department": "Phones", "Sales": 1000, "Weight": "55.8%"},
            {"Department": "Computers", "Sales": 600, "Weight": "26.1%"},
        ],
        style_table={'overflowX': 'auto'},
    )
])

app.clientside_callback(
    """
    function(n_clicks, data) {
        if (!n_clicks) return;
        const cols = Object.keys(data[0]);
        const tsv = [cols.join('\\t')]
            .concat(data.map(r => cols.map(c => r[c]).join('\\t')))
            .join('\\n');
        navigator.clipboard.writeText(tsv);
        return "Copied to clipboard! Paste in Excel.";
    }
    """,
    Output("message_copy", "children"),
    Input("copy_btn", "n_clicks"),
    State("sales_table", "data")
)

if __name__ == "__main__":
    app.run(debug=True)
