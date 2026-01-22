def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_pattern(limit):
    print("Table")
    for i in range(1, limit + 1):
        if is_prime(i):
            color = "Red"
        else:
            color = "Green"
        
        print(f"{i}. {color}")

generate_pattern(20)