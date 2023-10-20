import bpy
import bmesh
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import threading

df = pd.read_csv("/Users/ryantwemlow/Documents/KNN Blender/iris.csv")

print(df.head())

main_data = np.array(df[["5.1", "3.5", "1.4"]])

labels = df["Iris-setosa"]

materials = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]


label_encoder = LabelEncoder()
label_encoder.fit(labels)
integer_labels = label_encoder.transform(labels)

def showData(main_data , labels):
    for i in range(len(main_data)):
        bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(main_data[i][0], main_data[i][1], main_data[i][2]), 
        scale=(0.1, 0.1, 0.1))
        ob = bpy.context.active_object
        print(ob.data.materials)
        mat = bpy.data.materials.get(materials[integer_labels[i]])
        if ob.data.materials:
            ob.data.materials[0] = mat
        else:
            ob.data.materials.append(mat)
            
def countOccurance(list_):
    cache = []
    finalDict = {}
    for i in list_:
        if i in cache:
            finalDict[i] += 1
        else:
            cache.append(i)
            finalDict[i] = 1
    return finalDict
        
        
        
ob = bpy.context.active_object


def calculateDistance(vec1, vec2):
    return np.sqrt(np.sum((vec1 - vec2)**2))

def createPath(sloc, eloc):
    #Create a new mesh object and link it to the scene
    mesh = bpy.data.meshes.new("path_mesh")
    obj = bpy.data.objects.new("Path_Object", mesh)
    scene = bpy.context.scene
    scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    #create bmesh object
    #create bmesh object
    bm = bmesh.new()

    #create the start and end verts
    start_vert = bm.verts.new(sloc)
    end_vert = bm.verts.new(eloc)

    # create an edge between the verts
    bm.edges.new((start_vert, end_vert))

    #Update the mesh with the new verts and free the bmesh
    bm.to_mesh(mesh)
    bm.free()

    # Create curve from mesh
    bpy.ops.object.convert(target='CURVE')
    bpy.context.object.data.bevel_depth = 0.004
    mat = bpy.data.materials.get("wire")
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    

    
    
def determineClass(dataset, k):    
    distanceList = []
    ob = bpy.context.active_object
    loc = np.array(ob.location)
    print(loc)
    for i in range(len(dataset)):
        distanceList.append((integer_labels[i], calculateDistance(loc, main_data[i]), main_data[i]))
        
    sorted_points = sorted(distanceList, key=lambda x: x[1])
    coordinates = [sorted_points[i][2] for i in range(len(sorted_points)) if i < k]
    class_selection = [sorted_points[i][0] for i in range(len(sorted_points)) if i < k]
    for i in coordinates:
        createPath(ob.location, i)
    result = countOccurance(class_selection)
    print(result)
    maximum = 0
    top_class = 0
    for (key, value) in result.items():
        if maximum < value:
            top_class = key
            maximum = value
    print(top_class)
    mat = bpy.data.materials.get(materials[top_class])
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)
            
  
    
determineClass(main_data, 60)

