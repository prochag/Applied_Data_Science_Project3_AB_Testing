# ============================================================
# app/movies.py — Shared movie dataset and recommendation logic
# Used by both version_a and version_b
# ============================================================

MOVIES = [
    # Action
    {"title": "Mad Max: Fury Road",     "genre": ["Action"],            "mood": ["Excited", "Adventurous"], "year": 2015, "rating": 8.1, "length": "short",  "era": "modern",  "emoji": "🚗"},
    {"title": "John Wick",              "genre": ["Action", "Thriller"], "mood": ["Excited", "Tense"],       "year": 2014, "rating": 7.4, "length": "short",  "era": "modern",  "emoji": "🔫"},
    {"title": "The Dark Knight",        "genre": ["Action", "Drama"],    "mood": ["Tense", "Thoughtful"],    "year": 2008, "rating": 9.0, "length": "long",   "era": "modern",  "emoji": "🦇"},
    {"title": "Die Hard",               "genre": ["Action"],             "mood": ["Excited", "Fun"],         "year": 1988, "rating": 8.2, "length": "medium", "era": "classic", "emoji": "🏢"},
    # Comedy
    {"title": "The Grand Budapest Hotel","genre": ["Comedy", "Drama"],   "mood": ["Fun", "Relaxed"],         "year": 2014, "rating": 8.1, "length": "medium", "era": "modern",  "emoji": "🏨"},
    {"title": "Superbad",               "genre": ["Comedy"],             "mood": ["Fun", "Relaxed"],         "year": 2007, "rating": 7.6, "length": "medium", "era": "modern",  "emoji": "😂"},
    {"title": "Knives Out",             "genre": ["Comedy", "Thriller"], "mood": ["Fun", "Tense"],           "year": 2019, "rating": 7.9, "length": "medium", "era": "modern",  "emoji": "🔪"},
    {"title": "Groundhog Day",          "genre": ["Comedy"],             "mood": ["Fun", "Relaxed"],         "year": 1993, "rating": 8.0, "length": "short",  "era": "classic", "emoji": "🌤️"},
    # Drama
    {"title": "The Shawshank Redemption","genre": ["Drama"],             "mood": ["Thoughtful", "Emotional"],"year": 1994, "rating": 9.3, "length": "long",   "era": "classic", "emoji": "🏛️"},
    {"title": "Parasite",               "genre": ["Drama", "Thriller"],  "mood": ["Tense", "Thoughtful"],    "year": 2019, "rating": 8.5, "length": "long",   "era": "modern",  "emoji": "🏠"},
    {"title": "Marriage Story",         "genre": ["Drama"],              "mood": ["Emotional", "Thoughtful"],"year": 2019, "rating": 7.9, "length": "long",   "era": "modern",  "emoji": "💔"},
    {"title": "Forrest Gump",           "genre": ["Drama"],              "mood": ["Emotional", "Relaxed"],   "year": 1994, "rating": 8.8, "length": "long",   "era": "classic", "emoji": "🏃"},
    # Sci-Fi
    {"title": "Interstellar",           "genre": ["Sci-Fi", "Drama"],    "mood": ["Thoughtful", "Adventurous"],"year": 2014,"rating": 8.6,"length": "long",   "era": "modern",  "emoji": "🚀"},
    {"title": "The Matrix",             "genre": ["Sci-Fi", "Action"],   "mood": ["Excited", "Thoughtful"],  "year": 1999, "rating": 8.7, "length": "medium", "era": "classic", "emoji": "💊"},
    {"title": "Arrival",                "genre": ["Sci-Fi", "Drama"],    "mood": ["Thoughtful", "Tense"],    "year": 2016, "rating": 7.9, "length": "medium", "era": "modern",  "emoji": "🛸"},
    {"title": "Blade Runner 2049",      "genre": ["Sci-Fi"],             "mood": ["Thoughtful", "Adventurous"],"year": 2017,"rating": 8.0,"length": "long",   "era": "modern",  "emoji": "🤖"},
    # Horror
    {"title": "Get Out",                "genre": ["Horror", "Thriller"], "mood": ["Tense"],                  "year": 2017, "rating": 7.7, "length": "medium", "era": "modern",  "emoji": "😱"},
    {"title": "Hereditary",             "genre": ["Horror"],             "mood": ["Tense"],                  "year": 2018, "rating": 7.3, "length": "long",   "era": "modern",  "emoji": "👁️"},
    {"title": "The Shining",            "genre": ["Horror"],             "mood": ["Tense"],                  "year": 1980, "rating": 8.4, "length": "long",   "era": "classic", "emoji": "🪓"},
    # Romance
    {"title": "Before Sunrise",         "genre": ["Romance", "Drama"],   "mood": ["Romantic", "Relaxed"],    "year": 1995, "rating": 8.1, "length": "short",  "era": "classic", "emoji": "🌅"},
    {"title": "La La Land",             "genre": ["Romance", "Drama"],   "mood": ["Romantic", "Emotional"],  "year": 2016, "rating": 8.0, "length": "medium", "era": "modern",  "emoji": "🎭"},
    {"title": "Eternal Sunshine",       "genre": ["Romance", "Sci-Fi"],  "mood": ["Romantic", "Thoughtful"], "year": 2004, "rating": 8.3, "length": "medium", "era": "modern",  "emoji": "☀️"},
    # Documentary
    {"title": "Free Solo",              "genre": ["Documentary"],        "mood": ["Adventurous", "Excited"], "year": 2018, "rating": 8.2, "length": "medium", "era": "modern",  "emoji": "🧗"},
    {"title": "Won't You Be My Neighbor","genre": ["Documentary"],       "mood": ["Emotional", "Relaxed"],   "year": 2018, "rating": 8.4, "length": "short",  "era": "modern",  "emoji": "🧸"},
    # Thriller
    {"title": "Gone Girl",              "genre": ["Thriller", "Drama"],  "mood": ["Tense", "Thoughtful"],    "year": 2014, "rating": 8.1, "length": "long",   "era": "modern",  "emoji": "🕵️"},
    {"title": "Prisoners",              "genre": ["Thriller", "Drama"],  "mood": ["Tense"],                  "year": 2013, "rating": 8.1, "length": "long",   "era": "modern",  "emoji": "🔒"},
]

MOODS = ["Excited", "Relaxed", "Adventurous", "Tense", "Thoughtful",
         "Emotional", "Fun", "Romantic"]

GENRES = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror",
          "Romance", "Thriller", "Documentary"]

LENGTH_LABELS = {"short": "Under 100 min", "medium": "100–130 min", "long": "Over 130 min"}
ERA_LABELS    = {"classic": "Classic (pre-2000)", "modern": "Modern (2000+)", "any": "Any era"}


def recommend(mood: str, genres: list, length: str, era: str, min_rating: float) -> list:
    """Score and rank movies based on user preferences. Returns top 5."""
    results = []
    for m in MOVIES:
        score = 0
        if mood in m["mood"]:         score += 3
        if any(g in m["genre"] for g in genres): score += 2
        if length == "any" or m["length"] == length: score += 1
        if era == "any" or m["era"] == era:          score += 1
        if m["rating"] >= min_rating:                score += 1
        if score > 0:
            results.append({**m, "score": score})
    results.sort(key=lambda x: (-x["score"], -x["rating"]))
    return results[:5]