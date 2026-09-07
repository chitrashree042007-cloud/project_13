# ==============================
# SIMPLE QUIZ PROGRAM
# ==============================

# Get player's name
player = input("Enter your name: ")

print()
print("Welcome,", player, "!")
print("Let's start the quiz.")
print()


# ==============================
# QUESTIONS AND ANSWERS
# ==============================

questions = [
    {
        "question": "What is 2 + 2?",
        "answer": "4"
    },
    {
        "question": "Capital of Japan?",
        "answer": "Tokyo"
    },
    {
        "question": "How many days in a week?",
        "answer": "7"
    }
]


# ==============================
# START QUIZ
# ==============================

score = 0

for item in questions:

    user_answer = input(item["question"] + " ")

    # Remove spaces and ignore capital letters
    user_answer = user_answer.strip().lower()

    # Check answer
    if user_answer == item["answer"].lower():
        print("Correct!")
        score = score + 1

    else:
        print("Wrong. The answer was", item["answer"])

    print()


# ==============================
# QUIZ RESULT
# ==============================

print("==============================")
print("QUIZ OVER!")
print("==============================")

print("Player:", player)
print("Your score was:", score, "out of", len(questions))
print()


# ==============================
# FEEDBACK
# ==============================

if score == len(questions):
    print("Perfect score! Amazing!")

elif score >= len(questions) / 2:
    print("Good job!")

else:
    print("Keep practising — you will get there!")


# ==============================
# SAVE SCORE TO FILE
# ==============================

with open("scores.txt", "a") as file:
    file.write(player + " scored " + str(score) + " out of " + str(len(questions)) + "\n")

print()
print("Your score was saved!")
quiz_bank = {
 "Maths": [
 {"question": "2 + 2?", "answer": "4"},
 {"question": "10 - 3?", "answer": "7"}
 ],
 "Geography": [
 {"question": "Capital of Japan?", "answer": "Tokyo"}
 ]
}
print("Categories available:")
for name in quiz_bank:
 print("-", name)
