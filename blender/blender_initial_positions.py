import bpy
import math

house_A_object_name = "House"
house_B_object_name = "Modern House"
house_C_object_name = "Apartment building"
house_D_object_name = "House.001"
tree_object_name = "Tree"

obj1 = bpy.data.objects.get(house_A_object_name)
if obj1:
    obj1.location.x = 15
    obj1.location.y = 80
    obj1.rotation_euler.z = math.radians(270)

obj2 = bpy.data.objects.get(house_B_object_name)
if obj2:
    obj2.location.x = 25
    obj2.location.y = 30
    obj2.rotation_euler.z = math.radians(270)

obj3 = bpy.data.objects.get(house_C_object_name)
if obj3:
    obj3.location.x = -20
    obj3.location.y = 35
    obj3.rotation_euler.z = math.radians(0)

obj4 = bpy.data.objects.get(house_D_object_name)
if obj4:
    obj4.location.x = 20
    obj4.location.y = -15
    obj4.rotation_euler.z = math.radians(0)

obj5 = bpy.data.objects.get(tree_object_name)
if obj5:
    obj5.location.x = 55
    obj5.location.y = 38
    obj5.rotation_euler.z = math.radians(0.000014)
        
bpy.context.view_layer.update()
bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        