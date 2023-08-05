import pyrbdl
import numpy as np
np.set_printoptions(linewidth=np.inf)
model = pyrbdl.Model()
is_floating_base = True
verbose = True
urdf_file_name = "OneJointRobot.urdf" #cube_234.urdf" #"zerojointrobot.urdf"#sphere_10meter_0.25kg.urdf" # "nao.urdf"

pyrbdl.URDFReadFromFile(urdf_file_name,model,is_floating_base, verbose)

print("model.dof_count = ",model.dof_count)
print("model.q_size=",model.q_size)


q = np.zeros(model.q_size,dtype = np.double)

update_kinematics = True

pyrbdl.TestAlgorithm(model, q)
H = pyrbdl.CompositeRigidBodyAlgorithm(model, q, update_kinematics)
print("H=",H)