import pyrbdl as rbdl
import time
print(dir(rbdl))

import numpy as np

model = rbdl.Model()

body_a = rbdl.Body (1., [1., 0., 0.], [1., 1., 1.])
joint_a = rbdl.Joint( [0., 1., 0., 0., 0., 0.])
body_a_id = model.AddBody(0, rbdl.Xtrans([0., 0., 2.]), joint_a, body_a, "body_a");

body_b = rbdl.Body (1., [1., 0., 0.], [1., 1., 1.])
joint_b = rbdl.Joint( [0., 1., 0., 0., 0., 0.])
body_b_id = model.AddBody(body_a_id, rbdl.Xtrans([0., 0., 2.]), joint_a, body_a, "body_b");

update_kinematics = True
local_pos=[0,0,0]
Q=[0,0]
pos_world_a = rbdl.CalcBodyToBaseCoordinates(model, Q, body_a_id, local_pos, update_kinematics)
pos_world_b = rbdl.CalcBodyToBaseCoordinates(model, Q, body_b_id, local_pos, update_kinematics)
print("pos_world_a=",pos_world_a)
print("pos_world_b=",pos_world_b)

print("model.dof_count=", model.dof_count)
while (1):
  time.sleep(1)
  