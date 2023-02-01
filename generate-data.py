import numpy as np

xy = 10
n = xy**2
n_sectors = 5

minX, maxX, minY, maxY = 8, 80, 8, 80

x = np.linspace(minX, maxX, xy, dtype=int)
y = np.linspace(minY, maxY, xy, dtype=int)

X, Y = np.meshgrid(x, y)

X = X.reshape((np.prod(X.shape),))
Y = Y.reshape((np.prod(Y.shape),))

print(X, Y)

with open("data2.txt", "w") as f:
    f.write("machines_x\n")
    for num in X[:-1]:
        f.write(f"{num},")
    f.write(f"{X[-1]}\n")
    f.write("machines_y\n")
    for num in Y[:-1]:
        f.write(f"{num},")
    f.write(f"{Y[-1]}\n")
    f.write("machine_names\n")
    for i in range(n - 1):
        f.write(f"{i},")
    f.write(f"{n - 1}\n")
    f.write("n_sectors\n")
    f.write(f"{n_sectors}\n")

