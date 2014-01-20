l = [1,2,3]
def square(x):
    return (x**2, x)
for x, x1 in [square(y) for y in l]:
    print str(x) + "--" + str(x1)
    
