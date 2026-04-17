# ============================================================
# app/version_a/app.py — Control Group
# INTENTIONALLY plain: government-form aesthetic, Times New Roman,
# no color, no personality. Makes the A/B difference unmistakable.
# ============================================================

import sys, time
from pathlib import Path
from shiny import App, ui, render, reactive

sys.path.append(str(Path(__file__).parent.parent))
from logger import log_session
from movies import MOODS, GENRES, LENGTH_LABELS, ERA_LABELS, recommend

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Times New Roman', Times, serif;
    background: #ffffff;
    color: #000000;
    font-size: 14px;
    line-height: 1.5;
}
.page {
    max-width: 580px;
    margin: 30px auto;
    padding: 0 20px 60px;
}
.site-header {
    border-bottom: 2px solid #000;
    padding-bottom: 8px;
    margin-bottom: 24px;
}
.site-header h1 {
    font-size: 16px;
    font-weight: bold;
    letter-spacing: 0;
}
.site-header p {
    font-size: 12px;
    color: #444;
}
.step-counter {
    font-size: 12px;
    color: #555;
    margin-bottom: 6px;
    font-family: Arial, sans-serif;
}
h2 {
    font-size: 15px;
    font-weight: bold;
    margin-bottom: 16px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 6px;
}
.instruction {
    font-size: 13px;
    color: #333;
    margin-bottom: 12px;
    font-style: italic;
}
.option-list {
    list-style: none;
    margin-bottom: 16px;
}
.option-list li {
    margin-bottom: 4px;
}
.option-list label {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 4px 0;
    font-size: 14px;
}
.option-list input[type=radio],
.option-list input[type=checkbox] {
    width: 14px;
    height: 14px;
    cursor: pointer;
    flex-shrink: 0;
}
.form-row {
    margin-bottom: 14px;
}
.form-row label {
    display: block;
    font-size: 13px;
    font-weight: bold;
    margin-bottom: 4px;
}
.form-row select {
    width: 100%;
    padding: 5px 6px;
    border: 1px solid #999;
    border-radius: 0;
    font-size: 13px;
    font-family: 'Times New Roman', serif;
    background: white;
}
.form-row input[type=range] {
    width: 100%;
    margin-top: 4px;
}
.rating-note {
    font-size: 12px;
    color: #555;
    margin-top: 2px;
}
.btn-row {
    display: flex;
    gap: 10px;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #ccc;
}
.btn-next {
    padding: 6px 20px;
    background: #000;
    color: #fff;
    border: 1px solid #000;
    font-family: Arial, sans-serif;
    font-size: 13px;
    cursor: pointer;
    border-radius: 0;
}
.btn-next:hover { background: #333; }
.btn-back {
    padding: 6px 20px;
    background: #fff;
    color: #000;
    border: 1px solid #999;
    font-family: Arial, sans-serif;
    font-size: 13px;
    cursor: pointer;
    border-radius: 0;
}
.btn-back:hover { background: #f5f5f5; }
.rec-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
    font-size: 13px;
}
.rec-table th {
    text-align: left;
    border-bottom: 2px solid #000;
    padding: 4px 8px;
    font-size: 12px;
    font-family: Arial, sans-serif;
    font-weight: bold;
}
.rec-table td {
    padding: 6px 8px;
    border-bottom: 1px solid #ddd;
    vertical-align: top;
}
.rec-table tr:hover td { background: #f9f9f9; }
.rec-table tr.picked td { background: #ffffcc; }
.pick-radio { cursor: pointer; }
.final-box {
    border: 1px solid #000;
    padding: 16px;
    margin-bottom: 16px;
}
.final-box h3 { font-size: 15px; margin-bottom: 10px; }
.final-box ul { padding-left: 20px; }
.final-box ul li { margin-bottom: 6px; font-size: 13px; }
.error { color: #cc0000; font-size: 12px; margin-top: 6px;
         font-family: Arial, sans-serif; }
.version-tag {
    position: fixed; bottom: 8px; right: 10px;
    font-size: 10px; color: #aaa; font-family: Arial, sans-serif;
}
"""

JS = """
<script>
var _t0 = Date.now();
var _mood = "";
var _genres = [];
var _pick = "";

function selectMood(val) {
    _mood = val;
    Shiny.setInputValue('js_mood', val, {priority:'event'});
}
function toggleGenre(val) {
    var idx = _genres.indexOf(val);
    if (idx === -1) _genres.push(val);
    else _genres.splice(idx, 1);
    Shiny.setInputValue('js_genres', _genres.join(','), {priority:'event'});
}
function selectPick(val) {
    _pick = val;
    document.querySelectorAll('.rec-table tr').forEach(function(r){r.classList.remove('picked');});
    var row = document.getElementById('row-' + val.replace(/[^a-zA-Z0-9]/g,'_'));
    if (row) row.classList.add('picked');
    Shiny.setInputValue('js_pick', val, {priority:'event'});
}
function goNext(step) {
    Shiny.setInputValue('js_step', step, {priority:'event'});
    Shiny.setInputValue('js_time', Math.round((Date.now()-_t0)/1000));
}
function goBack(step) {
    Shiny.setInputValue('js_step', step, {priority:'event'});
}
setInterval(function(){
    Shiny.setInputValue('js_time', Math.round((Date.now()-_t0)/1000));
}, 4000);
</script>
"""

app_ui = ui.page_fluid(
    ui.tags.head(ui.tags.style(CSS)),
    ui.HTML(JS),
    ui.div({"class": "page"},
        ui.div({"class": "site-header"},
            ui.tags.h1("Movie Recommendation Form"),
            ui.tags.p("Complete all steps to receive your recommendation."),
        ),
        ui.output_ui("quiz_body"),
    ),
    ui.div({"class": "version-tag"}, "v.A"),
)

def server(input, output, session):
    t0 = time.time()
    step       = reactive.value(1)
    mood       = reactive.value("")
    genres     = reactive.value([])
    length     = reactive.value("any")
    era        = reactive.value("any")
    min_rating = reactive.value(7.0)
    pick       = reactive.value("")
    max_step   = reactive.value(1)

    @reactive.effect
    def _s():
        try:
            s = int(input.js_step())
            step.set(s)
            if s > max_step.get(): max_step.set(s)
        except: pass
    @reactive.effect
    def _m():
        try: mood.set(input.js_mood())
        except: pass
    @reactive.effect
    def _g():
        try:
            r = input.js_genres()
            genres.set([x for x in r.split(",") if x] if r else [])
        except: pass
    @reactive.effect
    def _p():
        try: pick.set(input.js_pick())
        except: pass

    @render.ui
    def quiz_body():
        s = step.get()

        # ── Step 1 ──────────────────────────────────────────
        if s == 1:
            opts = "".join([
                f'<li><label>'
                f'<input type="radio" name="mood" value="{m}" onchange="selectMood(\'{m}\')">'
                f'{m}</label></li>'
                for m in MOODS
            ])
            return ui.HTML(f"""
                <div class="step-counter">Step 1 of 5</div>
                <h2>Current Mood</h2>
                <p class="instruction">Select the option that best describes your current mood.</p>
                <ul class="option-list">{opts}</ul>
                <div class="error" id="e1"></div>
                <div class="btn-row">
                    <button class="btn-next" onclick="
                        if(!_mood){{document.getElementById('e1').textContent='Please make a selection.';return;}}
                        goNext(2)">Next &gt;</button>
                </div>
            """)

        # ── Step 2 ──────────────────────────────────────────
        elif s == 2:
            opts = "".join([
                f'<li><label>'
                f'<input type="checkbox" value="{g}" onchange="toggleGenre(\'{g}\')">'
                f'{g}</label></li>'
                for g in GENRES
            ])
            return ui.HTML(f"""
                <div class="step-counter">Step 2 of 5</div>
                <h2>Genre Preferences</h2>
                <p class="instruction">Select one or more genres. You may select multiple.</p>
                <ul class="option-list">{opts}</ul>
                <div class="error" id="e2"></div>
                <div class="btn-row">
                    <button class="btn-back" onclick="goBack(1)">&lt; Back</button>
                    <button class="btn-next" onclick="
                        if(_genres.length===0){{document.getElementById('e2').textContent='Select at least one genre.';return;}}
                        goNext(3)">Next &gt;</button>
                </div>
            """)

        # ── Step 3 ──────────────────────────────────────────
        elif s == 3:
            l_opts = "".join([f'<option value="{k}">{v}</option>'
                              for k,v in [("any","No preference")]+list(LENGTH_LABELS.items())])
            e_opts = "".join([f'<option value="{k}">{v}</option>'
                              for k,v in [("any","No preference")]+list(ERA_LABELS.items())])
            return ui.HTML(f"""
                <div class="step-counter">Step 3 of 5</div>
                <h2>Additional Preferences</h2>
                <p class="instruction">Complete the fields below. All fields are optional.</p>
                <div class="form-row">
                    <label for="len_sel">Preferred Length</label>
                    <select id="len_sel" onchange="Shiny.setInputValue('js_length',this.value)">{l_opts}</select>
                </div>
                <div class="form-row">
                    <label for="era_sel">Preferred Era</label>
                    <select id="era_sel" onchange="Shiny.setInputValue('js_era',this.value)">{e_opts}</select>
                </div>
                <div class="form-row">
                    <label>Minimum Acceptable Rating (1–10):
                        <span id="rv">7.0</span>
                    </label>
                    <input type="range" min="5" max="9" step="0.5" value="7"
                           oninput="document.getElementById('rv').textContent=parseFloat(this.value).toFixed(1);
                                    Shiny.setInputValue('js_rating',parseFloat(this.value))">
                    <p class="rating-note">Slide left to include lower-rated films.</p>
                </div>
                <div class="btn-row">
                    <button class="btn-back" onclick="goBack(2)">&lt; Back</button>
                    <button class="btn-next" onclick="goNext(4)">View Results &gt;</button>
                </div>
            """)

        # ── Step 4 ──────────────────────────────────────────
        elif s == 4:
            try: length.set(input.js_length())
            except: pass
            try: era.set(input.js_era())
            except: pass
            try: min_rating.set(float(input.js_rating()))
            except: pass

            recs = recommend(mood.get(), genres.get(), length.get(), era.get(), min_rating.get())
            if not recs:
                return ui.HTML("""
                    <div class="step-counter">Step 4 of 5</div>
                    <h2>Results</h2>
                    <p>No results matched your criteria. Please go back and broaden your preferences.</p>
                    <div class="btn-row">
                        <button class="btn-back" onclick="goBack(3)">&lt; Back</button>
                    </div>
                """)

            rows = "".join([
                f'<tr id="row_{r["title"].replace(" ","_").replace(":","")}"">'
                f'<td><input type="radio" class="pick-radio" name="pick" '
                f'onchange="selectPick(\'{r["title"]}\')"></td>'
                f'<td>{r["emoji"]} {r["title"]}</td>'
                f'<td>{r["year"]}</td>'
                f'<td>{r["rating"]}</td>'
                f'<td>{", ".join(r["genre"])}</td>'
                f'</tr>'
                for r in recs
            ])

            return ui.HTML(f"""
                <div class="step-counter">Step 4 of 5</div>
                <h2>Recommended Results</h2>
                <p class="instruction">
                    The following films match your criteria. Select one using the radio button,
                    then click Next.
                </p>
                <table class="rec-table">
                    <tr>
                        <th style="width:30px;"></th>
                        <th>Title</th><th>Year</th><th>Rating</th><th>Genre(s)</th>
                    </tr>
                    {rows}
                </table>
                <div class="error" id="e4"></div>
                <div class="btn-row">
                    <button class="btn-back" onclick="goBack(3)">&lt; Back</button>
                    <button class="btn-next" onclick="
                        if(!_pick){{document.getElementById('e4').textContent='Please select a film.';return;}}
                        goNext(5)">Next &gt;</button>
                </div>
            """)

        # ── Step 5 ──────────────────────────────────────────
        elif s == 5:
            chosen = pick.get()
            from movies import MOVIES as ALL
            movie = next((m for m in ALL if m["title"] == chosen), None)
            if not movie:
                return ui.HTML("<p>Error. <button onclick='goBack(4)'>Go back</button></p>")

            snack = {"Excited":"Popcorn","Relaxed":"Tea","Tense":"Snacks","Fun":"Soda",
                     "Thoughtful":"Coffee","Emotional":"Chocolate","Adventurous":"Smoothie",
                     "Romantic":"Wine"}.get(mood.get(),"Popcorn")
            length_note = {"short":"Under 100 minutes","medium":"Approximately 2 hours",
                           "long":"Over 2 hours"}.get(movie["length"],"")

            return ui.HTML(f"""
                <div class="step-counter">Step 5 of 5</div>
                <h2>Your Recommendation</h2>
                <div class="final-box">
                    <h3>{movie['emoji']} {movie['title']} ({movie['year']})</h3>
                    <ul>
                        <li><strong>Rating:</strong> {movie['rating']} / 10</li>
                        <li><strong>Length:</strong> {length_note}</li>
                        <li><strong>Genre(s):</strong> {', '.join(movie['genre'])}</li>
                        <li><strong>Suggested snack:</strong> {snack}</li>
                        <li><strong>Where to watch:</strong> Check JustWatch.com</li>
                    </ul>
                </div>
                <div class="btn-row">
                    <button class="btn-back" onclick="goBack(4)">&lt; Change selection</button>
                    <button class="btn-next" onclick="
                        Shiny.setInputValue('js_done',true,{{priority:'event'}});
                        this.textContent='Saved.'; this.disabled=true;">
                        Submit &#10003;</button>
                </div>
            """)

    async def _end():
        elapsed = time.time() - t0
        try: n = len(genres.get())
        except: n = 0
        log_session("A", elapsed, max_step.get(), max_step.get()>=5,
                    n, mood.get() or "none", bool(pick.get()))
    session.on_ended(_end)

app = App(app_ui, server)