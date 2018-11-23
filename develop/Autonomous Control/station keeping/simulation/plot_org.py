import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import time
import math
import threading
from sailboat_org import sailboat
import random



start_time=time.time()
my_boat=sailboat()
x=my_boat.location[0]
y=my_boat.location[1]
heading_angle=my_boat.heading_angle
desired_angle=my_boat.desired_angle
rudder=my_boat.rudder
sail=my_boat.sail
v=0




fig = plt.figure()
gs1 = gridspec.GridSpec(1, 1)
gs2 = gridspec.GridSpec(3, 1)

ax=fig.add_subplot(gs1[0])

theta = np.linspace(0, 2*np.pi,100)
x_t,y_t = np.cos(theta)*5+np.linspace(10,10,100), np.sin(theta)*5+np.linspace(30,30,100)
ax.plot(x_t, y_t, color='red', linewidth=1.0)
theta = np.linspace(0, 2*np.pi,100)
x_p,y_p = np.cos(theta)*10+np.linspace(10,10,100), np.sin(theta)*10+np.linspace(30,30,100)
ax.plot(x_p, y_p, color='orange', linewidth=1.0)

plt.xlim(-3,30)
plt.ylim(-5,50)
gs1.tight_layout(fig, rect=[0, 0, 0.6, 1])

ax1 = fig.add_subplot(gs2[0])
plt.xlabel('v')
plt.ylim(-0.1,5)
ax2 = fig.add_subplot(gs2[1])
plt.xlabel('u')
plt.ylim(-0.2,0.2)
ax3 = fig.add_subplot(gs2[2])
plt.xlabel('w')
plt.ylim(-1,1)
gs2.tight_layout(fig, rect=[0.6, 0, 1, 1], h_pad=0.5)


top = min(gs1.top, gs2.top)
bottom = max(gs1.bottom, gs2.bottom)

gs1.update(top=top, bottom=bottom)
gs2.update(top=top, bottom=bottom)

x_data = np.zeros(5000)
y_data=np.zeros(5000)
line, = ax.plot(x_data,y_data)
x1_data = np.linspace(0, 5, 500)
y_data1=np.zeros(500)
line1, = ax1.plot(x1_data, y_data1)
# x2_data = np.linspace(0, 5, 500)
y2_data=np.zeros(500)
line2, = ax2.plot(x1_data, y2_data)
# x3_data = np.linspace(0, 5, 500)
y3_data=np.zeros(500)
line3, = ax3.plot(x1_data, y3_data)
boat_y_data=np.array([y-math.sin(heading_angle)-math.cos(heading_angle)*0.5,
                    y+math.sin(heading_angle)-math.cos(heading_angle)*0.5,
                    y+1.5*math.sin(heading_angle),
                    y+math.sin(heading_angle)+math.cos(heading_angle)*0.5,
                    y-math.sin(heading_angle)+math.cos(heading_angle)*0.5,])
boat_x_data=np.array([x-math.cos(heading_angle)+math.sin(heading_angle)*0.5,
                    x+math.cos(heading_angle)+math.sin(heading_angle)*0.5,
                    x-1.5*math.cos(heading_angle),
                    x+math.cos(heading_angle)-math.sin(heading_angle)*0.5,
                    x-math.cos(heading_angle)-math.sin(heading_angle)*0.5])
line_boat, = ax.plot(boat_x_data,boat_y_data)

rudder_y_data=np.array([y-math.sin(heading_angle),
                        y-math.sin(heading_angle)-math.cos(rudder-math.pi/2+heading_angle)])
rudder_x_data=np.array([x-math.cos(heading_angle),
                        x-math.cos(heading_angle)+math.sin(rudder-math.pi/2+heading_angle)])
line_rudder,=ax.plot(rudder_x_data,rudder_y_data)

sail_y_data=np.array([y+0.8*math.sin(heading_angle),
                        y+0.8*math.sin(heading_angle)-2*math.cos(sail-math.pi/2+heading_angle)])
sail_x_data=np.array([x+0.8*math.cos(heading_angle),
                        x+0.8*math.cos(heading_angle)+2*math.sin(sail-math.pi/2+heading_angle)])
line_sail,=ax.plot(sail_x_data,sail_y_data)

