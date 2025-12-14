import bpy, mathutils, math
from mathutils import Vector

#===================================================CREATE BONE======================================
collection_name = "WGT_COD_RIG"

# Данные по объектам:  Имя : Тип Empty
empty_data = {
    "Ball": "CIRCLE",
    "Clavicle": "CUBE",
    "ClavicleIK": "SPHERE",
    "ElbowPoleIk": "SPHERE",
    "Eye": "CIRCLE",
    "Eyeball": "SPHERE",
    "EyeIK": "CUBE",
    "Finger": "SPHERE",
    "HandIK": "CIRCLE",
    "Head": "SPHERE",
    "HeelIK": "CUBE",
    "KneePole": "SPHERE",
    "Spine": "CUBE",
    "Wrist": "CUBE",
    "WristIK": "SPHERE"   # "Cphere" исправлено на обычный Sphere
}

# Удаляем старую коллекцию, если есть
if collection_name in bpy.data.collections:
    old_col = bpy.data.collections[collection_name]
    bpy.data.collections.remove(old_col)

# Создаём коллекцию
col = bpy.data.collections.new(collection_name)
bpy.context.scene.collection.children.link(col)

# Создание объектов
created_objects = []

for name, empty_type in empty_data.items():
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = empty_type
    obj.empty_display_size = 1
    col.objects.link(obj)
    created_objects.append(obj)

# Скрыть коллекцию полностью
col.hide_viewport = True
col.hide_render = True

print("Готово! Все Empty созданы, добавлены в коллекцию и скрыты.")

#===================================MAIN IK RIG==================================================================

Edit_bones = bpy.context.object.data.edit_bones
Pose_bones = bpy.context.object.pose.bones

ConnectBones = (
"j_shoulder_ri", "j_elbow_ri", "j_wrist_ri", "j_shoulder_le", "j_elbow_le", "j_wrist_le",

"j_knee_ri", "j_ankle_ri", "j_ball_ri", "j_knee_le", "j_ankle_le", "j_ball_le",

"j_thumb_ri_2", "j_thumb_ri_3",
"j_index_ri_2", "j_index_ri_3",
"j_mid_ri_2", "j_mid_ri_3",
"j_ring_ri_2", "j_ring_ri_3",
"j_pinky_ri_2", "j_pinky_ri_3",

"j_thumb_le_2", "j_thumb_le_3",
"j_index_le_2", "j_index_le_3",
"j_mid_le_2", "j_mid_le_3",
"j_ring_le_2", "j_ring_le_3",
"j_pinky_le_2", "j_pinky_le_3",
)

bpy.ops.object.mode_set(mode='EDIT')

for bone in ConnectBones:
    if Edit_bones.get(bone) is not None: 
        ParentBone = Edit_bones[bone].parent				
        ParentBone.tail = Edit_bones[bone].head
        
RotateBones = (
"j_wrist_ri", "j_wristfronttwist1_ri", "j_wrist_le", "j_wristfronttwist1_le", "j_ball_ri", "j_ball_le", 
"j_thumb_ri_3", "j_index_ri_3", "j_mid_ri_3", "j_ring_ri_3", "j_pinky_ri_3", 
"j_thumb_le_3", "j_index_le_3", "j_mid_le_3", "j_ring_le_3", "j_pinky_le_3",
)

bpy.ops.armature.select_all(action='DESELECT')
bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'

for bone in RotateBones:
    if Edit_bones.get(bone) is not None:
        bpy.ops.armature.select_all(action='DESELECT')
        Edit_bones[bone].select_tail = True
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='NORMAL')

def HandIKPrep(IKParentBone, IKParentRoll, IKConstraintBone, IKConstraintRoll, IKPoleName, IKPoleLength, IKPoleDistance, IKPoleRoll, IKTargetBone, IKTargetLength, IKControlName, IKControlLength):
    Edit_bones[IKParentBone].roll = IKParentRoll
    Edit_bones[IKConstraintBone].roll = IKConstraintRoll
    CreatePoleBone = bpy.context.object.data.edit_bones.new(IKPoleName)
    CreatePoleBone.head = Edit_bones[IKConstraintBone].head + Vector((IKPoleDistance, 0, 0))
    CreatePoleBone.tail = CreatePoleBone.head + Vector((IKPoleLength, 0, 0))
    CreatePoleBone.roll = IKPoleRoll
    Edit_bones[IKTargetBone].length = IKTargetLength
    CreateControlBone = bpy.context.object.data.edit_bones.new(IKControlName)
    CreateControlBone.head = Edit_bones[IKTargetBone].head
    CreateControlBone.tail = Edit_bones[IKTargetBone].tail
    CreateControlBone.length = IKControlLength
    Edit_bones[IKTargetBone].parent = CreateControlBone

    
HandIKPrep("j_shoulder_ri", -30/180*3.141, "j_elbow_ri", -102/180*3.141, "ElbowPole.R", -5, -50, 1.5708, "j_wrist_ri", 4, "HandIK.R", 8)
HandIKPrep("j_shoulder_le", -2.6/180*3.141, "j_elbow_le", -20/180*3.141, "ElbowPole.L", -5, -50, 1.5708, "j_wrist_le", 4, "HandIK.L", 8)



Edit_bones["j_thumb_ri_3"].length = -3.6
Edit_bones["j_index_ri_3"].length = -2.6
Edit_bones["j_mid_ri_3"].length = -3
Edit_bones["j_ring_ri_3"].length = -3
Edit_bones["j_pinky_ri_3"].length = -2.7
Edit_bones["j_thumb_le_3"].length = -3.6
Edit_bones["j_index_le_3"].length = 2.6
Edit_bones["j_mid_le_3"].length = -3
Edit_bones["j_ring_le_3"].length = -3
Edit_bones["j_pinky_le_3"].length = -2.7

