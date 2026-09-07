import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


# ============================================================
# SIMILARITY FUNCTION
# ============================================================

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0

    return np.dot(a, b) / denominator


# ============================================================
# MOVIE LIBRARY
# ============================================================

movies = [
    {
        "title": "Inception",
        "ratings": [5, 5, 4, 5]
    },
    {
        "title": "Interstellar",
        "ratings": [5, 5, 5, 4]
    },
    {
        "title": "Titanic",
        "ratings": [4, 5, 4, 5]
    },
    {
        "title": "The Dark Knight",
        "ratings": [5, 5, 5, 5]
    },
    {
        "title": "Avatar",
        "ratings": [4, 5, 4, 4]
    },
    {
        "title": "3 Idiots",
        "ratings": [5, 5, 5, 5]
    }
]


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def recommend(chosen, how_many=3):

    scores = []

    chosen_movie = None

    # Find the selected movie
    for movie in movies:
        if movie["title"] == chosen:
            chosen_movie = movie
            break

    # Movie not found
    if chosen_movie is None:
        return []

    # Compare selected movie with every other movie
    for movie in movies:

        title = movie["title"]

        # Do not recommend the movie itself
        if title == chosen:
            continue

        score = cosine_similarity(
            chosen_movie["ratings"],
            movie["ratings"]
        )

        scores.append((title, score))

    # Sort from highest similarity to lowest
    scores.sort(
        key=lambda pair: pair[1],
        reverse=True
    )

    return scores[:how_many]


# ============================================================
# DISPLAY RECOMMENDATIONS
# ============================================================

def show_recommendations():

    chosen = movie_combo.get()

    if chosen == "":
        messagebox.showwarning(
            "No Movie Selected",
            "Please select a movie first."
        )
        return

    # Clear old recommendations
    result_text.delete("1.0", tk.END)

    result_text.insert(
        tk.END,
        "🎬 Because you liked " + chosen + ",\n"
    )

    result_text.insert(
        tk.END,
        "you might enjoy:\n\n"
    )

    recommendations = recommend(chosen, 3)

    for title, score in recommendations:

        result_text.insert(
            tk.END,
            "⭐ " + title + "\n"
        )

        result_text.insert(
            tk.END,
            "   Similarity: " + str(round(score, 4)) + "\n\n"
        )


# ============================================================
# CLEAR BUTTON
# ============================================================

def clear_results():

    movie_combo.set("")

    result_text.delete(
        "1.0",
        tk.END
    )


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title("🎬 Movie Recommendation System")

window.geometry("650x550")

window.resizable(False, False)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    window,
    text="🎬 Movie Recommendation System",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=20)


# ============================================================
# DESCRIPTION
# ============================================================

description = tk.Label(
    window,
    text="Select a movie you like and get similar movie recommendations.",
    font=("Arial", 11)
)

description.pack(pady=5)


# ============================================================
# MOVIE SELECTION
# ============================================================

select_label = tk.Label(
    window,
    text="Choose a movie:",
    font=("Arial", 13, "bold")
)

select_label.pack(pady=(25, 8))


movie_combo = ttk.Combobox(
    window,
    values=[movie["title"] for movie in movies],
    state="readonly",
    width=35,
    font=("Arial", 12)
)

movie_combo.pack(pady=5)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(window)

button_frame.pack(pady=20)


# Recommend button
recommend_button = tk.Button(
    button_frame,
    text="🎯 Recommend Movies",
    command=show_recommendations,
    font=("Arial", 12, "bold"),
    padx=15,
    pady=8
)

recommend_button.grid(
    row=0,
    column=0,
    padx=10
)


# Clear button
clear_button = tk.Button(
    button_frame,
    text="🔄 Clear",
    command=clear_results,
    font=("Arial", 12),
    padx=20,
    pady=8
)

clear_button.grid(
    row=0,
    column=1,
    padx=10
)


# ============================================================
# RESULT LABEL
# ============================================================

result_label = tk.Label(
    window,
    text="Recommendations",
    font=("Arial", 15, "bold")
)

result_label.pack(pady=(10, 5))


# ============================================================
# RESULT BOX
# ============================================================

result_text = tk.Text(
    window,
    height=13,
    width=65,
    font=("Arial", 12),
    wrap=tk.WORD
)

result_text.pack(
    padx=20,
    pady=10
)


# ============================================================
# MOVIES WE KNOW
# ============================================================

known_movies = tk.Label(
    window,
    text="Movies I know: "
         + ", ".join(movie["title"] for movie in movies),
    font=("Arial", 9),
    wraplength=600
)

known_movies.pack(
    side=tk.BOTTOM,
    pady=10
)


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()