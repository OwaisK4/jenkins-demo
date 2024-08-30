def mod_func(a,b):
  return a%b


def matrix_multiply(A, B):
    # Multiplying matrices A and B
    result = [[sum(a * b for a, b in zip(A_row, B_col)) 
                        for B_col in zip(*B)]
                                for A_row in A]
    return result

A = [[12, 7, 3],
    [4, 5, 6],
    [7, 8, 9]]

# take a 3x4 matrix
B = [[5, 8, 1, 2],
    [6, 7, 3, 0],
    [4, 5, 9, 1]]

result = matrix_multiply(A, B)

var = "hello world"

a=5
b=15
#sum = sum_func(a,b)
mod = mod_func(b,a)

for r in result:
    print(r)

print(mod)