Edit_bones["j_pinky_le_1"].roll = 260 / 180 * 3.141
Edit_bones["j_pinky_le_2"].roll = 303 / 180 * 3.141
Edit_bones["j_pinky_le_3"].roll = -327 / 180 * 3.141
Edit_bones["j_ring_le_1"].roll = -106 / 180 * 3.141
Edit_bones["j_ring_le_2"].roll = 296 / 180 * 3.141
Edit_bones["j_ring_le_3"].roll = -340 / 180 * 3.141
Edit_bones["j_mid_le_1"].roll = -104 / 180 * 3.141
Edit_bones["j_mid_le_2"].roll = 315 / 180 * 3.141
Edit_bones["j_mid_le_3"].roll = 19 / 180 * 3.141
Edit_bones["j_index_le_1"].roll = -102 / 180 * 3.141
Edit_bones["j_index_le_2"].roll = -79 / 180 * 3.141
Edit_bones["j_index_le_3"].roll = -29 / 180 * 3.141
Edit_bones["j_thumb_le_1"].roll = -18 / 180 * 3.141
Edit_bones["j_thumb_le_2"].roll = 19 / 180 * 3.141
Edit_bones["j_thumb_le_3"].roll = 30 / 180 * 3.141

Edit_bones["j_pinky_ri_1"].roll = 21 / 180 * 3.141
Edit_bones["j_pinky_ri_2"].roll = 37 / 180 * 3.141
Edit_bones["j_pinky_ri_3"].roll = 45 / 180 * 3.141
Edit_bones["j_ring_ri_1"].roll = 16 / 180 * 3.141
Edit_bones["j_ring_ri_2"].roll = 34 / 180 * 3.141
Edit_bones["j_ring_ri_3"].roll = 43 / 180 * 3.141
Edit_bones["j_mid_ri_1"].roll = 2.3 / 180 * 3.141
Edit_bones["j_mid_ri_2"].roll = 27 / 180 * 3.141
Edit_bones["j_mid_ri_3"].roll = 37 / 180 * 3.141
Edit_bones["j_index_ri_1"].roll = -17 / 180 * 3.141
Edit_bones["j_index_ri_2"].roll = -2.2 / 180 * 3.141
Edit_bones["j_index_ri_3"].roll = 16 / 180 * 3.141
Edit_bones["j_thumb_ri_1"].roll = -143 / 180 * 3.141
Edit_bones["j_thumb_ri_2"].roll = -114 / 180 * 3.141
Edit_bones["j_thumb_ri_3"].roll = -108 / 180 * 3.141

Edit_bones["j_knee_ri"].head = Edit_bones["j_knee_ri"].head + Vector((1.5, 0, 0))
Edit_bones["j_hip_ri"].tail = Edit_bones["j_knee_ri"].head
Edit_bones["j_knee_le"].head = Edit_bones["j_knee_le"].head + Vector((1.5, 0, 0))
Edit_bones["j_hip_le"].tail = Edit_bones["j_knee_le"].head

def LegIKPrep(IKParentBone, IKParentRoll, IKConstraintBone, IKConstraintRoll, IKPoleName, IKPoleLength, IKPoleDistance, IKPoleRoll, IKTargetBone, IKControlName, ):
    Edit_bones[IKParentBone].roll = IKParentRoll
    Edit_bones[IKConstraintBone].roll = IKConstraintRoll
    CreatePoleBone = bpy.context.object.data.edit_bones.new(IKPoleName)
    CreatePoleBone.head = Edit_bones[IKConstraintBone].head + Vector((IKPoleDistance, 0, 0))
    CreatePoleBone.tail = CreatePoleBone.head + Vector((IKPoleLength, 0, 0))
    CreatePoleBone.roll = IKPoleRoll
    CreateControlBone = bpy.context.object.data.edit_bones.new(IKControlName)
    CreateControlBone.head = Edit_bones[IKTargetBone].head
    CreateControlBone.tail = Edit_bones[IKTargetBone].head + Vector((-10, 0, 0))
    CreateControlBone.roll = -1.5708
    Edit_bones[IKTargetBone].parent = CreateControlBone
    CreatePoleBone.parent = CreateControlBone


LegIKPrep("j_hip_ri", -3.4/180*3.141, "j_knee_ri", 9.5/180*3.141, "KneePole.R", 10, 50, 1.5708, "j_ankle_ri", "HeelIK.R")
LegIKPrep("j_hip_le", -3.4/180*3.141, "j_knee_le", 9.5/180*3.141, "KneePole.L", 10, 50, 1.5708, "j_ankle_le", "HeelIK.L")

bpy.ops.object.mode_set(mode='POSE')

def LimbIKSetup(IKConstraintBone, IKPoleName, IKControlName, IKPoleAngle, IKTargetBone):    
    ParentIK = Pose_bones[IKConstraintBone].constraints.new("IK")
    ParentIK.name = 'IK'
    ParentIK.target = bpy.data.objects[bpy.context.active_object.name]
    ParentIK.subtarget = IKControlName
    ParentIK.chain_count = 2
    ParentIK.pole_target = bpy.data.objects[bpy.context.active_object.name]
    ParentIK.pole_subtarget = IKPoleName
    ParentIK.pole_angle = IKPoleAngle
    
    TargetCopyLocation = Pose_bones[IKTargetBone].constraints.new("COPY_LOCATION")
    TargetCopyLocation.target = bpy.data.objects[bpy.context.active_object.name]
    TargetCopyLocation.subtarget = IKConstraintBone
    TargetCopyLocation.head_tail = 1
    TargetCopyLocation.target_space = "WORLD"
    TargetCopyLocation.owner_space = "WORLD"
    
LimbIKSetup("j_elbow_ri", "ElbowPole.R", "HandIK.R", 3.141, "j_wrist_ri")
LimbIKSetup("j_elbow_le", "ElbowPole.L", "HandIK.L", 3.141, "j_wrist_le")

LimbIKSetup("j_knee_ri", "KneePole.R", "HeelIK.R", 0, "j_ankle_ri")
LimbIKSetup("j_knee_le", "KneePole.L", "HeelIK.L", 0, "j_ankle_le")

