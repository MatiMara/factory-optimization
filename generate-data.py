import numpy as np

# xy = 10
height = 3
width = 12
n = height * width
n_sectors = 4

minX, maxX, minY, maxY = 8, 8*width, 8, 8*height

x = np.linspace(minX, maxX, width, dtype=int)
y = np.linspace(minY, maxY, height, dtype=int)

X, Y = np.meshgrid(x, y)

X = X.reshape((np.prod(X.shape),))
Y = Y.reshape((np.prod(Y.shape),))

print(X, Y)

with open("data6.txt", "w") as f:
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

