#!/usr/bin/python2

#Author : Amutha Bharathi M
#This demo just changes the camera position in space and still faces front (just lateral movements)
import pi3d, time, sys, math
from random import randint


import ircam

### Initialisze IR camera

ircam.cam_init()


# DISPLAY parameters 
DISP = pi3d.Display.create()#(x = 50, y = 50)# h = 1920, w = 1080)
flatsh = pi3d.Shader('uv_flat')

ectex = pi3d.loadECfiles('skybox_hall/','skybox_hall')
#ectex = pi3d.loadECfiles('/home/pi/mycodes/python/zerolens/stripwood/','stripwood')
#ectex = pi3d.loadECfiles('/home/pi/mycodes/python/zerolens/blackwall/','blackwall')
myecube = pi3d.EnvironmentCube(size = 400.0, maptype = 'FACES')
myecube.set_draw_details(flatsh, ectex)

# Camera Settings
CAM = pi3d.Camera(eye=(0.0,10.0,-80.0))

cube_1 = pi3d.Cuboid(w=10,h=10,d=10)
cube_1.set_material((1,0,0))


############generate 5 random cubes#################
num_cubes = 5

cub = [0]*num_cubes
lin = [0]*num_cubes
for i in range(num_cubes):
	val_x = 10*randint(-15,15)
	val_y = 10*randint(-10,10)
	val_z = 10*randint(-2,10)
	val_s = randint(10,25)

	col_r = randint(0,2)
	col_g = randint(0,2)
	col_b = randint(0,2)

	cub[i] = pi3d.Cuboid(x = val_x, y = val_y, z =val_z, w=val_s, h=val_s, d=val_s)
	cub[i].set_material((col_r, col_g, col_b))
	
	lin[i] = pi3d.Lines(vertices = [(val_x,val_y,200), (val_x,val_y,val_z)],
									line_width =20)
	lin[i].set_material((col_r, col_g, col_b))
#####################################################
#	sph[i] = pi3d.Sphere(x = val_x*20, y=val_y*20, z=val_z*20, radius= 10)

mkeys = pi3d.Keyboard()
x_t = 0 
y_t = 0
z_t = -30


#IR Vars
ir_x = [0]*2
ir_y = [0]*2

temp_x = [0]*2
temp_y = [0]*2

diff_x = 0
diff_y = 0

dist_sqr = 0
ir_dist = 0
prev_ir_dist = 0

ir_mid_x = 0
ir_mid_y = 0

prev_ir_mid_x = 0
prev_ir_mid_y = 0

x_dir = 0
y_dir = 0

xm = ym = zm = 0
dist_val = [0.0,0.0, 0.0]
while DISP.loop_running():
	dist_val = [0.0,0.0, 0.0]
	crab_val = True
	CAM.reset()
	CAM.position((x_t, -y_t, z_t))
#	CAM.point_at((0,0,0))
	k = mkeys.read()
	if k == 27:
		DISP.destroy()
	
	elif k == ord('w'): 
		y_t+=5

	elif k == ord('s'):
		y_t-=5

	elif k == ord('a'):
		x_t+=5
		
	elif k == ord('d'):
		x_t-=5
	
	#camera distance
	elif k == ord('f'):
		z_t-=1
		if z_t < -30:
			z_t = -30
		else:
			dist_val = [3.5,0.0, 3.5]
			crab_val = False
	
	elif k == ord('r'):
		z_t+=1
		if z_t > 30:
			z_t = 30
		else:
			dist_val = [-3.5,0.0, -3.5]
			crab_val = False

	elif k == ord('p'): # Reset the view
		x_t = y_t =  0	
		z_t = -30
		xm = 0
		ym = 30
		zm = -60

	# Get IR position and compute the centre

	temp_x[0], temp_y[0], temp_x[1], temp_y[1] = ircam.get_pos()

	ir_x[0] = temp_x[0]
	ir_y[0] = temp_y[0]
	ir_x[1] = temp_x[1]
	ir_y[1] = temp_y[1]
	
	diff_x = ir_x[0] - ir_x[1]
	diff_y = ir_y[0] - ir_y[1]
	dist_sqr = (diff_x*diff_x) + (diff_y*diff_y) 
	
	if dist_sqr > 0:
		ir_dist = math.sqrt(dist_sqr)
	else:
		ir_dist = 0
	
	ir_mid_x = min(ir_x[0], ir_x[1]) + 0.5*ir_dist
	ir_mid_y = (ir_y[0] + ir_y[1])*0.5
		
	
	#Compute x,y,z direction movements
	x_dir = ir_mid_x - prev_ir_mid_x
	y_dir = ir_mid_y - prev_ir_mid_y	
	z_dir = ir_dist - prev_ir_dist

	
	if z_dir > 2.3:
		dist_val = [3.5,0.0, 3.5]
		crab_val = False
		z_t += 4
			
	elif z_dir < -2.3:
		dist_val = [-3.5,0.0, -3.5]
		crab_val = False
		z_t -= 4
				
	if crab_val == True: # No Z movement
		
		# Get 'X' direction
		if x_dir > 2:
			x_t += 4.8
		elif x_dir < -2:
			x_t -= 4.8
	
		# Get 'Y' direction
		if y_dir > 2:
			y_t += 4
		elif y_dir < -2:
			y_t -= 4

	else:  # There is Z movement so try to minimize X,Y movements jitter
				
		# Get 'X' direction
		if x_dir > 13:
			x_t += 1
		elif x_dir < -13:
			x_t -= 1
	
		# Get 'Y' direction
		if y_dir > 13:
			y_t += 1
		elif y_dir < -13:
			y_t -= 1

	#cam_pos = CAM.get_direction()
	if x_t > 80:
		x_t =80
	elif x_t < -80:
		x_t = -80

	if y_t > 80:
		y_t =80
	elif y_t < -80:
		y_t = -80

	if z_t > 60:
		z_t =60
	elif z_t < -60:
		z_t = -60



#	xm, ym, zm = CAM.relocate(rot = x_t, tilt = y_t,
#							  point = [xm, ym, zm],
#							  distance = dist_val, 
#							  crab = crab_val)
	
	myecube.draw()
	cube_1.draw() 
	#cube_2.draw() 

	for i in range(num_cubes):
		cub[i].draw()
#		lin[i].draw()	
	prev_ir_mid_x = ir_mid_x
	prev_ir_mid_y = ir_mid_y
	prev_ir_dist = ir_dist
#	time.sleep(0.015)


#print "x_t  y_t  z_t"
#o_file = open("info.txt",'w')

#o_file.write(str(x_t))
#o_file.write("\t")
#o_file.write(str(y_t))
#o_file.write("\t")
#o_file.write(str(z_t))
#o_file.close()