def ArmTwistSetup(TwistBoneName, IKTargetBone):      
    TargetCopyRotation1 = Pose_bones[TwistBoneName].constraints.new("COPY_ROTATION")
    TargetCopyRotation1.target = bpy.data.objects[bpy.context.active_object.name]
    TargetCopyRotation1.subtarget = IKTargetBone
    TargetCopyRotation1.target_space = "LOCAL"
    TargetCopyRotation1.owner_space = "LOCAL"
    TargetCopyRotation1.use_x = False
    TargetCopyRotation1.use_z = False
    TargetCopyRotation1.influence = 0.6
    
    TargetCopyRotation2 = Pose_bones[TwistBoneName].constraints.new("COPY_ROTATION")
    TargetCopyRotation2.target = bpy.data.objects[bpy.context.active_object.name]
    TargetCopyRotation2.subtarget = IKTargetBone
    TargetCopyRotation2.target_space = "LOCAL"
    TargetCopyRotation2.owner_space = "LOCAL"
    TargetCopyRotation2.use_x = False
    TargetCopyRotation2.use_y = False
    TargetCopyRotation2.influence = 0.372
    
    DriverAdd = Pose_bones[TwistBoneName].driver_add('location', 1) 
    DriverVariable = DriverAdd.driver.variables.new()
    DriverVariable.type = "TRANSFORMS"
    DriverTarget = DriverVariable.targets[0]
    DriverTarget.id = bpy.data.objects[bpy.context.active_object.name]
    DriverTarget.bone_target = IKTargetBone
    DriverTarget.transform_type  = 'ROT_X'
    DriverTarget.transform_space = 'LOCAL_SPACE'
    DriverTarget.rotation_mode = 'QUATERNION'

    DriverAdd.driver.expression = "-abs(var * .025)"

ArmTwistSetup("j_wristfronttwist1_ri", "j_wrist_ri")
ArmTwistSetup("j_wristfronttwist1_le", "j_wrist_le")

def LegTwistSetup(IKConstraintBone, IKTargetBone):     
    TargetCopyLocation = Pose_bones[IKTargetBone].constraints.new("COPY_LOCATION")
    TargetCopyLocation.target = bpy.data.objects[bpy.context.active_object.name]
    TargetCopyLocation.subtarget = IKConstraintBone
    TargetCopyLocation.head_tail = 1
    TargetCopyLocation.target_space = "WORLD"
    TargetCopyLocation.owner_space = "WORLD"
    
LegTwistSetup("j_knee_ri", "j_ankle_ri")
LegTwistSetup("j_knee_le", "j_ankle_le")

bone_pairs = [
    ("j_proc_lift_clavicle_le", "j_clavicle_le"),
    ("j_proc_lift_clavicle_ri", "j_clavicle_ri"),
]

#====================================================================================================

# Кости, которые нужно привязать
child_bones = ["ElbowPole.L", "ElbowPole.R"]

# Кость-родитель
parent_bone = "j_mainroot"

# Берём выделенный объект (должен быть Armature)
obj = bpy.context.object

if obj is None or obj.type != 'ARMATURE':
    raise Exception("Выдели объект Armature перед запуском скрипта!")

# Переходим в Edit Mode
bpy.ops.object.mode_set(mode='EDIT')

eb = obj.data.edit_bones

# Проверяем существование кости-родителя
if parent_bone not in eb:
    raise Exception(f"Кость родитель '{parent_bone}' не найдена")

# Назначаем родителей
for b in child_bones:
    if b in eb:
        eb[b].parent = eb[parent_bone]
        eb[b].use_connect = False   # Важно: Keep Offset (как на скрине)
    else:
        print(f"⚠ Кость '{b}' не найдена")

# Возвращаемся в Object Mode
bpy.ops.object.mode_set(mode='OBJECT')

#====================================================================================================

armature = bpy.context.object
if armature is None or armature.type != 'ARMATURE':
    raise Exception("Выберите объект типа Armature в режиме Object или Pose.")

bpy.ops.object.mode_set(mode='POSE')

for owner_bone, target_bone in bone_pairs:
    pose_bone = armature.pose.bones.get(owner_bone)
    if pose_bone is None:
        print(f"⚠️ Кость '{owner_bone}' не найдена, пропускаю.")
        continue

    for c in list(pose_bone.constraints):
        if c.name in {f"Copy Location ({target_bone})", f"Copy Rotation ({target_bone})"}:
            pose_bone.constraints.remove(c)

    copy_loc = pose_bone.constraints.new(type='COPY_LOCATION')
    copy_loc.name = f"Copy Location ({target_bone})"
    copy_loc.target = armature
    copy_loc.subtarget = target_bone
    copy_loc.target_space = 'LOCAL'
    copy_loc.owner_space = 'LOCAL'

    copy_rot = pose_bone.constraints.new(type='COPY_ROTATION')
    copy_rot.name = f"Copy Rotation ({target_bone})"
    copy_rot.target = armature
    copy_rot.subtarget = target_bone
    copy_rot.target_space = 'LOCAL'
    copy_rot.owner_space = 'LOCAL'


bone_pairs = [
    ("ElbowPole.L", "j_elbowdq_le"),
    ("ElbowPole.R", "j_elbowdq_ri"),
]

armature = bpy.context.object
if armature is None or armature.type != 'ARMATURE':
    raise Exception("Выбери объект типа Armature в Object или Pose режиме.")

bpy.ops.object.mode_set(mode='POSE')

for owner_bone, target_bone in bone_pairs:
    pose_bone = armature.pose.bones.get(owner_bone)
    if pose_bone is None:
        print(f"⚠️ Кость '{owner_bone}' не найдена, пропускаю.")
        continue

    for c in list(pose_bone.constraints):
        if c.type == 'CHILD_OF' and c.name == f"Child Of ({target_bone})":
            pose_bone.constraints.remove(c)

    con = pose_bone.constraints.new(type='CHILD_OF')
    con.name = f"Child Of ({target_bone})"
    con.target = armature
    con.subtarget = target_bone

    con.use_location_x = True
    con.use_location_y = True
    con.use_location_z = True
    con.use_rotation_x = False
    con.use_rotation_y = False
    con.use_rotation_z = False
    con.use_scale_x = False
    con.use_scale_y = False
    con.use_scale_z = False


    con.influence = 1.0
    bpy.context.view_layer.objects.active = armature
    bpy.ops.pose.select_all(action='DESELECT')
    pose_bone.select = True
    armature.data.bones.active = pose_bone.bone
    bpy.ops.constraint.childof_set_inverse(
    constraint=con.name,
    owner='BONE'
)


