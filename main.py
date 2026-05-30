from pathlib import Path

inp = Path("data/inbox")
out = Path("output")


def main():
    print("Распределение писем по папкам началось")
    print("Входящие письма:", inp)
    print("Исходящие письма:", out)

if __name__ == "__main__":
    main()