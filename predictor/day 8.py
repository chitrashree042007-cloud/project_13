def predict(x, m, c):
 return m * x + c
real = 62
guess = predict(3, 6, 46) # predict 3 hours
error = guess - real
print("Guess:", guess, "Real:", real, "Error:", error)
errors = [2, -3, 5, -1]
print("Just added (misleading):", sum(errors))
squared = [e*e for e in errors]
print("Squared (honest):", squared)
print("Sum of squared:", sum(squared))