source_bones = [
    "j_thumb_le_3", "j_thumb_ri_3",
    "j_index_le_3", "j_index_ri_3",
    "j_mid_le_3", "j_mid_ri_3",
    "j_ring_le_3", "j_ring_ri_3",
    "j_pinky_le_3", "j_pinky_ri_3",
]

extrude_length = -1.0

armature = bpy.context.object
if armature is None or armature.type != 'ARMATURE':
    raise Exception("Выбери объект типа Armature в Object или Edit режиме.")


bpy.ops.object.mode_set(mode='EDIT')
edit_bones = armature.data.edit_bones

for bone_name in source_bones:
    bone = edit_bones.get(bone_name)
    if bone is None:
        print(f"⚠️ Кость '{bone_name}' не найдена, пропускаю.")
        continue

    new_bone = edit_bones.new(f"{bone_name}_ik")


    new_bone.head = bone.tail.copy()

    direction = (bone.tail - bone.head).normalized()

    new_bone.tail = bone.tail - direction * extrude_length


    new_bone.parent = bone
    new_bone.use_connect = False

    print(f"✅ Создана кость {new_bone.name} длиной {extrude_length}")

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bpy.ops.object.mode_set(mode='POSE')

obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise ValueError("Выдели объект арматуры перед запуском скрипта!")

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = obj.data.edit_bones

bone_pairs = {
    "j_wrist_le": "j_wrist_le_ik",
    "j_wrist_ri": "j_wrist_ri_ik"
}
offset_z = 2.0

def create_ik_bone(src_name, ik_name, offset_z):
    if src_name not in edit_bones:
        print(f"⚠ Кость '{src_name}' не найдена — пропущена.")
        return

    src_bone = edit_bones[src_name]
    new_bone = edit_bones.new(ik_name)
    new_bone.head = src_bone.head.copy()
    new_bone.tail = src_bone.tail.copy()
    new_bone.roll = src_bone.roll

    mat = src_bone.matrix.to_3x3()
    local_z = mat.col[1].normalized()

    offset_vec = local_z * offset_z
    new_bone.head += offset_vec
    new_bone.tail += offset_vec


    new_bone.parent = src_bone
    new_bone.use_connect = False

    print(f"✅ Создана '{ik_name}' и подключена к '{src_name}' (Keep Offset, смещение по Y={offset_z})")


for src, ik in bone_pairs.items():
    create_ik_bone(src, ik, offset_z)

bpy.ops.object.mode_set(mode='OBJECT')
print(f"Готово! Созданы IK-кости для: {', '.join(bone_pairs.keys())}")

for src, ik in bone_pairs.items():
    create_ik_bone(src, ik, offset_z)

bpy.ops.object.mode_set(mode='OBJECT')
print(f"Готово! Созданы IK-кости для: {', '.join(bone_pairs.keys())}")

for src, ik in bone_pairs.items():
    create_ik_bone(src, ik, offset_z)

bpy.ops.object.mode_set(mode='OBJECT')
print(f"Готово! Созданы IK-кости для: {', '.join(bone_pairs.keys())}")

parent_sets = {
    "j_wrist_le_ik": [
        "j_thumb_le_3_ik",
        "j_index_le_3_ik",
        "j_mid_le_3_ik",
        "j_ring_le_3_ik",
        "j_pinky_le_3_ik"
    ],
    "j_wrist_ri_ik": [
        "j_thumb_ri_3_ik",
        "j_index_ri_3_ik",
        "j_mid_ri_3_ik",
        "j_ring_ri_3_ik",
        "j_pinky_ri_3_ik"
    ]
}

armature = bpy.context.object
if armature is None or armature.type != 'ARMATURE':
    raise Exception("Выбери объект типа Armature в Object или Edit режиме.")

bpy.ops.object.mode_set(mode='EDIT')

edit_bones = armature.data.edit_bones

for parent_name, children in parent_sets.items():
    parent_bone = edit_bones.get(parent_name)
    if parent_bone is None:
        print(f"⚠️ Родительская кость '{parent_name}' не найдена, пропускаю.")
        continue

    for child_name in children:
        child_bone = edit_bones.get(child_name)
        if child_bone is None:
            print(f"⚠️ Кость '{child_name}' не найдена, пропускаю.")
            continue

        child_bone.use_connect = False
        child_bone.parent = parent_bone
        print(f"✅ '{child_name}' теперь дочерняя к '{parent_name}' (Keep Offset)")

bpy.ops.object.mode_set(mode='POSE')


ik_pairs = [
    ("j_thumb_le_3", "j_thumb_le_3_ik", 3),
    ("j_thumb_ri_3", "j_thumb_ri_3_ik", 3),
    ("j_index_le_3", "j_index_le_3_ik", 4),
    ("j_index_ri_3", "j_index_ri_3_ik", 4),
    ("j_ring_le_3", "j_ring_le_3_ik", 4),
    ("j_ring_ri_3", "j_ring_ri_3_ik", 4),
    ("j_mid_le_3", "j_mid_le_3_ik", 4),
    ("j_mid_ri_3", "j_mid_ri_3_ik", 4),
    ("j_pinky_le_3", "j_pinky_le_3_ik", 4),
    ("j_pinky_ri_3", "j_pinky_ri_3_ik", 4),
]

armature = bpy.context.object
if armature is None or armature.type != 'ARMATURE':
    raise Exception("Выбери объект типа Armature в Object или Pose режиме.")

bpy.ops.object.mode_set(mode='POSE')

for bone_name, target_bone_name, chain_len in ik_pairs:
    pose_bone = armature.pose.bones.get(bone_name)
    if pose_bone is None:
        print(f"⚠️ Кость '{bone_name}' не найдена, пропускаю.")
        continue

    for c in list(pose_bone.constraints):
        if c.type == 'IK' and c.name == f"IK_to_{target_bone_name}":
            pose_bone.constraints.remove(c)

    ik = pose_bone.constraints.new(type='IK')
    ik.name = f"IK_to_{target_bone_name}"
    ik.target = armature
    ik.subtarget = target_bone_name
    ik.chain_count = chain_len
