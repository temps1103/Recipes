number = "1"

if not number:
    print("not valid")

if number:
    if not int(number) >= 1:
        print("not valid")

print("valid")