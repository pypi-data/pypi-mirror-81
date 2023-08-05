import pytinyopengl3 as p
import math, time
import pyrbdl as rbdl
import time
print(dir(rbdl))

import numpy as np

model = rbdl.Model()

com_a = [1., 0., 0.]
local_inertia_diag_a = [1., 1., 1.]
body_a = rbdl.Body (1., com_a, local_inertia_diag_a)
joint_a = rbdl.Joint( [0., 1., 0., 0., 0., 0.]) #joint frame (rotation, translation)
body_a_id = model.AddBody(0, rbdl.Xtrans([0., 0., 1.]), joint_a, body_a, "body_a");

body_b = rbdl.Body (1., [1., 0., 0.], [1., 1., 1.])
joint_b = rbdl.Joint( [0., 1., 0., 0., 0., 0.])
body_b_id = model.AddBody(body_a_id, rbdl.Xtrans([0., 0., 1.]), joint_a, body_a, "body_b");


print("model.dof_count=", model.dof_count)

app = p.TinyOpenGL3App("title")
app.renderer.init()
cam = app.renderer.get_active_camera()
cam.set_camera_distance(2.)
cam.set_camera_pitch(-20)

width = 256
height = 256
pixels = [255] * width * height * 3
colorR = 255
colorG = 255
colorB = 255

for i in range(width):
  for j in range(height):
     a = i < width / 2
     b = j < width / 2
     if (a == b):
        pixels[(i + j * width) * 3 + 0] = 0
        pixels[(i + j * width) * 3 + 1] = 255
        pixels[(i + j * width) * 3 + 2] = 255
     else:
      pixels[(i + j * width) * 3 + 0] = colorR
      pixels[(i + j * width) * 3 + 1] = colorG
      pixels[(i + j * width) * 3 + 2] = colorB


textureIndex = app.renderer.register_texture(pixels, width, height, False)
color = p.TinyVector3f(1.,1.,1.)
opacity = 1
orn = p.TinyQuaternionf(0.,0.,0.,1.)
pos = p.TinyVector3f(0.,0.,1.)
scaling = p.TinyVector3f(0.1,0.1,0.1)
shape = app.register_graphics_unit_sphere_shape(p.EnumSphereLevelOfDetail.SPHERE_LOD_HIGH, textureIndex)
sphere_a = app.renderer.register_graphics_instance(shape, pos, orn, color, scaling, opacity)
sphere_b = app.renderer.register_graphics_instance(shape, pos, orn, color, scaling, opacity)

app.renderer.write_transforms()


while not app.window.requested_exit():
  app.renderer.update_camera(2)
  dg = p.DrawGridData()
  dg.drawAxis=True
  app.draw_grid(dg)
  
  color=p.TinyVector3f(1,0,0)
  width=2
  
  #pos = p.TinyVector3f(0,0,math.sin(time.time())+1)

  update_kinematics = True
  local_pos=[0,0,0]
  Q=[math.sin(time.time()),0]
  pos_world_a = rbdl.CalcBodyToBaseCoordinates(model, Q, body_a_id, local_pos, update_kinematics)
  orn_world_a = rbdl.CalcBodyWorldOrientation(model, Q, body_a_id, update_kinematics)
  #print("orn_world_a=",orn_world_a)
  #print("orn_world_a[0]=",orn_world_a[0])
  #print("orn_world_a[0][0]=",orn_world_a[0][0])
  orn_a_mat = p.TinyMatrix3x3f( orn_world_a[0][0],orn_world_a[1][0],orn_world_a[2][0],
                                orn_world_a[0][1],orn_world_a[1][1],orn_world_a[2][1],
                                orn_world_a[0][2],orn_world_a[1][2],orn_world_a[2][2])
  orn_a = orn_a_mat.getRotation()
  
  
  #print("orn_a=",orn_a)
  #print("orn_world_a=",orn_world_a)
  pos_world_b = rbdl.CalcBodyToBaseCoordinates(model, Q, body_b_id, local_pos, update_kinematics)
  orn_world_b = rbdl.CalcBodyWorldOrientation(model, Q, body_b_id, update_kinematics)
  orn_b_mat = p.TinyMatrix3x3f( orn_world_b[0][0],orn_world_b[1][0],orn_world_b[2][0],
                                orn_world_b[0][1],orn_world_b[1][1],orn_world_b[2][1],
                                orn_world_b[0][2],orn_world_b[1][2],orn_world_b[2][2])
  orn_b = orn_b_mat.getRotation()
  
  #print("pos_world_a=",pos_world_a)
  #print("pos_world_b=",pos_world_b)

  pos_a = p.TinyVector3f(pos_world_a[0],pos_world_a[1],pos_world_a[2])
  pos_b = p.TinyVector3f(pos_world_b[0],pos_world_b[1],pos_world_b[2])
  app.renderer.write_single_instance_transform_to_cpu(pos_a, orn_a,sphere_a)
  app.renderer.write_single_instance_transform_to_cpu(pos_b, orn_b,sphere_b)
  
  app.renderer.draw_line(pos_a,pos_b,color,width)
  
  app.renderer.write_transforms()  
  app.renderer.render_scene()
  app.draw_text_3d("hi",1,1,1,1)
  app.swap_buffer()