def init1():  # only required for blitting to give a clean slate.
    x_data = np.zeros(5000)
    y_data=np.zeros(5000)
    line.set_data(x_data,y_data)
    y_data1=np.zeros(500)
    line1.set_ydata(y_data1)
    # x2_data = np.linspace(0, 5, 500)
    y2_data=np.zeros(500)
    line2.set_ydata(y2_data)
    y3_data=np.zeros(500)
    line3.set_ydata(y3_data)
    boat_y_data=np.array([y-math.sin(heading_angle)-math.cos(heading_angle)*0.5,
                    y+math.sin(heading_angle)-math.cos(heading_angle)*0.5,
                    y+1.5*math.sin(heading_angle),
                    y+math.sin(heading_angle)+math.cos(heading_angle)*0.5,
                    y-math.sin(heading_angle)+math.cos(heading_angle)*0.5,])
    boat_x_data=np.array([x-math.cos(heading_angle)+math.sin(heading_angle)*0.5,
                    x+math.cos(heading_angle)+math.sin(heading_angle)*0.5,
                    x-1.5*math.cos(heading_angle),
                    x+math.cos(heading_angle)-math.sin(heading_angle)*0.5,
                    x-math.cos(heading_angle)-math.sin(heading_angle)*0.5])
    line_boat.set_data(boat_x_data,boat_y_data)
    rudder_y_data=np.array([y-math.sin(heading_angle),
                            y-math.sin(heading_angle)-math.cos(sail-math.pi/2+heading_angle)])
    rudder_x_data=np.array([x-math.cos(heading_angle),
                            x-math.cos(heading_angle)+math.sin(sail-math.pi/2+heading_angle)])
    line_rudder.set_data(rudder_x_data,rudder_y_data)
    sail_y_data=np.array([y+0.8*math.sin(heading_angle),
                        y+0.8*math.sin(heading_angle)-2*math.cos(sail-math.pi/2+heading_angle)])
    sail_x_data=np.array([x+0.8*math.cos(heading_angle),
                            x+0.8*math.cos(heading_angle)+2*math.sin(sail-math.pi/2+heading_angle)])
    line_sail.set_data(sail_x_data,sail_y_data)
    return line,line1,line2,line3,line_boat,line_rudder,line_sail,


def animate1(i):
    global y_data1,x1_data,x_data,y_data,y2_data,y3_data,x,y,heading_angle,desired_angle
    global boat_x_data,boat_y_data
    # ,rudder_x_data,rudder_y_data
    info=my_boat.to_next_moment()
    info=my_boat.to_next_moment()
    info=my_boat.to_next_moment()
    info=my_boat.to_next_moment()
    x=info[0][0]
    y=info[0][1]
    rudder=info[1]
    sail=info[2]
    
    desired_angle=info[3]
    heading_angle=info[4]
    w=my_boat.angular_velocity
    v=my_boat.velocity[0]
    u=my_boat.velocity[1]

    x_data=np.delete(x_data,0,0)
    x_data=np.append(x_data,[x],0)
    y_data=np.delete(y_data,0,0)
    y_data=np.append(y_data,[y],0)
    line.set_data(x_data,y_data)

    y_data1=np.delete(y_data1,0,0)
    y_data1=np.append(y_data1,[v],0)
    line1.set_ydata(y_data1)  # update the data.

    
    y2_data=np.delete(y2_data,0,0)
    y2_data=np.append(y2_data,[u],0)
    line2.set_ydata(y2_data)  # update the data.
    y3_data=np.delete(y3_data,0,0)
    y3_data=np.append(y3_data,[w],0)
    line3.set_ydata(y3_data)
    boat_y_data=np.array([y-math.sin(heading_angle)-math.cos(heading_angle)*0.5,
                    y+math.sin(heading_angle)-math.cos(heading_angle)*0.5,
                    y+1.5*math.sin(heading_angle),
                    y+math.sin(heading_angle)+math.cos(heading_angle)*0.5,
                    y-math.sin(heading_angle)+math.cos(heading_angle)*0.5,])
    boat_x_data=np.array([x-math.cos(heading_angle)+math.sin(heading_angle)*0.5,
                        x+math.cos(heading_angle)+math.sin(heading_angle)*0.5,
                        x+1.5*math.cos(heading_angle),
                        x+math.cos(heading_angle)-math.sin(heading_angle)*0.5,
                        x-math.cos(heading_angle)-math.sin(heading_angle)*0.5])
    line_boat, = ax.plot(boat_x_data,boat_y_data,color='black')
    
    rudder_y_data=np.array([y-math.sin(heading_angle),
                            y-math.sin(heading_angle)-math.cos(rudder-math.pi/2+heading_angle)])
    rudder_x_data=np.array([x-math.cos(heading_angle),
                            x-math.cos(heading_angle)+math.sin(rudder-math.pi/2+heading_angle)])
    line_rudder, =ax.plot(rudder_x_data,rudder_y_data,color='r')
    sail_y_data=np.array([y+0.8*math.sin(heading_angle),
                        y+0.8*math.sin(heading_angle)-2*math.cos(sail-math.pi/2+heading_angle)])
    sail_x_data=np.array([x+0.8*math.cos(heading_angle),
                            x+0.8*math.cos(heading_angle)+2*math.sin(sail-math.pi/2+heading_angle)])
    line_sail,=ax.plot(sail_x_data,sail_y_data,color='r')
    return line,line1,line2,line3,line_boat,line_rudder,line_sail,









# def init_boat():  # only required for blitting to give a clean slate.
    
#     return line_boat,

# def animate_boat(i):
#     global boat_y_data,boat_x_data,x,y
    
def plot():
    ani = animation.FuncAnimation(
        fig, animate1, init_func=init1, interval=5, blit=True, save_count=50)
    # ani_boat = animation.FuncAnimation(
    #     fig, animate_boat, init_func=init_boat, interval=5, blit=True, save_count=50)
    # To save the animation, use e.g.
    #
    # ani.save("movie.mp4")
    #
    # or
    #
    # from matplotlib.animation import FFMpegWriter
    # writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    # ani.save("movie.mp4", writer=writer)

    plt.show()
plot()
