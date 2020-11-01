# python program to create colourful, rotating arcs
'''
 multiple stacked semi-circular slices whose rotation
 speeds/frequencies are equal to their radii
 Inspiration : https://twitter.com/InertialObservr/status/1239655491849957381
'''

## numpy for array operations
import numpy as np
## for plotting operations
import matplotlib.pyplot as plt
## colormap to use different colors for each arc
import matplotlib.cm as cm
## for some math operations
import math
## for viewing and saving animation
import matplotlib.animation as animation
## for drawing multiple arcs together
from matplotlib.collections import LineCollection



## initialise required variables
## number of frames
n_frames = 360
## number of arcs
n_arcs = 36
## min and max radius
r_min = 1
r_max = n_arcs
## adjusted width of the line
line_width = 4
## create the array of radii
radius_arr = np.linspace(r_min,r_max,n_arcs)
## initialize the angular velocities, normalize to the minimum radius and adjust to the number of frames
omega_arr = radius_arr/r_min * (2*np.pi/(n_frames-1))
## omega_arr = np.ones_like(radius_arr) * (2*np.pi/(n_frames-1))


## declare the figure and artist
fig= plt.figure()
## prepare the polar coordinates
ax1 = fig.add_subplot(111, projection='polar')
## hide background components
ax1.patch.set_visible(False)
## initialise the plot
arcplot = ax1.plot([], [],)[0]


def init():
    '''
    method to initialise the plotting window
    '''
    ## set maximum radius
    ax1.set_rmax(r_max+1)
    ## remove the grids and ticks
    ax1.grid(False)
    ax1.set_rticks([])
    ax1.set_xticks([])
    ## remove the axis
    ax1.axis('off')

    return arcplot,


def update(frame, radius_arr, omega_arr):
    ## choose a different colour for each radius
    colors = cm.rainbow(np.linspace(0, 1, len(radius_arr)))

    ## initialise the list that will contain the plotting data as [[arc1],[arc2],...] 
    plot_list = []
    ## resolution of the arc, use the same number of points for all arcs for now
    arc_points = 50
    ## datapoints for angles of each arc
    angles = np.linspace(0, np.pi, arc_points)
    ## loop over the arcs with different radii
    for i in range(len(radius_arr)):
        ## radius and angular velocity of the arc
        r = radius_arr[i]
        angular_vel = omega_arr[i]

        ## rotate the arcs by angular speed
        rotated_angles = angles + angular_vel*frame
        ## prepare the required radius array for plotting
        radii = np.zeros_like(rotated_angles)+r
        ## Append proper numpy arrays to the list of plotting data
        plot_list.append(np.column_stack([rotated_angles,radii]))
    
    ## prepare the collection of lines to be plotted
    lines = LineCollection(plot_list, linewidth=line_width,
                                       colors=colors, linestyle='solid')
    ## clean the previous drawing                                   
    ax1.collections = []
    ## add the collection of the lines to the clean window
    arcplot = ax1.add_collection(lines)

    ## return the animation iterable
    return arcplot,

## create the animation
ani = animation.FuncAnimation(fig, update, frames=n_frames, fargs=(radius_arr,omega_arr), init_func=init, blit=True, repeat=False)

# set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, metadata=dict(artist='pjoshi'), bitrate=1800)

# ## save the animation instead of viewing
# ani.save(r"E:\bitbucket\python_fun_projects\arcs_rotation.mp4", writer=writer)
plt.show()


'''
def update(frame, radius_arr, omega_arr):
    ## choose a different colour for each radius
    colors = cm.rainbow(np.linspace(0, 1, len(radius_arr)))
    angles_set = np.array([])
    radius_set = np.array([])
    ## resolution of the arc
    arc_points = 50
    ## angle datapoints
    angles = np.linspace(0, np.pi, arc_points)
    for i in range(len(radius_arr)):
        r = radius_arr[i]
        angular_vel = omega_arr[i]
        ## ## resolution of the arc
        ## arc_points = 50*math.ceil(r)
        ## rotate the arcs by angular speed = arc radius
        rotated_angles = angles + angular_vel*frame
        ## prepare the required radius array for plotting
        radii = np.zeros_like(rotated_angles)+r
        ## Append numpy arrays with care
        if i==0:
            angles_set = rotated_angles
            radius_set = radii
        elif i==1:
            angles_set = np.append([angles_set], [rotated_angles], axis=0)
            radius_set = np.append([radius_set], [radii], axis=0)
        else:
            angles_set = np.append(angles_set,[rotated_angles], axis=0)
            radius_set = np.append(radius_set,[radii], axis=0)

    arcplot = ax1.plot(angles_set.T, radius_set.T, '-', linewidth=5)
    ## arcplot.set_data(plot_set)
    return arcplot
'''
