

def find_primes():
    n = 8000000
    for p in range(2, n+1):
        for i in range(2, p):
            if p % i == 0:
                break
        else:
            print(p)
    print('Done')

def pow2(n):
    print(2**n)

pow2(16)