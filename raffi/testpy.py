"""
VSC Extension "Blender Development" von Jaques Lucke zuerst installieren
Python-Umgebung von Blender in VSC auswählen --> CTRL+Shift+P --> Pyhton: Select Interpreter --> In den Blender Ordner
pip install bpy
"""

import bpy
import math
import time

object_name = "House"

# Suche nach dem Objekt in der Szene
obj = bpy.data.objects.get(object_name)

if obj:
    # Schleife 25 Mal
    for i in range(25):
        # Bewege das Objekt entlang der Y-Achse um 1 Einheit
        obj.location.y += 1

        # Drehe das Objekt um 5 Grad um die Z-Achse
        obj.rotation_euler.z += math.radians(5)

        # Aktualisiere das Objekt in Blender
        bpy.context.view_layer.update()
        print("Durchführung: ", i + 1)

        # Warte 0,02 Sekunden
        time.sleep(0.02)

        # Erzwinge die Aktualisierung der Benutzeroberfläche
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
else:
    print("Objekt nicht gefunden: " + object_name)
    
    
    
if obj:
    # Schleife x Mal
    for i in range(60):
        # Bewege das Objekt entlang der Y-Achse um 1 Einheit
        obj.location.x -= 1

        # Drehe das Objekt um x Grad um die Z-Achse
        obj.rotation_euler.z += math.radians(5)

        # Aktualisiere das Objekt in Blender
        bpy.context.view_layer.update()
        print("Durchführung: ", i + 1)

        # Warte x Sekunden
        time.sleep(0.02)

        # Erzwinge die Aktualisierung der Benutzeroberfläche
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
else:
    print("Objekt nicht gefunden: " + object_name)


if obj:
    # Schleife x Mal
    for i in range(65):
        # Bewege das Objekt entlang der Y-Achse um 1 Einheit
        obj.location.y -= 1

        # Drehe das Objekt um x Grad um die Z-Achse
        obj.rotation_euler.z += math.radians(5)

        # Aktualisiere das Objekt in Blender
        bpy.context.view_layer.update()
        print("Durchführung: ", i + 1)

        # Warte x Sekunden
        time.sleep(0.02)

        # Erzwinge die Aktualisierung der Benutzeroberfläche
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
else:
    print("Objekt nicht gefunden: " + object_name)
    
    

if obj:
    # Schleife x Mal
    for i in range(65):
        # Bewege das Objekt entlang der Y-Achse um 1 Einheit
        obj.location.x += 1

        # Drehe das Objekt um x Grad um die Z-Achse
        obj.rotation_euler.z += math.radians(5)

        # Aktualisiere das Objekt in Blender
        bpy.context.view_layer.update()
        print("Durchführung: ", i + 1)

        # Warte x Sekunden
        time.sleep(0.02)

        # Erzwinge die Aktualisierung der Benutzeroberfläche
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
else:
    print("Objekt nicht gefunden: " + object_name)


if obj:
    # Schleife x Mal
    for i in range(40):
        # Bewege das Objekt entlang der Y-Achse um 1 Einheit
        obj.location.y += 1

        # Drehe das Objekt um x Grad um die Z-Achse
        obj.rotation_euler.z += math.radians(5)

        # Aktualisiere das Objekt in Blender
        bpy.context.view_layer.update()
        print("Durchführung: ", i + 1)

        # Warte x Sekunden
        time.sleep(0.02)

        # Erzwinge die Aktualisierung der Benutzeroberfläche
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
else:
    print("Objekt nicht gefunden: " + object_name)
    
    
if obj:
    # Schleife x Mal
    for i in range(10):
        # Bewege das Objekt entlang der Y-Achse um 1 Einheit
        obj.location.x -= 1

        # Drehe das Objekt um x Grad um die Z-Achse
        obj.rotation_euler.z += math.radians(5)

        # Aktualisiere das Objekt in Blender
        bpy.context.view_layer.update()
        print("Durchführung: ", i + 1)

        # Warte x Sekunden
        time.sleep(0.02)

        # Erzwinge die Aktualisierung der Benutzeroberfläche
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
else:
    print("Objekt nicht gefunden: " + object_name)
    