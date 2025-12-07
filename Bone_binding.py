import bpy

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
        "scale": (0.1, 0.1, 0.1),
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
        "scale": (30, 700, 1000),
    },
    {
        "shape": "Spine",
        "bones": ["j_spineupper"],
        "translation": (0, -3, 0),  
        "scale": (5, 100, 500),
    },
    {
        "shape": "Spine",
        "bones": ["j_spinelower"],
        "translation": (0, -3, 0),  
        "scale": (5, 100, 500),
    },
    {
        "shape": "Spine",
        "bones": ["j_spine4"],
        "translation": (0, -3, 0),  
        "scale": (10, 200, 600),
    },
    {
        "shape": "WristIK",
        "bones": ["j_wrist_le_ik"],
        "translation": (0, 5.2, -2),  
        "scale": (0.07, 0.07, 0.07),
    },
    {
        "shape": "WristIK",
        "bones": ["j_wrist_ri_ik"],
        "translation": (0, 5.2, 2),  
        "scale": (0.07, 0.07, 0.07),
    },
     {
        "shape": "Wrist",
        "bones": ["j_wrist_ri"],
        "translation": (0, 2, 0),  
        "scale": (0.05, 0.1, 0.01),
    },
    {
        "shape": "Wrist",
        "bones": ["j_wrist_le"],
        "translation": (0, 2, 0),  
        "scale": (0.05, 0.1, 0.01),
    },
    {
        "shape": "Finger",
        "bones": ["j_thumb_ri_3_ik", "j_index_ri_3_ik", "j_mid_ri_3_ik", "j_ring_ri_3_ik", "j_pinky_ri_3_ik"],
        "translation": (0, 0, 0),  
        "scale": (0.1, 0.1, 0.1),
    },
     {
        "shape": "Finger",
        "bones": ["j_thumb_le_3_ik", "j_index_le_3_ik", "j_mid_le_3_ik", "j_ring_le_3_ik", "j_pinky_le_3_ik"],
        "translation": (0, 0, 0),  
        "scale": (0.1, 0.1, 0.1),
    },
    {
        "shape": "EyeIK",
        "bones": ["tag_eye_ik"],
        "translation": (0, 0, 0),  
        "scale": (0.01, 0.15, 0.05),
    },
    {
        "shape": "Eyeball",
        "bones": ["j_eyeball_ri_up", "j_eyeball_le_up"],
        "translation": (0, 0, 0),  
        "scale": (50, 50, 50),
    },
    {
        "shape": "Eye",
        "bones": ["j_eyeball_ri", "j_eyeball_le"],
        "translation": (0, -1.5, 0),  
        "scale": (30, 30, 30),
    },
    {
        "shape": "Clavicle",
        "bones": ["j_clavicle_le", "j_clavicle_ri"],
        "translation": (0, 7.2, 0),  
        "scale": (0.01, 0.05, 0.01),
    },
    {
        "shape": "ClavicleIK",
        "bones": ["j_clavicle_le_ik", "j_clavicle_ri_ik"],
        "translation": (0, 0, 0),  
        "scale": (0.1, 0.1, 0.1),
    },
    {
        "shape": "Head",
        "bones": ["j_head", "j_neck"],
        "translation": (0, 0, 0),  
        "scale": (50, 50, 50),
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


#==================================================================

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
bones = arm.data.bones

for b in bones:
    if b.name not in visible_bones:
        b.hide = True
    else:
        b.hide = False

print("Готово: ненужные кости скрыты.")
