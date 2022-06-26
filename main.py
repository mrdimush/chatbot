import random

text = input()
if text in ['Hi', "hello"]:
    print(random.choice(["hello", "heyo"]))
elif text in ["buy", "poki"]:
    print(random.choice(["wait for our cita", "bao"]))
else:
    print("did not get it")

