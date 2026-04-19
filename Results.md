# A/B Test Results : Movie Recommendation Quiz

## Sample

| | Version A (Plain) | Version B (Cinematic) | Total |
|---|---|---|---|
| Sessions | 41 | 35 | 76 |
| Completion rate | 100% | 100% | 100% |

---

## Descriptive Statistics

| Metric | Version A | Version B |
|---|---|---|
| Mean steps completed | 5.00 | 5.00 |
| Quiz completion rate | 100.0% | 100.0% |
| Final pick rate | 100.0% | 100.0% |
| Mean time on page (s) | 47.0 | 79.6 |
| Mean genres selected | 2.39 | 2.57 |

---

## Statistical Tests

| # | Metric | Test | A | B | p-value | Result |
|---|---|---|---|---|---|---|
| 1 | Steps completed | Mann-Whitney U | 5.00 | 5.00 | 1.0000 | Not significant |
| 2 | Quiz completion | Fisher's exact | 100% | 100% | — | No variation (positive) |
| 3 | Final pick rate | Fisher's exact | 100% | 100% | — | No variation (positive) |
| 4 | Time on page | Wilcoxon rank-sum | 47.2s | 50.0s | **0.0443** | **Significant** |
| 5 | Genre selections | Mann-Whitney U | 2.39 | 2.57 | 0.8457 | Not significant |

Significance level: α = 0.05

---

## Effect Size

| Metric | Cohen's d | Magnitude |
|---|---|---|
| Time on page (B vs A) | 0.461 | Small |

---

## Key Findings

**Time on page** was the only metric that showed a statistically significant difference (p = 0.0443). Version B (cinematic dark theme) kept users engaged for longer — a median of 50.0s vs 47.2s for Version A, with a mean difference of ~32 seconds (47.0s vs 79.6s).

Both versions achieved 100% quiz completion and 100% final pick rates, meaning the design difference did not affect whether users finished — but it did affect how long they spent engaging with the experience.

The effect size for time on page was small (Cohen's d = 0.461), suggesting a real but modest practical difference.

---

## Plots

See in `analysis/plots/`:

- `time_boxplot.png` — time on page distribution by group
- `genre_violin.png` — genre selections by group  
- `completion_bar.png` — quiz completion rates by group