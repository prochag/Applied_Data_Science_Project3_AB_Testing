# Project 3: A/B Testing — Movie Night Recommendation Quiz

## Research Question
Does a polished, animated UI (Version B) lead to higher quiz completion rates and deeper engagement compared to a plain UI (Version A) in a 5-step interactive recommendation quiz?

## Versions
| | Version A (Control) | Version B (Treatment) |
|---|---|---|
| Style | Plain, minimal, light | Dark, animated, gradient cards |
| Progress | Step X of 5 label | Animated progress bar with labels |
| Mood select | Text buttons | Emoji pill buttons |
| Genre select | Text buttons | Emoji tile grid |
| Rec cards | Simple bordered boxes | Glowing interactive cards |
| Final step | Basic text box | Hero card with plan grid |

## Metrics tracked per session
| Column | Description |
|---|---|
| `steps_completed` | Furthest step reached (1–5) |
| `reached_step5` | Whether user completed the full quiz |
| `made_final_pick` | Whether user selected a movie on step 4 |
| `time_on_page` | Total seconds in the app |
| `genre_selections` | Number of genres selected |
| `mood_selection` | Which mood was chosen |


## Set Up Details (for purposes of reproducing this test)

1. Create Google Sheet with tab named `logs` and headers:
   `session_id, group, timestamp, time_on_page, steps_completed, reached_step5, genre_selections, mood_selection, made_final_pick`
2. Deploy Google Apps Script → paste URL into `app/logger.py`
3. `pip install -r requirements.txt rsconnect-python`
4. Deploy all three apps to shinyapps.io:
   ```bash
   rsconnect deploy shiny app/version_a --name YOUR_ACCOUNT --title version_a
   rsconnect deploy shiny app/version_b --name YOUR_ACCOUNT --title version_b
   rsconnect deploy shiny app/router    --name YOUR_ACCOUNT --title router
   ```
5. Update `URL_A` and `URL_B` in `app/router/app.py`, redeploy router
6. Share: `https://YOUR_ACCOUNT.shinyapps.io/router`

## Run analysis
```bash
# Set SHEET_ID in analysis/analysis.py first
python analysis/analysis.py
```
