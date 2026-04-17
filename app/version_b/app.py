# ============================================================
# app/version_b/app.py — Treatment Group
# Cinematic, full-screen immersive design. Large bold type,
# full-bleed color backgrounds per step, smooth animated
# transitions. Feels like a completely different product.
# ============================================================

import sys, time
from pathlib import Path
from shiny import App, ui, render, reactive

sys.path.append(str(Path(__file__).parent.parent))
from logger import log_session
from movies import MOODS, GENRES, LENGTH_LABELS, ERA_LABELS, recommend

MOOD_META = {
    "Excited":     {"emoji":"⚡","bg":"#1a0533","accent":"#c084fc","sub":"#7c3aed"},
    "Relaxed":     {"emoji":"🌊","bg":"#001a2e","accent":"#38bdf8","sub":"#0369a1"},
    "Adventurous": {"emoji":"🏔","bg":"#0f1a0a","accent":"#86efac","sub":"#16a34a"},
    "Tense":       {"emoji":"🔥","bg":"#1a0a00","accent":"#fb923c","sub":"#c2410c"},
    "Thoughtful":  {"emoji":"🌙","bg":"#0d0d1a","accent":"#a5b4fc","sub":"#4338ca"},
    "Emotional":   {"emoji":"💫","bg":"#1a0011","accent":"#f9a8d4","sub":"#be185d"},
    "Fun":         {"emoji":"🎉","bg":"#1a1500","accent":"#fde047","sub":"#ca8a04"},
    "Romantic":    {"emoji":"🌹","bg":"#1a0008","accent":"#fda4af","sub":"#be123c"},
}

