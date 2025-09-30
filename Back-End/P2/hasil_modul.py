from Penambahan import add, label as label_add
from Pengurangan import subtract, label as label_sub
from Perkalian import multiply, label as label_mul
from Pembagian import divide, label as label_div

def main():
    a = float(input("Enter the first number: "))
    b = float(input("Enter the second number: "))
    results = [
        (label_add(), add(a, b)),
        (label_sub(), subtract(a, b)),
        (label_mul(), multiply(a, b)),
        (label_div(), divide(a, b)),
    ]

    for lbl, val in results:
        print(f"{lbl}: {val}")

if __name__ == "__main__":
    main()