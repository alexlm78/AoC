
import sys

def solve():
    # Constants
    D = 119315717514047
    K = 101741582076661
    TARGET_POS = 2020
    
    # Read input
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    
    # We process instructions in reverse order to build the inverse function
    # The function maps final_position -> initial_position (card number)
    # x = a * y + b (mod D)
    # Initially identity: x = 1 * y + 0
    
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
        
    # Now we have the linear function for ONE reverse shuffle: f(y) = (a*y + b) % D
    # We need to apply this K times.
    # f^K(y) = A_K * y + B_K
    # A_K = a^K % D
    # B_K = b * (a^K - 1) * modinv(a - 1) % D  (geometric series sum)
    
    A_k = pow(a, K, D)
    
    if a == 1:
        B_k = (b * K) % D
    else:
        # B_k = b * (a^K - 1) / (a - 1)
        numerator = b * (A_k - 1)
        denominator = a - 1
        B_k = (numerator * pow(denominator, -1, D)) % D
        
    # Calculate final answer for position 2020
    # x = A_k * 2020 + B_k
    result = (A_k * TARGET_POS + B_k) % D
    
    print(result)

if __name__ == "__main__":
    solve()
