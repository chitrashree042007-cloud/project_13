import numpy as np


def similarity(a, b):
    return np.dot(a, b)


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


def recommend(chosen, how_many=3):
    scores = []

    chosen_movie = None

    for movie in movies:
        if movie["title"] == chosen:
            chosen_movie = movie
            break

    if chosen_movie is None:
        return []

    for movie in movies:
        title = movie["title"]

        if title == chosen:
            continue

        s = similarity(
            chosen_movie["ratings"],
            movie["ratings"]
        )

        scores.append((title, s))

    scores.sort(key=lambda pair: pair[1], reverse=True)

    return scores[:how_many]


# Test
recommendations = recommend("Inception", 3)

print()
print("🎬 Recommended movies:")
print("----------------------")

for title, score in recommendations:
    print(title, "similarity:", score)
    print(recommend("Die Hard"))
    print("Movies I know:", [movie["title"] for movie in movies])

while True:
    choice = input("Tell me a movie you like (or bye): ")

    if choice == "bye":
        break

    # Check whether the movie exists
    if choice not in [movie["title"] for movie in movies]:
        print("I don't know that one. Try one from the list.")
        continue

    print("Because you liked", choice, "you might enjoy:")

    for title, score in recommend(choice):
        print(" -", title)
        import numpy as np
small = np.array([1, 1, 1])
big = np.array([10, 10, 10])
same_taste = np.array([2, 2, 2])
print("dot(small, same):", np.dot(small, same_taste))
print("dot(big, same):", np.dot(big, same_taste))
def cosine_similarity(a, b):
 return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))