# Проверяем, что выделен объект-армейчер
obj = bpy.context.object
if obj and obj.type == 'ARMATURE':
    arm = obj
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = arm.data.edit_bones

    # Проверяем наличие родительской кости
    parent_bone = edit_bones.get("j_spine4")
    if not parent_bone:
        print("Кость 'j_spine4' не найдена! Создание остановлено.")
    else:
        # Функция для создания IK-кости и настройки
        def create_ik(src_name):
            ik_name = src_name + "_ik"
            if src_name not in edit_bones:
                print(f"Кость '{src_name}' не найдена.")
                return None
            
            src_bone = edit_bones[src_name]
            new_bone = edit_bones.new(ik_name)
            new_bone.head = src_bone.head.copy()
            new_bone.tail = src_bone.tail.copy()

            # Сдвигаем по локальной оси Y на 10
            offset = src_bone.matrix.to_quaternion() @ mathutils.Vector((0, 30, 0))
            new_bone.head += offset
            new_bone.tail += offset

            # Устанавливаем длину = 1
            direction = (new_bone.tail - new_bone.head).normalized()
            new_bone.tail = new_bone.head + direction * 3.0

            # Назначаем родителя
            new_bone.parent = parent_bone
            new_bone.use_connect = False

            return ik_name

        # Создаём левые и правые кости
        left_ik = create_ik("j_clavicle_le")
        right_ik = create_ik("j_clavicle_ri")

        bpy.ops.object.mode_set(mode='POSE')

        # Функция для добавления Damped Track
        def add_damped_track(src_name, target_name):
            pose_bone = arm.pose.bones.get(src_name)
            if not pose_bone:
                print(f"Поза-кость '{src_name}' не найдена.")
                return
            # Удаляем старые Damped Track
            for c in pose_bone.constraints:
                if c.type == 'DAMPED_TRACK':
                    pose_bone.constraints.remove(c)
            # Добавляем новый
            con = pose_bone.constraints.new(type='DAMPED_TRACK')
            con.target = arm
            con.subtarget = target_name
            con.track_axis = 'TRACK_Y'

        # Добавляем констрейнты
        if left_ik:
            add_damped_track("j_clavicle_le", left_ik)
        if right_ik:
            add_damped_track("j_clavicle_ri", right_ik)

        bpy.ops.object.mode_set(mode='OBJECT')
        print("IK-кости и констрейнты успешно созданы и подключены к j_mainroot.")

else:
    print("Выдели объект-армейчер перед запуском скрипта.")

# Проверяем, что выделен объект-армейчер
obj = bpy.context.object
if obj and obj.type == 'ARMATURE':
    arm = obj
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = arm.data.edit_bones

    # Проверяем наличие базовых костей
    head_bone = edit_bones.get("j_head")
    mainroot_bone = edit_bones.get("j_mainroot")
    if not head_bone or not mainroot_bone:
        print("Не найдены кости 'j_head' или 'j_mainroot'! Создание остановлено.")
    else:
        # Функция для создания IK-кости
        def create_ik(src_name, parent_bone_name=None, hide=False):
            ik_name = src_name + "_ik"
            if src_name not in edit_bones:
                print(f"Кость '{src_name}' не найдена.")
                return None

            src_bone = edit_bones[src_name]
            new_bone = edit_bones.new(ik_name)
            new_bone.head = src_bone.head.copy()
            new_bone.tail = src_bone.tail.copy()

            # Сдвигаем по глобальной оси X на 10
            offset = mathutils.Vector((10, 0, 0))
            new_bone.head += offset
            new_bone.tail += offset

            # Устанавливаем длину = 2
            direction = (new_bone.tail - new_bone.head).normalized()
            new_bone.tail = new_bone.head + direction * 2.0

            # Назначаем родителя, если задан
            if parent_bone_name and parent_bone_name in edit_bones:
                new_bone.parent = edit_bones[parent_bone_name]
                new_bone.use_connect = False

            # Скрываем кость, если нужно
            if hide:
                new_bone.hide = True

            return ik_name

        # Создаём кость tag_eye_ik (родитель j_mainroot)
        eye_ik = create_ik("tag_eye", parent_bone_name="j_head")

        # Создаём левые и правые кости, родитель tag_eye_ik, скрытые
        left_ik = create_ik("j_eyeball_le", parent_bone_name="tag_eye_ik", hide=True)
        right_ik = create_ik("j_eyeball_ri", parent_bone_name="tag_eye_ik", hide=True)

        bpy.ops.object.mode_set(mode='POSE')

        # Функция для добавления Damped Track
        def add_damped_track(src_name, target_name):
            pose_bone = arm.pose.bones.get(src_name)
            if not pose_bone:
                print(f"Поза-кость '{src_name}' не найдена.")
                return
            # Удаляем старые Damped Track
            for c in pose_bone.constraints:
                if c.type == 'DAMPED_TRACK':
                    pose_bone.constraints.remove(c)
            # Добавляем новый
            con = pose_bone.constraints.new(type='DAMPED_TRACK')
            con.target = arm
            con.subtarget = target_name
            con.track_axis = 'TRACK_NEGATIVE_Y'

        # Добавляем констрейнты
        if left_ik:
            add_damped_track("j_eyeball_le", left_ik)
        if right_ik:
            add_damped_track("j_eyeball_ri", right_ik)

        # Скрываем кости и в Pose Mode
        for name in (left_ik, right_ik):
            if name in arm.pose.bones:
                arm.pose.bones[name].bone.hide = True

        bpy.ops.object.mode_set(mode='OBJECT')
        print("IK-кости успешно созданы:")
        print("- tag_eye_ik → родитель j_mainroot")
        print("- j_eyeball_le_ik и j_eyeball_ri_ik → родитель tag_eye_ik (скрыты)")
else:
    print("Выдели объект-армейчер перед запуском скрипта.")

    import bpy
import mathutils

# === Проверяем, что выбран объект типа Armature ===
obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise ValueError("Выдели объект арматуры перед запуском скрипта!")

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = obj.data.edit_bones

# === Настройки костей ===
source_bone_name = "j_eyeball_le"
new_bone_name = "j_eyeball_le_up"
parent_bone_name = "j_head"
offset_y = 2.0  