GENRE_META = {
    "Action":      {"emoji":"💥","color":"#ef4444"},
    "Comedy":      {"emoji":"😂","color":"#f59e0b"},
    "Drama":       {"emoji":"🎭","color":"#8b5cf6"},
    "Sci-Fi":      {"emoji":"🚀","color":"#06b6d4"},
    "Horror":      {"emoji":"👻","color":"#64748b"},
    "Romance":     {"emoji":"💕","color":"#ec4899"},
    "Thriller":    {"emoji":"🔪","color":"#f97316"},
    "Documentary": {"emoji":"🎥","color":"#10b981"},
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

* { box-sizing:border-box; margin:0; padding:0; }

body {
    font-family:'Outfit',sans-serif;
    background:#080810;
    color:#fff;
    min-height:100vh;
    overflow-x:hidden;
}

/* ── Full-bleed step container ── */
.step-wrap {
    min-height:100vh;
    display:flex;
    flex-direction:column;
    justify-content:center;
    padding:40px 24px 80px;
    transition:background .6s ease;
    position:relative;
    overflow:hidden;
}
.step-wrap::before {
    content:'';
    position:absolute;
    inset:0;
    background:radial-gradient(ellipse at 20% 50%, var(--glow-color,transparent) 0%, transparent 60%);
    pointer-events:none;
}

/* ── Step counter strip ── */
.step-strip {
    position:fixed;
    top:0; left:0; right:0;
    height:4px;
    background:rgba(255,255,255,.08);
    z-index:100;
}
.step-strip-fill {
    height:100%;
    background:var(--accent,#fff);
    transition:width .5s cubic-bezier(.4,0,.2,1), background .6s ease;
}
.step-dots {
    position:fixed;
    bottom:24px;
    left:50%;
    transform:translateX(-50%);
    display:flex;
    gap:8px;
    z-index:100;
}
.dot {
    width:6px; height:6px;
    border-radius:50%;
    background:rgba(255,255,255,.2);
    transition:all .3s;
}
.dot.active { background:#fff; width:20px; border-radius:3px; }
.dot.done   { background:rgba(255,255,255,.5); }

/* ── Big headline ── */
.big-q {
    font-size:clamp(28px,6vw,52px);
    font-weight:800;
    line-height:1.1;
    letter-spacing:-1px;
    margin-bottom:10px;
    max-width:640px;
}
.big-sub {
    font-size:16px;
    color:rgba(255,255,255,.5);
    margin-bottom:36px;
    font-weight:300;
}

/* ── Mood cards ── */
.mood-grid {
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(130px,1fr));
    gap:12px;
    max-width:640px;
    margin-bottom:32px;
}
.mood-card {
    background:rgba(255,255,255,.04);
    border:1.5px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:20px 12px 16px;
    text-align:center;
    cursor:pointer;
    transition:all .2s ease;
    user-select:none;
}
.mood-card:hover {
    background:rgba(255,255,255,.08);
    border-color:rgba(255,255,255,.2);
    transform:translateY(-2px);
}
.mood-card.selected {
    border-color:var(--accent,#fff);
    background:rgba(255,255,255,.1);
    box-shadow:0 0 24px rgba(255,255,255,.08);
    transform:translateY(-2px);
}
.mood-icon { font-size:28px; display:block; margin-bottom:8px; }
.mood-label { font-size:13px; font-weight:600; color:rgba(255,255,255,.85); }

/* ── Genre chips ── */
.genre-grid {
    display:flex; flex-wrap:wrap; gap:10px;
    max-width:640px; margin-bottom:32px;
}
.genre-chip {
    padding:12px 20px;
    border:1.5px solid rgba(255,255,255,.1);
    border-radius:99px;
    background:rgba(255,255,255,.04);
    color:rgba(255,255,255,.7);
    font-size:15px;
    font-family:'Outfit',sans-serif;
    font-weight:400;
    cursor:pointer;
    transition:all .2s;
    user-select:none;
    display:flex; align-items:center; gap:8px;
}
.genre-chip:hover { border-color:rgba(255,255,255,.3); color:#fff; }
.genre-chip.selected {
    border-color:var(--chip-color,#fff);
    background:rgba(255,255,255,.08);
    color:#fff;
    box-shadow:0 0 0 1px var(--chip-color,#fff);
}

/* ── Prefs ── */
.pref-block { max-width:540px; margin-bottom:28px; }
.pref-label {
    font-size:11px; font-weight:600; letter-spacing:1.5px;
    text-transform:uppercase; color:rgba(255,255,255,.35);
    margin-bottom:12px;
}
.seg-row { display:flex; gap:8px; flex-wrap:wrap; }
.seg {
    padding:10px 18px;
    border:1.5px solid rgba(255,255,255,.1);
    border-radius:10px;
    background:transparent;
    color:rgba(255,255,255,.55);
    font-size:14px;
    font-family:'Outfit',sans-serif;
    cursor:pointer;
    transition:all .2s;
}
.seg:hover { border-color:rgba(255,255,255,.3); color:#fff; }
.seg.on { border-color:var(--accent,#fff); color:#fff; background:rgba(255,255,255,.06); }
.slider-row { display:flex; align-items:center; gap:16px; }
input[type=range] { flex:1; accent-color:var(--accent,#fff); }
.slider-val {
    font-size:22px; font-weight:800;
    color:var(--accent,#fff); min-width:48px;
}

/* ── Rec cards ── */
.rec-stack { max-width:640px; margin-bottom:28px; }
.rec-card {
    display:flex; align-items:center; gap:16px;
    padding:18px 20px;
    border:1.5px solid rgba(255,255,255,.07);
    border-radius:18px;
    background:rgba(255,255,255,.03);
    margin-bottom:10px;
    cursor:pointer;
    transition:all .2s;
}
.rec-card:hover { border-color:rgba(255,255,255,.2); background:rgba(255,255,255,.06); }
.rec-card.chosen {
    border-color:var(--accent,#fff);
    background:rgba(255,255,255,.07);
    box-shadow:0 0 28px rgba(255,255,255,.04);
}
.rec-icon-big { font-size:36px; flex-shrink:0; }
.rec-info { flex:1; }
.rec-title-big {
    font-size:17px; font-weight:700; color:#fff; margin-bottom:3px;
}
.rec-meta-row {
    font-size:12px; color:rgba(255,255,255,.4);
    display:flex; gap:12px; margin-bottom:4px;
}
.rec-stars { color:#fbbf24; font-size:13px; }
.rec-genres-row {
    display:flex; gap:6px; flex-wrap:wrap; margin-top:6px;
}
.rec-genre-tag {
    padding:2px 10px; border-radius:99px;
    font-size:11px; font-weight:600;
    background:rgba(255,255,255,.07);
    color:rgba(255,255,255,.5);
}
.chosen-check {
    width:28px; height:28px; border-radius:50%;
    border:2px solid rgba(255,255,255,.15);
    display:flex; align-items:center; justify-content:center;
    font-size:14px; flex-shrink:0; transition:all .2s;
}
.rec-card.chosen .chosen-check {
    background:var(--accent,#fff);
    border-color:var(--accent,#fff);
    color:#000;
}

/* ── Final screen ── */
.final-hero {
    max-width:600px;
    text-align:center;
    margin-bottom:32px;
}
.final-icon-big {
    font-size:80px;
    display:block;
    margin-bottom:20px;
    filter:drop-shadow(0 0 32px rgba(255,255,255,.15));
}
.final-title-big {
    font-size:clamp(24px,5vw,40px);
    font-weight:800;
    letter-spacing:-1px;
    margin-bottom:8px;
}
.final-rating { font-size:16px; color:rgba(255,255,255,.4); margin-bottom:32px; }
.plan-cards {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
    max-width:520px;
    margin:0 auto;
    text-align:left;
}
.plan-card {
    background:rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    border-radius:14px;
    padding:16px 18px;
}
.plan-card-label {
    font-size:10px; font-weight:600; letter-spacing:1.5px;
    text-transform:uppercase; color:rgba(255,255,255,.3);
    margin-bottom:6px;
}
.plan-card-val { font-size:14px; color:rgba(255,255,255,.85); font-weight:400; }

/* ── Buttons ── */
.cta-row { display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
.cta {
    padding:16px 36px;
    background:var(--accent,#fff);
    color:#000;
    border:none;
    border-radius:14px;
    font-size:16px;
    font-weight:700;
    font-family:'Outfit',sans-serif;
    cursor:pointer;
    transition:transform .15s, opacity .15s;
    letter-spacing:-.2px;
}
.cta:hover { transform:translateY(-2px); opacity:.9; }
.cta-ghost {
    padding:16px 28px;
    background:transparent;
    color:rgba(255,255,255,.45);
    border:1.5px solid rgba(255,255,255,.12);
    border-radius:14px;
    font-size:15px;
    font-family:'Outfit',sans-serif;
    cursor:pointer;
    transition:all .15s;
}
.cta-ghost:hover { border-color:rgba(255,255,255,.3); color:rgba(255,255,255,.7); }

.err { color:#f87171; font-size:13px; margin-top:10px; }
.version-tag {
    position:fixed; bottom:10px; right:14px;
    font-size:10px; color:rgba(255,255,255,.2);
    font-family:'Outfit',sans-serif;
}
"""

JS = """
<script>
var _t0=Date.now(), _mood="", _genres=[], _pick="";

function setAccent(color) {
    document.documentElement.style.setProperty('--accent', color);
}
function setGlow(color) {
    document.documentElement.style.setProperty('--glow-color', color);
}
function selectMood(val, accent, bg) {
    _mood = val;
    document.querySelectorAll('.mood-card').forEach(c=>c.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    document.body.style.background = bg;
    setAccent(accent);
    setGlow(accent+'33');
    Shiny.setInputValue('js_mood', val, {priority:'event'});
    Shiny.setInputValue('js_accent', accent, {priority:'event'});
}
function toggleGenre(val, color, el) {
    var idx=_genres.indexOf(val);
    if(idx===-1){_genres.push(val); el.classList.add('selected'); el.style.setProperty('--chip-color',color);}
    else{_genres.splice(idx,1); el.classList.remove('selected');}
    Shiny.setInputValue('js_genres', _genres.join(','), {priority:'event'});
}
function setSeg(type, val, el) {
    el.closest('.seg-row').querySelectorAll('.seg').forEach(b=>b.classList.remove('on'));
    el.classList.add('on');
    Shiny.setInputValue('js_'+type, val, {priority:'event'});
}
function setRating(val) {
    document.getElementById('sv').textContent = parseFloat(val).toFixed(1);
    Shiny.setInputValue('js_rating', parseFloat(val));
}
function pickMovie(title, el) {
    _pick = title;
    document.querySelectorAll('.rec-card').forEach(c=>{
        c.classList.remove('chosen');
        var chk=c.querySelector('.chosen-check');
        if(chk) chk.textContent='';
    });
    el.classList.add('chosen');
    var chk=el.querySelector('.chosen-check');
    if(chk) chk.textContent='✓';
    Shiny.setInputValue('js_pick', title, {priority:'event'});
}
function goNext(step) {
    Shiny.setInputValue('js_step', step, {priority:'event'});
    Shiny.setInputValue('js_time', Math.round((Date.now()-_t0)/1000));
    window.scrollTo({top:0, behavior:'smooth'});
}
function goBack(step) {
    Shiny.setInputValue('js_step', step, {priority:'event'});
    window.scrollTo({top:0, behavior:'smooth'});
}
setInterval(function(){
    Shiny.setInputValue('js_time', Math.round((Date.now()-_t0)/1000));
}, 4000);
</script>
"""

def dots(current):
    return "".join([
        f'<div class="dot {"active" if i==current else "done" if i<current else ""}"></div>'
        for i in range(1,6)
    ])

def strip(current, accent="#fff"):
    pct = (current-1)/4*100
    return f"""
    <div class="step-strip">
        <div class="step-strip-fill" style="width:{pct}%; --accent:{accent};"></div>
    </div>
    <div class="step-dots">{dots(current)}</div>
    """

app_ui = ui.page_fluid(
    ui.tags.head(ui.tags.style(CSS)),
    ui.HTML(JS),
    ui.output_ui("quiz_body"),
    ui.div({"class":"version-tag"}, "v.B"),
)

def server(input, output, session):
    t0 = time.time()
    step       = reactive.value(1)
    mood       = reactive.value("")
    accent     = reactive.value("#c084fc")
    genres     = reactive.value([])
    length     = reactive.value("any")
    era        = reactive.value("any")
    min_rating = reactive.value(7.0)
    pick       = reactive.value("")
    max_step   = reactive.value(1)

    @reactive.effect
    def _s():
        try:
            s=int(input.js_step()); step.set(s)
            if s>max_step.get(): max_step.set(s)
        except: pass
    @reactive.effect
    def _m():
        try: mood.set(input.js_mood())
        except: pass
    @reactive.effect
    def _ac():
        try: accent.set(input.js_accent())
        except: pass
    @reactive.effect
    def _g():
        try:
            r=input.js_genres()
            genres.set([x for x in r.split(",") if x] if r else [])
        except: pass
    @reactive.effect
    def _p():
        try: pick.set(input.js_pick())
        except: pass

    @render.ui
    def quiz_body():
        s = step.get()
        ac = accent.get()
        bg = MOOD_META.get(mood.get(), {}).get("bg", "#080810")

        # ── Step 1: Mood ─────────────────────────────────────
        if s == 1:
            cards = "".join([
                f'<div class="mood-card" onclick="selectMood(\'{m}\',\'{MOOD_META[m]["accent"]}\',\'{MOOD_META[m]["bg"]}\')">'
                f'<span class="mood-icon">{MOOD_META[m]["emoji"]}</span>'
                f'<span class="mood-label">{m}</span>'
                f'</div>'
                for m in MOODS
            ])
            return ui.HTML(f"""
                {strip(1)}
                <div class="step-wrap" style="background:{bg}; --glow-color:{ac}33;">
                    <div class="big-q">How are you<br>feeling tonight?</div>
                    <div class="big-sub">Your mood is the starting point for everything.</div>
                    <div class="mood-grid">{cards}</div>
                    <div class="err" id="e1"></div>
                    <div class="cta-row">
                        <button class="cta" style="background:{ac}; color:#000;" onclick="
                            if(!_mood){{document.getElementById('e1').textContent='Pick a mood to continue.';return;}}
                            goNext(2)">Let's go →</button>
                    </div>
                </div>
            """)

        # ── Step 2: Genres ───────────────────────────────────
        elif s == 2:
            chips = "".join([
                f'<button class="genre-chip" style="--chip-color:{GENRE_META[g]["color"]};"'
                f' onclick="toggleGenre(\'{g}\',\'{GENRE_META[g]["color"]}\',this)">'
                f'{GENRE_META[g]["emoji"]} {g}'
                f'</button>'
                for g in GENRES
            ])
            return ui.HTML(f"""
                {strip(2, ac)}
                <div class="step-wrap" style="background:{bg};">
                    <div class="big-q">What kind of<br>story calls to you?</div>
                    <div class="big-sub">Pick as many as you want.</div>
                    <div class="genre-grid">{chips}</div>
                    <div class="err" id="e2"></div>
                    <div class="cta-row">
                        <button class="cta-ghost" onclick="goBack(1)">← Back</button>
                        <button class="cta" style="background:{ac}; color:#000;" onclick="
                            if(_genres.length===0){{document.getElementById('e2').textContent='Pick at least one genre.';return;}}
                            goNext(3)">Continue →</button>
                    </div>
                </div>
            """)

        # ── Step 3: Preferences ──────────────────────────────
        elif s == 3:
            l_segs = "".join([
                f'<button class="seg{"  on" if k=="any" else ""}" onclick="setSeg(\'length\',\'{k}\',this)">{v}</button>'
                for k,v in [("any","Any"),("short","Short"),("medium","Medium"),("long","Long")]
            ])
            e_segs = "".join([
                f'<button class="seg{"  on" if k=="any" else ""}" onclick="setSeg(\'era\',\'{k}\',this)">{v}</button>'
                for k,v in [("any","Any era"),("classic","Classic"),("modern","Modern")]
            ])
            return ui.HTML(f"""
                {strip(3, ac)}
                <div class="step-wrap" style="background:{bg};">
                    <div class="big-q">Make it<br>yours.</div>
                    <div class="big-sub">Fine-tune so we find the perfect match.</div>
                    <div class="pref-block">
                        <div class="pref-label">Length</div>
                        <div class="seg-row" style="--accent:{ac};">{l_segs}</div>
                    </div>
                    <div class="pref-block">
                        <div class="pref-label">Era</div>
                        <div class="seg-row" style="--accent:{ac};">{e_segs}</div>
                    </div>
                    <div class="pref-block">
                        <div class="pref-label">Minimum rating</div>
                        <div class="slider-row">
                            <input type="range" min="5" max="9" step="0.5" value="7"
                                   style="--accent:{ac};" oninput="setRating(this.value)">
                            <span class="slider-val" style="color:{ac};" id="sv">7.0</span>
                        </div>
                    </div>
                    <div class="cta-row">
                        <button class="cta-ghost" onclick="goBack(2)">← Back</button>
                        <button class="cta" style="background:{ac}; color:#000;" onclick="goNext(4)">
                            Find my movies →</button>
                    </div>
                </div>
            """)

        # ── Step 4: Recommendations ──────────────────────────
        elif s == 4:
            try: length.set(input.js_length())
            except: pass
            try: era.set(input.js_era())
            except: pass
            try: min_rating.set(float(input.js_rating()))
            except: pass

            recs = recommend(mood.get(), genres.get(), length.get(), era.get(), min_rating.get())
            if not recs:
                return ui.HTML(f"""
                    {strip(4, ac)}
                    <div class="step-wrap" style="background:{bg};">
                        <div class="big-q">No matches found.</div>
                        <div class="big-sub">Try loosening your preferences — especially rating or era.</div>
                        <div class="cta-row">
                            <button class="cta-ghost" onclick="goBack(3)">← Adjust</button>
                        </div>
                    </div>
                """)

            cards = ""
            for r in recs:
                stars = "★"*int(r["rating"]) + "☆"*(10-int(r["rating"]))
                genre_tags = "".join([f'<span class="rec-genre-tag">{g}</span>' for g in r["genre"]])
                cards += f"""
                <div class="rec-card" onclick="pickMovie('{r['title']}', this)">
                    <div class="rec-icon-big">{r['emoji']}</div>
                    <div class="rec-info">
                        <div class="rec-title-big">{r['title']}</div>
                        <div class="rec-meta-row">
                            <span>{r['year']}</span>
                            <span>{r['length'].capitalize()}</span>
                            <span>{r['era'].capitalize()}</span>
                        </div>
                        <div class="rec-stars">{stars[:10]} {r['rating']}</div>
                        <div class="rec-genres-row">{genre_tags}</div>
                    </div>
                    <div class="chosen-check"></div>
                </div>"""

            return ui.HTML(f"""
                {strip(4, ac)}
                <div class="step-wrap" style="background:{bg};">
                    <div class="big-q">Your picks.</div>
                    <div class="big-sub">Tap one to select it, then continue.</div>
                    <div class="rec-stack">{cards}</div>
                    <div class="err" id="e4"></div>
                    <div class="cta-row">
                        <button class="cta-ghost" onclick="goBack(3)">← Back</button>
                        <button class="cta" style="background:{ac}; color:#000;" onclick="
                            if(!_pick){{document.getElementById('e4').textContent='Tap a movie first.';return;}}
                            goNext(5)">Build my night →</button>
                    </div>
                </div>
            """)

        # ── Step 5: Watch Plan ───────────────────────────────
        elif s == 5:
            chosen = pick.get()
            from movies import MOVIES as ALL
            movie = next((m for m in ALL if m["title"] == chosen), None)
            if not movie:
                return ui.HTML(f"{strip(5,ac)}<div class='step-wrap'><p>Error. <button onclick='goBack(4)'>Go back</button></p></div>")

            snack = {"Excited":"Popcorn & energy drink","Relaxed":"Tea & blanket",
                     "Tense":"Stress snacks","Fun":"Soda & chips",
                     "Thoughtful":"Coffee & notebook","Emotional":"Chocolate & tissues",
                     "Adventurous":"Smoothie & trail mix","Romantic":"Wine & candles"
                    }.get(mood.get(),"Popcorn")
            length_note = {"short":"Under 100 min — great for tonight",
                           "medium":"~2 hours — clear your evening",
                           "long":"2h+ — commit fully"}.get(movie["length"],"")

            return ui.HTML(f"""
                {strip(5, ac)}
                <div class="step-wrap" style="background:{bg}; text-align:center;">
                    <div class="final-hero">
                        <span class="final-icon-big">{movie['emoji']}</span>
                        <div class="final-title-big">{movie['title']}</div>
                        <div class="final-rating">★ {movie['rating']} &nbsp;·&nbsp; {movie['year']}</div>
                        <div class="plan-cards">
                            <div class="plan-card">
                                <div class="plan-card-label">Length</div>
                                <div class="plan-card-val">{length_note}</div>
                            </div>
                            <div class="plan-card">
                                <div class="plan-card-label">Snack pairing</div>
                                <div class="plan-card-val">{snack}</div>
                            </div>
                            <div class="plan-card">
                                <div class="plan-card-label">Where to watch</div>
                                <div class="plan-card-val">Check JustWatch.com</div>
                            </div>
                            <div class="plan-card">
                                <div class="plan-card-label">Pro tip</div>
                                <div class="plan-card-val">Go in blind — no trailers</div>
                            </div>
                        </div>
                    </div>
                    <div class="cta-row" style="justify-content:center;">
                        <button class="cta-ghost" onclick="goBack(4)">← Change pick</button>
                        <button class="cta" id="done-btn" style="background:{ac}; color:#000;" onclick="
                            Shiny.setInputValue('js_done',true,{{priority:'event'}});
                            this.textContent='🎬 Enjoy the movie!';
                            this.style.background='#22c55e';
                            this.disabled=true;">
                            I'm ready to watch →</button>
                    </div>
                </div>
            """)

    async def _end():
        elapsed = time.time() - t0
        try: n = len(genres.get())
        except: n = 0
        log_session("B", elapsed, max_step.get(), max_step.get()>=5,
                    n, mood.get() or "none", bool(pick.get()))
    session.on_ended(_end)

app = App(app_ui, server)