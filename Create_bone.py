import bpy

# Имя коллекции
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