# === Проверяем наличие исходной кости ===
if source_bone_name not in edit_bones:
    raise ValueError(f"Кость '{source_bone_name}' не найдена в арматуре '{obj.name}'.")

src_bone = edit_bones[source_bone_name]
parent_bone = edit_bones.get(parent_bone_name)

# === Создаем новую кость ===
new_bone = edit_bones.new(new_bone_name)
new_bone.head = src_bone.head.copy()
new_bone.tail = src_bone.tail.copy()
new_bone.roll = src_bone.roll

# === Локальные оси ===
local_z = (src_bone.tail - src_bone.head).normalized()
mat = src_bone.matrix.to_3x3()
local_x = mat.col[0].normalized()
local_y = mat.col[1].normalized()

# === Смещаем по локальной оси Y ===
offset_vec = local_y * offset_y
new_bone.head += offset_vec
new_bone.tail += offset_vec

# === Подключаем новую кость к голове ===
new_bone.parent = parent_bone
new_bone.use_connect = False  # Keep Offset

# === Список костей, которые нужно подключить к j_eyeball_le_up ===
child_bones = [
    "j_eyelash_top_le_5",
    "j_eyelash_top_le_2",
    "j_eyelash_top_le",
    "j_eyelash_top_le_4",
    "j_eyelash_top_le_1",
    "j_eyelidbulge_le",
    "j_eye_lid_top_le"
]

# === Подключаем каждую кость из списка ===
for bone_name in child_bones:
    if bone_name in edit_bones:
        edit_bones[bone_name].parent = edit_bones[new_bone_name]
        edit_bones[bone_name].use_connect = False  # Keep Offset
    else:
        print(f"⚠ Кость '{bone_name}' не найдена — пропущена")

bpy.ops.object.mode_set(mode='OBJECT')

#================================================================================

import bpy
import mathutils

# === Проверяем, что выбран объект типа Armature ===
obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise ValueError("Выдели объект арматуры перед запуском скрипта!")

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = obj.data.edit_bones

# === Настройки костей ===
source_bone_name = "j_eyeball_le_up"
new_bone_name = "j_eyeball_le_low"
parent_bone_name = "j_head"
offset_y = 0  

# === Проверяем наличие исходной кости ===
if source_bone_name not in edit_bones:
    raise ValueError(f"Кость '{source_bone_name}' не найдена в арматуре '{obj.name}'.")

src_bone = edit_bones[source_bone_name]
parent_bone = edit_bones.get(parent_bone_name)

# === Создаем новую кость ===
new_bone = edit_bones.new(new_bone_name)
new_bone.head = src_bone.head.copy()
new_bone.tail = src_bone.tail.copy()
new_bone.roll = src_bone.roll

# === Локальные оси ===
local_z = (src_bone.tail - src_bone.head).normalized()
mat = src_bone.matrix.to_3x3()
local_x = mat.col[0].normalized()
local_y = mat.col[1].normalized()

# === Смещаем по локальной оси Y ===
offset_vec = local_y * offset_y
new_bone.head += offset_vec
new_bone.tail += offset_vec

# === Подключаем новую кость к голове ===
new_bone.parent = parent_bone
new_bone.use_connect = False  # Keep Offset

# === Список костей, которые нужно подключить к j_eyeball_le_up ===
child_bones = [
    "j_eyelash_bot_le_2",
    "j_eye_lid_bot_le",
    "j_eyelash_bot_le_1",
    "j_periorbital_le_1",
    "j_periorbital_le_2",
    "j_periorbital_le_3",
]

# === Подключаем каждую кость из списка ===
for bone_name in child_bones:
    if bone_name in edit_bones:
        edit_bones[bone_name].parent = edit_bones[new_bone_name]
        edit_bones[bone_name].use_connect = False  # Keep Offset
    else:
        print(f"⚠ Кость '{bone_name}' не найдена — пропущена")

bpy.ops.object.mode_set(mode='OBJECT')

#======================================================================================
# === Проверяем, что выбран объект типа Armature ===
obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise ValueError("Выдели объект арматуры перед запуском скрипта!")

# === Настройки костей ===
target_bone = "j_eyeball_le_up"   # откуда копировать поворот
owner_bone = "j_eyeball_le_low"   # на какую кость ставим констрейнт

# === Переходим в Pose Mode ===
bpy.ops.object.mode_set(mode='POSE')

pose_bones = obj.pose.bones

# === Проверяем наличие костей ===
if owner_bone not in pose_bones:
    raise ValueError(f"Кость '{owner_bone}' не найдена в арматуре '{obj.name}'!")
if target_bone not in pose_bones:
    raise ValueError(f"Кость '{target_bone}' не найдена в арматуре '{obj.name}'!")

# === Удаляем старые Copy Rotation (если есть) ===
for c in pose_bones[owner_bone].constraints:
    if c.type == 'COPY_ROTATION':
        pose_bones[owner_bone].constraints.remove(c)

# === Создаем новый констрейнт Copy Rotation ===
con = pose_bones[owner_bone].constraints.new('COPY_ROTATION')
con.name = "Copy Rotation - Eyeball Up"
con.target = obj                  # активная арматура как Target
con.subtarget = target_bone       # целевая кость

# === Настройки как на картинке ===
con.target_space = 'LOCAL'
con.owner_space = 'LOCAL'
con.mix_mode = 'AFTER'
con.invert_x = True
con.invert_y = False
con.invert_z = False
con.use_x = True
con.use_y = True
con.use_z = True
con.euler_order = 'XYZ'
con.influence = 0.7

bpy.ops.object.mode_set(mode='OBJECT')

#№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
import bpy
import mathutils

# === Проверяем, что выбран объект типа Armature ===
obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise ValueError("Выдели объект арматуры перед запуском скрипта!")

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = obj.data.edit_bones

# === Настройки костей ===
source_bone_name = "j_eyeball_ri"
new_bone_name = "j_eyeball_ri_up"
parent_bone_name = "j_head"
offset_y = 2.0  

# === Проверяем наличие исходной кости ===
if source_bone_name not in edit_bones:
    raise ValueError(f"Кость '{source_bone_name}' не найдена в арматуре '{obj.name}'.")

src_bone = edit_bones[source_bone_name]
parent_bone = edit_bones.get(parent_bone_name)

