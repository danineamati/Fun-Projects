# Daniel Neamati
# 6 July 2019

import matplotlib.pyplot as plt
import matplotlib.animation as anim

filename = 'data.txt'
fig = plt.figure()
ax = fig.add_subplot(111)

# The way that the animation function works, we 
# need to pass it a function
def animate(frame):
	# We need to read the data from file
	all_data = open(filename, 'r').read()
	data_array = all_data.split('\n')

	# Check the data and convert the data to floats
	num_data_array = []
	for data in data_array:
		try: 
			num_data_array.append(float(data))
		except ValueError:
			continue

	ax.clear()
	plt.plot(range(len(num_data_array)), num_data_array)

# Now we can make the plot and call this function

ani = anim.FuncAnimation(fig, animate, interval = 1000)
plt.show()