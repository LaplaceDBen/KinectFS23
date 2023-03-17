import pyvista as pv

# load the STL file
mesh = pv.read('CatanHouse.stl')

# create a plane
plane = pv.Plane(center=(0,0,0), direction=(0,0,1), i_size=10, j_size=10)

# plot the mesh and the plane
p = pv.Plotter()
p.add_mesh(mesh)
p.add_mesh(plane, color='white')
p.show()

import numpy as np

# define the animation path
path = np.array([[0,1,5], [0,0,5], [5,3,3], [0,1,5]])

# create the plotter
p = pv.Plotter()

# add the plane
plane = pv.Plane(center=(0,0,0), direction=(0,0,1), i_size=10, j_size=10)
p.add_mesh(plane, color='white')

# add the mesh as a textured mesh
texture = pv.read_texture('path/to/texture.jpg')
textured_mesh = pv.textured_sphere(texture=texture)
p.add_textured_mesh(textured_mesh)

# create the animation loop
for i in range(path.shape[0]):
    # update the mesh position
    textured_mesh.center = path[i]
    # render the scene
    p.show(auto_close=False)
    # pause for a short time
    pv.plotting.update() # this is necessary for some backends
    pv.plotting.time.sleep(0.1)

# close the plotter
p.close()