# === Создаем новую кость ===
new_bone = edit_bones.new(new_bone_name)
new_bone.head = src_bone.head.copy()
new_bone.tail = src_bone.tail.copy()
new_bone.roll = src_bone.roll

# === Локальные оси ===
local_z = (src_bone.tail - src_bone.head).normalized()
mat = src_bone.matrix.to_3x3()
local_x = mat.col[0].normalized()
local_y = mat.col[1].normalized()

# === Смещаем по локальной оси Y ===
offset_vec = local_y * offset_y
new_bone.head += offset_vec
new_bone.tail += offset_vec

# === Подключаем новую кость к голове ===
new_bone.parent = parent_bone
new_bone.use_connect = False  # Keep Offset

# === Список костей, которые нужно подключить к j_eyeball_le_up ===
child_bones = [
    "j_eyelash_top_ri_5",
    "j_eyelash_top_ri_2",
    "j_eyelash_top_ri",
    "j_eyelash_top_ri_4",
    "j_eyelash_top_ri_1",
    "j_eyelidbulge_ri",
    "j_eye_lid_top_ri"
]

# === Подключаем каждую кость из списка ===
for bone_name in child_bones:
    if bone_name in edit_bones:
        edit_bones[bone_name].parent = edit_bones[new_bone_name]
        edit_bones[bone_name].use_connect = False  # Keep Offset
    else:
        print(f"⚠ Кость '{bone_name}' не найдена — пропущена")

bpy.ops.object.mode_set(mode='OBJECT')

#================================================================================

import bpy
import mathutils

# === Проверяем, что выбран объект типа Armature ===
obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise ValueError("Выдели объект арматуры перед запуском скрипта!")

bpy.ops.object.mode_set(mode='EDIT')
edit_bones = obj.data.edit_bones

# === Настройки костей ===
source_bone_name = "j_eyeball_ri_up"
new_bone_name = "j_eyeball_ri_low"
parent_bone_name = "j_head"
offset_y = 0  

# === Проверяем наличие исходной кости ===
if source_bone_name not in edit_bones:
    raise ValueError(f"Кость '{source_bone_name}' не найдена в арматуре '{obj.name}'.")

src_bone = edit_bones[source_bone_name]
parent_bone = edit_bones.get(parent_bone_name)

# === Создаем новую кость ===
new_bone = edit_bones.new(new_bone_name)
new_bone.head = src_bone.head.copy()
new_bone.tail = src_bone.tail.copy()
new_bone.roll = src_bone.roll

# === Локальные оси ===
local_z = (src_bone.tail - src_bone.head).normalized()
mat = src_bone.matrix.to_3x3()
local_x = mat.col[0].normalized()
local_y = mat.col[1].normalized()

# === Смещаем по локальной оси Y ===
offset_vec = local_y * offset_y
new_bone.head += offset_vec
new_bone.tail += offset_vec

# === Подключаем новую кость к голове ===
new_bone.parent = parent_bone
new_bone.use_connect = False  # Keep Offset

# === Список костей, которые нужно подключить к j_eyeball_le_up ===
child_bones = [
    "j_eyelash_bot_ri_2",
    "j_eye_lid_bot_ri",
    "j_eyelash_bot_ri_1",
    "j_periorbital_ri_1",
    "j_periorbital_ri_2",
    "j_periorbital_ri_3",
]

# === Подключаем каждую кость из списка ===
for bone_name in child_bones:
    if bone_name in edit_bones:
        edit_bones[bone_name].parent = edit_bones[new_bone_name]
        edit_bones[bone_name].use_connect = False  # Keep Offset
    else:
        print(f"⚠ Кость '{bone_name}' не найдена — пропущена")

bpy.ops.object.mode_set(mode='OBJECT')

#======================================================================================
# === Проверяем, что выбран объект типа Armature ===
obj = bpy.context.active_object
if not obj or obj.type != 'ARMATURE':
    raise ValueError("Выдели объект арматуры перед запуском скрипта!")

# === Настройки костей ===
target_bone = "j_eyeball_ri_up"   # откуда копировать поворот
owner_bone = "j_eyeball_ri_low"   # на какую кость ставим констрейнт

# === Переходим в Pose Mode ===
bpy.ops.object.mode_set(mode='POSE')

pose_bones = obj.pose.bones

# === Проверяем наличие костей ===
if owner_bone not in pose_bones:
    raise ValueError(f"Кость '{owner_bone}' не найдена в арматуре '{obj.name}'!")
if target_bone not in pose_bones:
    raise ValueError(f"Кость '{target_bone}' не найдена в арматуре '{obj.name}'!")

# === Удаляем старые Copy Rotation (если есть) ===
for c in pose_bones[owner_bone].constraints:
    if c.type == 'COPY_ROTATION':
        pose_bones[owner_bone].constraints.remove(c)

# === Создаем новый констрейнт Copy Rotation ===
con = pose_bones[owner_bone].constraints.new('COPY_ROTATION')
con.name = "Copy Rotation - Eyeball Up"
con.target = obj                  # активная арматура как Target
con.subtarget = target_bone       # целевая кость

# === Настройки как на картинке ===
con.target_space = 'LOCAL'
con.owner_space = 'LOCAL'
con.mix_mode = 'AFTER'
con.invert_x = True
con.invert_y = False
con.invert_z = False
con.use_x = True
con.use_y = True
con.use_z = True
con.euler_order = 'XYZ'
con.influence = 0.7

bpy.ops.object.mode_set(mode='OBJECT')

# =============== НАБОРЫ ДЛЯ НАСТРОЙКИ ===============

