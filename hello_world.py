def mod_func(a,b):
  return a%b

def addition_func(a,b):
  return a+b

def mult_func(a,b):
  c=a*b
  return c


a=5
b=11
sum = addition_func(a,b)
mod = mod_func(b,a)
mul = mult_func(a,b)

print(sum)
print(mul)
print(mod)
