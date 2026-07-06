x = "There are %d five types of chicken" % 5
print(x)

y = "her name is %s and he is %d years old" % ("Aishat-Qaanitat", 15)
print(y)


# Newer way in py3
z = "There are {0} types of chicken and {1} types of ducks".format(5, "ten")
print(z)


# string concatenation
a = "Hello"
b = "World"
c = a + " " + b
print(c)

# Newerway in py3
d = f"{a} {b}"
print(d)
