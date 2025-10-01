import sys

AMOUNT_TO_READ = 80


def operate():
    if len(sys.argv) != 2:
        print("Only One Parameter Is Allowed.")
        return

    with open(sys.argv[1], "rb") as file:
        while True:
            lst = []
            try:
                bytes_st = file.read(AMOUNT_TO_READ)
                if bytes_st == b"":
                    break
                for i in range(0, AMOUNT_TO_READ // 2, 2):
                    item = bytes_st[i:i + 1]
                    lst.append(item.hex())
                print("\t".join(lst), end="\t\t")

                char_lst = ['' if item == '' else chr(int(item, 16)) if 32 <= int(item, 16) <= 126 else '.'
                            for item in lst]
                print(''.join(char_lst))
            except Exception as e:
                print(f"An Error Occurred. {e}")
                break

if __name__ == "__main__":
    operate()
