questions = [
 {"question": "What is 2 + 2?", "answer": "4"},
 {"question": "Capital of Japan?", "answer": "Tokyo"},
 {"question": "How many days in a week?", "answer": "7"}
]
print("First question:", questions[0]["question"])
print("Its answer:", questions[0]["answer"])
for item in questions:
    user_answer = input(item["question"] + " ")

    if user_answer == item["answer"]:
        print("Correct!")
    else:
        print("Wrong. The answer was", item["answer"])