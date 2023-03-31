import pyvista as pv
from pyvistaqt import BackgroundPlotter

# Function for updating the positions of the meshes and light in the update loop as a callback
def update_scene():
    # PyVista has simplified rotation methods for each rotation direction or you call call the rotate method and explicitly specify all rotations
    # We call inplace=True to update the changes to the mesh directly
    #mesh.rotate_y(10,inplace=True)
    sphere.rotate_y(-10,inplace=True)
    #move mesh 10 cells in x axis
    mesh1.translate([10,0,0],inplace=False)
    #print position of mesh
    #print(mesh.center)
    #move mesh to position

    
    mesh1.rotate_y(-10,inplace=False)
    
    
    # As the light object does not contain a rotate method, we just update its position based on the sphere.center position. 
    # The position method can both get and set the light position.
    light.position = sphere.center
    # We update the whole plotter
    p.update()

if __name__ == '__main__':
    # Load the mesh or point cloud if required
    mesh_path = 'Test_scripts\model.obj'
    mesh = pv.read(mesh_path)
    mesh1 = pv.read(mesh_path)
    # if the mesh has a texture, it needs to be loaded separetely using read_texture
    #tex_path = 'mesh/angelStatue_lp.jpg'
    #tex = pv.read_texture(tex_path)

    # We create a plotter for non-blocking visualization, using pyvistaqt. If we don't need interactivity or animations we can just call pyvista.Plotter
    p = BackgroundPlotter(window_size=(1280, 720), title='PyVistaQt Plotter', multi_samples=8, line_smoothing=True, point_smoothing=True, polygon_smoothing=True, auto_update=False)
    
    # We set the camera position to be in the xy plane 
    p.camera_position = [(0, 0, 100), (0, 0, 0), (0, 1, 0)]
    # We set the front and back clipping planes
    p.camera.clipping_range = (0, 100)

    # We create the sphere which will orbit the angel statue and set its radius and center
    sphere = pv.Sphere(radius = 0.2, center=(0, 0, 100))

    # We create a blue point light at the position of the sphere
    light = pv.Light((0, 0, 1), (0, 0, 0), 'blue')

    # We add the angel statue mesh together with its texture to the plotter
    p.add_mesh(mesh,name='angel',texture = None)
    p.add_mesh(mesh1, color='red', opacity=0.5, name='angel1', show_edges=True, line_width=5, render_points_as_spheres=True)
    # We add the sphere to the plotter. Just to demonstrate that PyVista supports the pbr rendering from VTK we make the sphere metallic.
    # If you get an error here your VTK version is <9.0. Either remove the pbr value or upgrade.
    p.add_mesh(sphere, pbr=True, metallic=0.7, roughness=0.2, diffuse=1)
    # We add the light to the plotter
    p.add_light(light)
    p.add_axes()
    p.add_bounding_box()
    #m0ve mesh1 to diffrent side of bounding box
    mesh1.translate([10,0,0],inplace=False)

    # We add the update_scene function as a callback to the plotter. The interval is in milliseconds.
    p.add_callback(update_scene, interval=100)
    
    p.add_toolbars()
    p.add_slider_widget(update_scene, [0, 100], value=50, title='Slider', pointa=(0.8, 0.1), pointb=(0.9, 0.1))


    #p.add_callback(update_scene, interval=100)
    print(mesh)

    # We show the plotter and call p.app.exec_(), so the plotter stays open. This is important when running the pyvistaqt plotter.
    # If your visualization automatically closes add the last line
    p.show() 
    p.app.exec_()

