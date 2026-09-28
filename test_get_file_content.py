from functions.get_file_content import get_file_content

def test() -> None:
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print("")

    result = get_file_content("calculator", "main.py")
    print("Result for 'main.py' file:")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator.py' file:")
    print(result)
    print("")

    result = get_file_content("calculator", "/bin/cat")
    print("Result for '/bin/cat' file:")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'pkg/does_not_exist.py' file:")
    print(result)
    print("")


if __name__ == "__main__":
    test()
