m = 6 # slope: score goes up ~6 per hour (a guess)
c = 46 # intercept: score at 0 hours (a guess)
def predict(x):
 return m * x + c
print("Predict 3 hours:", predict(3))
print("Predict 5 hours:", predict(5))
