#I do not know how to use this libary
#Shows the number of comparisons to the grid size
import matplotlib.pyplot as plt
import numpy as np

grid_size = []
threeD_num_of_comparisons = []
twoD_num_of_comparisons = []

twoD_num_of_comparisons = np.array([((2*x)+(2*x)) for x in range(2, 30)])
grid_size = np.array([x for x in range(2, 30)])
threeD_num_of_comparisons = np.array([(4*(x*x)) for x in range(2, 30)])

#Prints line assuming grid is square
plt.plot(grid_size, threeD_num_of_comparisons)#Exponential
plt.plot(grid_size, twoD_num_of_comparisons)#Linear
plt.show()
#twoD may be seen as a straight line due to the size of threed