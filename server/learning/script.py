from matplotlib import pyplot as plt

x = [1, 2, 250]
y = [4, 5, 60]
z = [0.2, 8, 1.8]

fig = plt.figure(figsize=(15,15))
ax = plt.axes(projection = '3d')

ax.scatter3D(x, y, z, c='b', marker='o', s=100)
plt.title("Revenue vs Energy and Capacity ratings", fontweight='bold')


ax.set_xlabel('Energy (MWh)', labelpad = 20)
ax.set_ylabel('Capacity-Power (MW)', labelpad = 20)
ax.set_zlabel('Total reveune from ES ($)', labelpad = 20)

plt.rc('font',size = 40)
plt.rc('axes',titlesize = 45)

ax.text(0, 0, 0, s="test text")
ax.view_init(azim=40, elev=15)

plt.show()