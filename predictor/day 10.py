hours = [1, 2, 3, 4, 5]
scores = [52, 58, 62, 71, 78]


def loss(m, c):
    total = 0

    for x, real in zip(hours, scores):
        guess = m * x + c
        total = total + (guess - real) ** 2

    return total / len(hours)


print("Loss for m=6, c=46:", loss(6, 46))
print("Loss for m=2, c=50:", loss(2, 50))