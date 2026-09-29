
from functions.run_python_file import run_python_file

def test() -> None:
    result = run_python_file("calculator", "main.py")
    print("(Should print the calculator's usage instructions")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Should run the calculator")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Should run the calculator's tests successfully")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Should return an error")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("Should return an error")
    print(result)

    result = run_python_file("calculator", "lorem.txt")
    print("Should return an error")
    print(result)


if __name__ == "__main__":
    test()
