import numpy as np

x = np.array([[2, -1, -1],
              [1, -1, -3],
              [0, 2, -5]])
print(np.linalg.det(x))
exit()
p = np.array([[1, 2, 3],
              [2, 2, 1],
              [3, 4, 3]])

x = p.dot(p).dot(p)
print(x)
exit()

# inverse of a matrix
x = np.linalg.inv(p)
print(x)

exit()
x = np.array([[-1, 1, 1],
              [1, 0, 2],
              [1, 1, -1]])
# matrix determinant
res = np.linalg.det(x)

print(x.shape)

exit()
x = np.array([[-2, 1],
              [10, -4],
              [-10, 4]])

y = np.array([[3, -1],
              [-5, 2]])

z = np.array([[2, 1],
              [5, 3]])

res = np.dot(x, z)
res2 = np.dot(res, y)
print(res2)

print(res2.shape)
