def get_palindrome(word: str) -> bool:
    cleaned = word.replace(" ","").lower()

    return cleaned == cleaned[::-1]

def second_largest(num: list) -> int:
    #unique values
    unique_values = list(set(num))

    unique_values.sort()

    if len(unique_values) < 2:
        return None
    else:
        return unique_values[-1]

def sum_file_numbers(filename: str) -> int:
    total = 0
    try:
        with open (filename, "r") as f:
            for line in f:
                total += int(line.strip())
    except FileNotFoundError:
        print("Error:file not found")
        return None
    except ValueError:
        print("Non numeric value")
        return None
    return total



def main():
    print(get_palindrome("madam"))
    print(second_largest([1,4,8,7]))
    print(sum_file_numbers("C:\\Users\CapwellTheNerd\\Desktop\\Interview_prep_11th_sep\\Python_Solutions\\data.txt"))


if __name__ == "__main__":
    main()