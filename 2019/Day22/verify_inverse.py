
import sys

def verify():
    # Constants for Part 1 verification
    D = 10007
    K = 1
    TARGET_POS = 1538 # This is the result from part1.py
    EXPECTED_CARD = 2019
    
    # Read input
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    
    # Inverse logic as in solution_part2.py
    a = 1
    b = 0
    
    # Process instructions in forward order
    # lines = lines[::-1] # Do not reverse!
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line == "deal into new stack":
            # Inverse: y -> -y - 1
            # x = a(-y - 1) + b = -ay - a + b
            b = b - a
            a = -a
        elif line.startswith("cut"):
            # Inverse: y -> y + N
            # x = a(y + N) + b = ay + aN + b
            try:
                n = int(line.split()[-1])
                b = b + a * n
            except ValueError:
                print(f"Error parsing line: {line}")
                sys.exit(1)
        elif line.startswith("deal with increment"):
            # Inverse: y -> y * modinv(N)
            # x = a(y * modinv(N)) + b
            try:
                n = int(line.split()[-1])
                # Modular inverse of n modulo D
                inv_n = pow(n, -1, D)
                a = a * inv_n
            except ValueError:
                print(f"Error parsing line: {line}")
                sys.exit(1)
        
        # Keep coefficients modulo D
        a %= D
        b %= D
        
    # Apply once
    A_k = pow(a, K, D)
    if a == 1:
        B_k = (b * K) % D
    else:
        B_k = (b * (A_k - 1) * pow(a - 1, -1, D)) % D
        
    # Calculate final answer
    result = (A_k * TARGET_POS + B_k) % D
    
    print(f"Calculated: {result}")
    print(f"Expected: {EXPECTED_CARD}")
    
    if result == EXPECTED_CARD:
        print("Verification SUCCESS!")
    else:
        print("Verification FAILED!")

if __name__ == "__main__":
    verify()