configs = [
    {
        "shape": "HeelIK",
        "bones": ["HeelIK.L", "HeelIK.R"],
        "translation": (-8.2, -13.0, 0.0),
        "scale": (0.05, 1.58, 0.66),
    },
    {
        "shape": "ElbowPoleIk",
        "bones": ["ElbowPole.L", "ElbowPole.R"],
        "translation": (0, 0, 0),
        "scale": (1, 1, 1),
    },
    {
        "shape": "Ball",
        "bones": ["j_ball_ri", "j_ball_le"],
        "translation": (2.7, 17.0, 0.0),  
        "scale": (1000.0, 1000.0, 1000.0),
    },
    {
        "shape": "KneePole",
        "bones": ["KneePole.R", "KneePole.L"],
        "translation": (0, 0, 0),  
        "scale": (0.5, 0.5, 0.5),
    },
    {
        "shape": "HandIK",
        "bones": ["HandIK.L", "HandIK.R"],
        "translation": (0, 0, 0),  
        "scale": (0.7, 0.7, 0.7),
    },
    {
        "shape": "Spine",
        "bones": ["j_mainroot"],
        "translation": (0, -3, 0),  
        "scale": (200, 6000, 8000),
    },
    {
        "shape": "Spine",
        "bones": ["j_spineupper"],
        "translation": (0, -3, 0),  
        "scale": (50, 1000, 5000),
    },
    {
        "shape": "Spine",
        "bones": ["j_spinelower"],
        "translation": (0, -3, 0),  
        "scale": (50, 1000, 5000),
    },
    {
        "shape": "Spine",
        "bones": ["j_spine4"],
        "translation": (0, -3, 0),  
        "scale": (100, 2000, 6000),
    },
    {
        "shape": "WristIK",
        "bones": ["j_wrist_le_ik"],
        "translation": (0, 5.2, -2),  
        "scale": (0.7, 0.7, 0.7),
    },
    {
        "shape": "WristIK",
        "bones": ["j_wrist_ri_ik"],
        "translation": (0, 5.2, 2),  
        "scale": (0.7, 0.7, 0.7),
    },
     {
        "shape": "Wrist",
        "bones": ["j_wrist_ri"],
        "translation": (0, 2, 0),  
        "scale": (0.5, 1, 0.1),
    },
    {
        "shape": "Wrist",
        "bones": ["j_wrist_le"],
        "translation": (0, 2, 0),  
        "scale": (0.5, 1, 0.1),
    },
    {
        "shape": "Finger",
        "bones": ["j_thumb_ri_3_ik", "j_index_ri_3_ik", "j_mid_ri_3_ik", "j_ring_ri_3_ik", "j_pinky_ri_3_ik"],
        "translation": (0, 0, 0),  
        "scale": (1, 1, 1),
    },
     {
        "shape": "Finger",
        "bones": ["j_thumb_le_3_ik", "j_index_le_3_ik", "j_mid_le_3_ik", "j_ring_le_3_ik", "j_pinky_le_3_ik"],
        "translation": (0, 0, 0),  
        "scale": (1, 1, 1),
    },
    {
        "shape": "EyeIK",
        "bones": ["tag_eye_ik"],
        "translation": (0, 0, 0),  
        "scale": (0.1, 1.5, 0.5),
    },
    {
        "shape": "Eyeball",
        "bones": ["j_eyeball_ri_up", "j_eyeball_le_up"],
        "translation": (0, 0, 0),  
        "scale": (200, 200, 200),
    },
    {
        "shape": "Eye",
        "bones": ["j_eyeball_ri", "j_eyeball_le"],
        "translation": (0, -1.5, 0),  
        "scale": (200, 200, 200),
    },
    {
        "shape": "Clavicle",
        "bones": ["j_clavicle_le", "j_clavicle_ri"],
        "translation": (0, 7.2, 0),  
        "scale": (0.1, 0.5, 0.1),
    },
    {
        "shape": "ClavicleIK",
        "bones": ["j_clavicle_le_ik", "j_clavicle_ri_ik"],
        "translation": (0, 0, 0),  
        "scale": (1, 1, 1),
    },
    {
        "shape": "Head",
        "bones": ["j_head", "j_neck"],
        "translation": (0, 0, 0),  
        "scale": (500, 500, 500),
    },
]
# ====================================================

arm = bpy.context.object
if arm is None or arm.type != 'ARMATURE':
    raise Exception("Выдели арматуру перед запуском скрипта!")

bpy.ops.object.mode_set(mode='POSE')

for cfg in configs:
    shape_name = cfg["shape"]
    bones = cfg["bones"]
    translation = cfg["translation"]
    scale = cfg["scale"]

    shape_obj = bpy.data.objects.get(shape_name)
    if shape_obj is None:
        print(f"[ОШИБКА] Кастом-объект '{shape_name}' не найден, пропускаю.")
        continue

    for name in bones:
        pbone = arm.pose.bones.get(name)
        if not pbone:
            print(f"[ОШИБКА] Кость '{name}' не найдена, пропускаю.")
            continue

        pbone.custom_shape = shape_obj
        pbone.custom_shape_translation = translation
        pbone.custom_shape_scale_xyz = scale


#===========================BONE BINDING=======================================

# Список костей, которые должны остаться видимыми
visible_bones = {
    "HeelIK.L", "HeelIK.R",
    "ElbowPole.L", "ElbowPole.R",
    "j_ball_ri", "j_ball_le",
    "KneePole.R", "KneePole.L",
    "HandIK.L", "HandIK.R",
    "j_mainroot", "j_spineupper", "j_spinelower", "j_spine4",
    "j_wrist_le_ik", "j_wrist_ri_ik", "j_wrist_ri", "j_wrist_le",
    "j_thumb_ri_3_ik", "j_index_ri_3_ik", "j_mid_ri_3_ik", "j_ring_ri_3_ik", "j_pinky_ri_3_ik",
    "j_thumb_le_3_ik", "j_index_le_3_ik", "j_mid_le_3_ik", "j_ring_le_3_ik", "j_pinky_le_3_ik",
    "tag_eye_ik",
    "j_eyeball_le_up", "j_eyeball_ri_up",
    "j_eyeball_le", "j_eyeball_ri",
    "j_clavicle_ri", "j_clavicle_le",
    "j_clavicle_ri_ik", "j_clavicle_le_ik",
    "j_neck", "j_head"
}

# Получаем активную арматуру
arm = bpy.context.object

if arm is None or arm.type != 'ARMATURE':
    raise Exception("Активный объект должен быть арматурой!")

# Работаем с поза-костями, если они есть, иначе ― с обычными костями
bpy.ops.object.mode_set(mode='POSE')
for pb in arm.pose.bones:
    pb.hide = pb.name not in visible_bones

print("Готово: ненужные кости скрыты.")
