# ============================================================
# app/router/app.py — Random Assignment Router
# Share ONLY this URL with participants.
# Update URL_A and URL_B after deploying version_a and version_b.
# ============================================================

from shiny import App, ui

URL_A = "https://prochag.shinyapps.io/version_a/"
URL_B = "https://prochag.shinyapps.io/version_b/"

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style("""
            body { background:#0d0f18; margin:0; display:flex;
                   align-items:center; justify-content:center; height:100vh; }
            .wrap { text-align:center; color:#6b7280;
                    font-family:'DM Sans',sans-serif; }
            .spinner { width:40px; height:40px; margin:0 auto 16px;
                       border:3px solid #1e2236;
                       border-top-color:#6366f1; border-radius:50%;
                       animation:spin .8s linear infinite; }
            @keyframes spin { to { transform:rotate(360deg); } }
            p { font-size:14px; }
        """),
        ui.tags.script(f"""
            var group = Math.random() < 0.5 ? 'A' : 'B';
            var dest  = group === 'A' ? '{URL_A}' : '{URL_B}';
            window.location.replace(dest + '?group=' + group);
        """),
    ),
    ui.div({"class":"wrap"},
        ui.div({"class":"spinner"}),
        ui.p("Finding your perfect movie night…"),
    ),
)

def server(input, output, session): pass

app = App(app_ui, server)