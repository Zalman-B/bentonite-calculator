from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from datetime import datetime

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

languages = {
    "ka": {
        "title": "🧪 ბენტონიტის დოზირების გაფართოებული კალკულატორი",
        "filtration": "ფილტრაციის კოეფიციენტი",
        "ph": "ღვინის pH",
        "alcohol": "ალკოჰოლის შემცველობა (%)",
        "volume": "ღვინის მოცულობა (ლიტრი)",
        "bentonite_type": "ბენტონიტის ტიპი",
        "bentonite_options": ["სოდიუმი (Sodium)", "კალციუმი (Calcium)"],
        "contact_time": "კონტაქტის დრო (სთ)",
        "processing_temp": "დამუშავების ტემპერატურა (°C)",
        "injection_method": "შეტანის მეთოდი",
        "injection_options": ["სუსპენზია წყალში", "მშრალი ფხვნილი"],
        "calculate": "გამოთვლა",
        "result_label": "რეკომენდებული დოზა",
        "language": "ენა",
    }
}

lang = "ka"

app.layout = dbc.Container([
    html.H1(languages[lang]["title"], className="text-center my-4"),

    dbc.Row([
        dbc.Col([
            dbc.Label(languages[lang]["filtration"]),
            dbc.Input(id="filtration", type="number")
        ]),
        dbc.Col([
            dbc.Label(languages[lang]["ph"]),
            dbc.Input(id="ph", type="number")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label(languages[lang]["alcohol"]),
            dcc.Dropdown(
                id="alcohol",
                options=[{"label": f"{i}%", "value": float(i)} for i in range(11, 16)],
                placeholder="აირჩიეთ"
            )
        ]),
        dbc.Col([
            dbc.Label(languages[lang]["volume"]),
            dbc.Input(id="volume", type="number")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label(languages[lang]["bentonite_type"]),
            dcc.Dropdown(
                id="bentonite",
                options=[
                    {"label": label, "value": value}
                    for label, value in zip(languages[lang]["bentonite_options"], ["sodium", "calcium"])
                ],
                placeholder="აირჩიეთ"
            )
        ]),
        dbc.Col([
            dbc.Label(languages[lang]["processing_temp"]),
            dbc.Input(id="process_temp", type="number")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label(languages[lang]["contact_time"]),
            dbc.Input(id="contact_time", type="number")
        ]),
        dbc.Col([
            dbc.Label(languages[lang]["injection_method"]),
            dcc.RadioItems(id="injection_method", options=[
                {"label": label, "value": value}
                for label, value in zip(languages[lang]["injection_options"], ["wet", "dry"])
            ])
        ])
    ]),

    dbc.Button(languages[lang]["calculate"], id="calc-btn", color="primary", className="mt-3"),
    html.Hr(),
    html.Div(id="result", className="h4 text-success mt-4"),

    html.Hr(),
    html.H3("📋 რეკომენდაციების ცხრილები"),

    dbc.Tabs([
        dbc.Tab(label="ფილტრაციის კოეფიციენტი", children=[
            dbc.Table([
                html.Thead(html.Tr([html.Th("კოეფიციენტი"), html.Th("პირობები"), html.Th("რეკომენდაცია")])),
                html.Tbody([
                    html.Tr([html.Td("< 1.0"), html.Td("სტაბილური ღვინო"), html.Td("ბენტონიტი არ არის საჭირო")]),
                    html.Tr([html.Td("1.0 – 1.5"), html.Td("მცირე დაბინდვის რისკი"), html.Td("დაბალი დოზა (0.5–1.0 გ/ლ)")]),
                    html.Tr([html.Td("1.5 – 2.0"), html.Td("ზომიერი დაბინდება"), html.Td("საშუალო დოზა (1.0–1.5 გ/ლ)")]),
                    html.Tr([html.Td("> 2.0"), html.Td("მაღალი ცილის შემცველობა"), html.Td("მაღალი დოზა (1.5–2.0 გ/ლ ან მეტი)")]),
                ])
            ], bordered=True, striped=True, hover=True)
        ]),
        dbc.Tab(label="pH-ის გავლენა", children=[
            dbc.Table([
                html.Thead(html.Tr([html.Th("pH"), html.Th("ცილების სტაბილურობა"), html.Th("კორექცია")])),
                html.Tbody([
                    html.Tr([html.Td("< 3.0"), html.Td("ნაკლები სტაბილურობა"), html.Td("+25%")]),
                    html.Tr([html.Td("3.0 – 3.6"), html.Td("ოპტიმალური"), html.Td("ცვლილება არ არის")]),
                    html.Tr([html.Td("> 3.6"), html.Td("უფრო სტაბილური ცილები"), html.Td("+15%")]),
                ])
            ], bordered=True, striped=True, hover=True)
        ]),
        dbc.Tab(label="ალკოჰოლის გავლენა", children=[
            dbc.Table([
                html.Thead(html.Tr([html.Th("ალკოჰოლი"), html.Th("ცილების ქცევა"), html.Th("კორექცია")])),
                html.Tbody([
                    html.Tr([html.Td("11.0%"), html.Td("მეტი ხსნადობა"), html.Td("+15%")]),
                    html.Tr([html.Td("12.0–14.0%"), html.Td("სტაბილური"), html.Td("ცვლილება არ არის")]),
                    html.Tr([html.Td("> 14.0%"), html.Td("დენატურაცია"), html.Td("–15%")]),
                ])
            ], bordered=True, striped=True, hover=True)
        ])
    ])
])

@app.callback(
    Output("result", "children"),
    Input("calc-btn", "n_clicks"),
    State("filtration", "value"),
    State("ph", "value"),
    State("alcohol", "value"),
    State("volume", "value"),
    State("bentonite", "value"),
    State("process_temp", "value"),
    State("contact_time", "value"),
    State("injection_method", "value"),
    prevent_initial_call=True
)
def calculate_dose(n, filtration, ph, alcohol, volume, bentonite,
                   process_temp, contact_time, injection_method):
    try:
        if None in [filtration, ph, alcohol, volume, bentonite]:
            return "❗️შეავსე ყველა ველი."

        if filtration < 1.0:
            base = 0.0
        elif 1.0 <= filtration < 1.5:
            base = 0.75
        elif 1.5 <= filtration <= 2.0:
            base = 1.25
        else:
            base = 1.75

        if ph < 3.0:
            base *= 1.25
        elif ph > 3.6:
            base *= 1.15

        if alcohol == 11.0:
            base *= 1.15
        elif alcohol > 14.0:
            base *= 0.85

        if bentonite == "sodium":
            base *= 1.2

        if process_temp is not None and process_temp < 10:
            base *= 1.15
        if contact_time is not None and contact_time < 8:
            base *= 1.2

        warnings = []
        if injection_method == "dry":
            warnings.append("⚠️ რეკომენდებულია ბენტონიტის წინასწარ გახსნა წყალში მინ. 12 საათით ადრე")

        dose = base * volume

        return html.Div([
            html.P(f"💡 {languages[lang]['result_label']}: {dose:.2f} გ (ერთ ლიტრზე: {base:.2f} გ/ლ)"),
            html.Ul([html.Li(w) for w in warnings]) if warnings else None
        ])

    except Exception as e:
        return f"შეცდომა: {e}"

if __name__ == '__main__':
    app.run(debug=True)
