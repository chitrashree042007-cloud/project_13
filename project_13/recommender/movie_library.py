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
for movie in movies:
    print(f"{movie['title']}: {movie['ratings']}")