# ============================================================
# app/logger.py — Shared session logging to Google Sheets
#
# SETUP (one-time):
# 1. Create a Google Sheet, rename tab to "logs", add headers:
#    session_id | group | timestamp | time_on_page |
#    steps_completed | reached_step5 | genre_selections |
#    mood_selection | made_final_pick
#
# 2. Share sheet as "Anyone with link → Viewer"
#    Copy the Sheet ID from the URL.
#
# 3. Go to script.google.com → New Project → paste this:
#
#   function doPost(e) {
#     var sheet = SpreadsheetApp.openById("YOUR_SHEET_ID")
#                               .getSheetByName("logs");
#     var d = JSON.parse(e.postData.contents);
#     sheet.appendRow([
#       d.session_id, d.group, d.timestamp, d.time_on_page,
#       d.steps_completed, d.reached_step5, d.genre_selections,
#       d.mood_selection, d.made_final_pick
#     ]);
#     return ContentService
#       .createTextOutput(JSON.stringify({status:"ok"}))
#       .setMimeType(ContentService.MimeType.JSON);
#   }
#
# 4. Deploy → New Deployment → Web App
#    Execute as: Me | Who has access: Anyone
#    Copy the deployment URL → paste as APPS_SCRIPT_URL below.
# ============================================================

import urllib.request
import urllib.error
import json
import random
import string
from datetime import datetime

# ---- PASTE YOUR APPS SCRIPT DEPLOYMENT URL HERE ----
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwV50vAewiiCdP_eRw-quwdHXTos3D7FUX9cNIb0y54cPj4d3BmSFj8fn9D8uoxkzbLTw/exec"


def log_session(
    group: str,
    time_on_page: float,
    steps_completed: int,
    reached_step5: bool,
    genre_selections: int,
    mood_selection: str,
    made_final_pick: bool,
) -> bool:
    session_id = (
        f"{group}-{datetime.now().strftime('%Y%m%d%H%M%S')}-"
        f"{''.join(random.choices(string.digits, k=4))}"
    )
    payload = json.dumps({
        "session_id":       session_id,
        "group":            group,
        "timestamp":        datetime.now().isoformat(),
        "time_on_page":     round(time_on_page, 1),
        "steps_completed":  steps_completed,
        "reached_step5":    int(reached_step5),
        "genre_selections": genre_selections,
        "mood_selection":   mood_selection,
        "made_final_pick":  int(made_final_pick),
    }).encode("utf-8")

    req = urllib.request.Request(
        APPS_SCRIPT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            result = json.loads(resp.read().decode())
            return result.get("status") == "ok"
    except Exception:
        return False  # never crash the app over logging