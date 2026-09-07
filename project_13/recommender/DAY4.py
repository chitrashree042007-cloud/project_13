import numpy as np
movies = {
 "Die Hard": np.array([9, 1, 2]),
 "Notebook": np.array([1, 9, 2]),
 "Deadpool": np.array([8, 3, 8]),
 "Toy Story": np.array([3, 4, 9]),
}
for title in movies:
 print(title, "->", movies[title])