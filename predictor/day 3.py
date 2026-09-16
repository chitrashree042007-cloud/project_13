import matplotlib.pyplot as plt
hours = [1, 2, 3, 4, 5]
scores = [52, 58, 62, 71, 78]
m, c = 6, 46
plt.scatter(hours, scores) # real data as dots
line_y = [m*x + c for x in hours]
plt.plot(hours, line_y, color="red") # your line
plt.xlabel("Hours"); plt.ylabel("Score")
plt.show()
