import math

a = float(input())
b = float(input())
c = float(input())

if abs(a) <= 0:
    if abs(b) <= 0:
        if abs(c) <= 0:
            print(3)
        else:
            print(0)
    else:
        x = -c / b
        print(1, x)
else:
    discriminant = (b**2) - (4 * a * c)
    if discriminant > 0:
        sqrt_d = math.sqrt(discriminant)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        roots = sorted([x1, x2])
        print(2, roots[0], roots[1])
    elif discriminant < 0:
        print(0)
    else:
        print(1, -1 * (b / (2 * a)))