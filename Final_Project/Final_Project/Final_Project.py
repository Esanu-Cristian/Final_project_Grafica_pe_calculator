from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import distance
from ursina.shaders import lit_with_shadows_shader
from ursina.lights import PointLight
import math


def is_near(entity, target, max_dist=2.8):
    return distance(entity.position, target.position) < max_dist

app = Ursina()

# jucatorul
player = FirstPersonController(position=(10,1,5))

player_light = PointLight(
    parent=player,
    color=color.white,
    y=1,
    z=0
)

player.disable() #pentru a afisa meniul start mai intai

# gravitatea
player.gravity = 1

# meniu
menu_bg = Entity(
    model='quad',
    parent=camera.ui,
    scale=(2,1.2),
    color=color.rgba(0,0,0,1),
    z=1,
    enabled=True
)
menu_title = Text(
    text='Instructions:\n\n-Collect the red artifacts by pressing "E" near them\n\n-After this a red button near the gate will appear,\npress it to open the gate\n\n-Do not let the green virus touch you, otherwise you will lose\n\n-Get to the green platform to win',
    origin=(0,0),
    scale=2,
    y=0.2,
    color=color.azure,
    enabled=True
)
start_button = Button(
    text='Start Game',
    color=color.blue,
    scale=(0.3, 0.1),
    position=(0, -0.2),
    enabled=True
)


def start_game():
    global player
    menu_title.enabled = False
    start_button.enabled = False
    menu_bg.enabled = False
    player.enable()

start_button.on_click = start_game

cube1d = False
cube2d = False
cube3d = False
cube4d = False
cube5d = False
cube6d = False

# skybox
Sky()

# lumina directionala
ambient_light = AmbientLight(color=color.rgba(20, 20, 20, 0.1))
directional_light = DirectionalLight(shadows=True)
directional_light.look_at(Vec3(1 ,1, -1))
window.bloom = True


# podea camera
ground1 = Entity(
      model='plane',
      texture='floor.jpg',
      scale=(40, 1, 25),
      position=(5, -1, -2.5),
      collider='box'
)

# tavan
ceiling1 = Entity(
    model='cube',
    color=color.gray,
    texture='ceiling.jpg',
    scale=(40, 0.1, 25),
    position=(5, 4, -2.5),
    collider='box'
)

# podea afara
ground2 = Entity(
      model='plane',
      texture='grass',
      scale=(15, 1, 30),
      position=(5, -1, 25),
      collider='box'
)


# copaci DOAR de-a lungul lui ground2
tree_model = 'tree/tree1_3ds/Tree1.3ds'
tree_scale = 0.3
tree_spacing = 3
tree_y = -1

# dimensiuni ground2
g2_x, g2_y, g2_z = ground2.scale
g2_cx, g2_cy, g2_cz = ground2.position

# calculeaza marginile
min_x = g2_cx - g2_x/2
max_x = g2_cx + g2_x/2
min_z = g2_cz - g2_z/2
max_z = g2_cz + g2_z/2


# marginea est (dreapta)
for z in range(int(min_z)+2, int(max_z)+1, tree_spacing):
    Entity(model=tree_model, position=(max_x-1, tree_y, z), scale=tree_scale, collider='box')
# marginea vest (stanga)
for z in range(int(min_z)+2, int(max_z)+1, tree_spacing):
    Entity(model=tree_model, position=(min_x+1, tree_y, z), scale=tree_scale, collider='box')


# perete cu poarta 
wall_length = 40
wall_height = 5
wall_thickness = 0.3
wall_y = 1.5

# perete stanga
wall_left = Entity(
    model='cube',
    color=color.gray,
    texture='wall.jpg',
    scale=(wall_length/2 - 2, wall_height, wall_thickness),
    position=(5 - wall_length/4 - 1, wall_y, 10),
    collider='box'
)
# perete dreapta
wall_right = Entity(
    model='cube',
    color=color.gray,
    texture='wall.jpg',
    scale=(wall_length/2 - 2, wall_height, wall_thickness),
    position=(5 + wall_length/4 + 1, wall_y, 10),
    collider='box'
)
# poarta (initial inchisa)
gate = Entity(
    model='cube',
    texture='gate.jpg',
    scale=(4, wall_height, 0.2),
    position=(5, wall_y, 9.75),
    collider='box'
)
gate_open = False
gate_initial_pos = gate.position




# pereti la marginea planului
wall_thickness = 0.5
wall_height = 5
ground_size = 40

# perete sud (spate)
wall_south = Entity(
    model='cube',
    scale=(ground_size, wall_height, wall_thickness),
    position=(5, 1.5, 5 - ground_size/2),
    color=color.gray,
    texture='wall.jpg',
    collider='box'
)
# perete est (stanga)
wall_east = Entity(
    model='cube',
    scale=(wall_thickness, wall_height, 25),
    position=(5 + ground_size/2, 1.5, -2.5),
    color=color.gray, 
    texture='wall.jpg',
    collider='box'
)
# perete vest (dreapta)
wall_west = Entity(
    model='cube',
    scale=(wall_thickness, wall_height, 25),
    position=(5 - ground_size/2, 1.5, -2.5),
    color=color.gray,
    texture='wall.jpg',
    collider='box'
)


#baza pe care sta butonul
base = Entity(model='cube', texture='white_cube', position=(8,-0.25,9), scale=(0.6,1.5,0.6), color=color.gray, collider='box')

# butonul rosu
button_red = Entity(
    model='cube',
    color=color.red,
    position=(8, 0.55, 9),
    scale=(0.5, 0.1, 0.5),
    collider='box'
)
button_red_initial_pos = button_red.position

#initial ascuns (butonul)
base.disable()
button_red.disable()

#deschiderea portii
def on_button_red_click():
    global gate_open, chaser_touch
    if not gate_open and is_near(player, button_red, max_dist=5):
        button_red.animate_position(button_red.position + Vec3(0, -0.2, 0), duration=0.1)
        invoke(lambda: button_red.animate_position(button_red_initial_pos, duration=0.1), delay=0.1)
        gate.animate_position(gate_initial_pos + Vec3(4,0,0), duration=1)
        gate_open = True
        chaser_touch = False

button_red.on_click = on_button_red_click



# chaser
chaser = Entity(model='sphere',texture='chaser.jpg', position=(4,0,14), scale=2, collider='box')
chaser_touch = True
chaser_old_z = chaser.z



# colectabile semistatice
cube1 = Entity(model='cube', texture='bonus.jpg', position=(-8,0.15,-2), scale=(1,1,1), color=color.rgba(255, 50, 50, 200), collider='box', shader=lit_with_shadows_shader)
cube2 = Entity(model='cube', texture='bonus.jpg', position=(10,0.15,0), scale=(1,1,1), color=color.rgba(255, 50, 50, 200), collider='box', shader=lit_with_shadows_shader)
cube3 = Entity(model='cube', texture='bonus.jpg', position=(20,0.15,5), scale=(1,1,1), color=color.rgba(255, 50, 50, 200), collider='box', shader=lit_with_shadows_shader)
cube4 = Entity(model='cube', texture='bonus.jpg', position=(-3,0.15,-7), scale=(1,1,1), color=color.rgba(255, 50, 50, 200), collider='box', shader=lit_with_shadows_shader)
cube5 = Entity(model='cube', texture='bonus.jpg', position=(5,0.15,-6), scale=(1,1,1), color=color.rgba(255, 50, 50, 200), collider='box', shader=lit_with_shadows_shader)
cube6 = Entity(model='cube', texture='bonus.jpg', position=(15,0.15,-4), scale=(1,1,1), color=color.rgba(255, 50, 50, 200), collider='box', shader=lit_with_shadows_shader)

cube1_base_y = cube1.y
cube2_base_y = cube2.y
cube3_base_y = cube3.y
cube4_base_y = cube4.y
cube5_base_y = cube5.y
cube6_base_y = cube6.y


def update():
    global ambient_light, gate_open, chaser_touch, chaser_old_z, cube1d, cube2d, cube3d, cube4d, cube5d, cube6d

    # plutire cuburi
    float_speed = 2
    float_amplitude = 0.3

    if not cube1d:
        cube1.y = cube1_base_y + math.sin(time.time() * float_speed) * float_amplitude
    if not cube2d:
        cube2.y = cube2_base_y + math.sin(time.time() * float_speed + 1) * float_amplitude
    if not cube3d:
        cube3.y = cube3_base_y + math.sin(time.time() * float_speed + 2) * float_amplitude
    if not cube4d:
        cube4.y = cube4_base_y + math.sin(time.time() * float_speed + 3) * float_amplitude
    if not cube5d:
        cube5.y = cube5_base_y + math.sin(time.time() * float_speed + 4) * float_amplitude
    if not cube6d:
        cube6.y = cube6_base_y + math.sin(time.time() * float_speed + 5) * float_amplitude


    # se inchide poarta cand jucatorul se indeparteaza de buton
    if gate_open and not is_near(player, button_red, max_dist=6):
        gate.animate_position(gate_initial_pos, duration=1)
        gate_open = False

    # calculeaza directia spre player DOAR pe X si Z (Y ramane constant, adica sus/jos)
    if chaser_touch == False:
       chaser_old_z = chaser.z
       target_pos = Vec3(player.position.x, chaser.position.y, player.position.z)
       direction = (target_pos - chaser.position).normalized()
       next_position = chaser.position + direction * time.dt * 2.5
       chaser.position = Vec3(next_position.x, chaser.position.y, next_position.z)
       # fata la chaser mereu se intoarce spre jucator
       chaser.look_at(player.position)
       chaser.rotation_x = 0
       chaser.rotation_z = 0

    # daca chaser se atinge de player, atunci se opreste
    if distance(player.position, chaser.position) < 1.5:
        chaser_touch = True

    # verificare trecere prag Oz=8.75
    if ((chaser_old_z < 8.75 and chaser.position.z >= 8.75) and gate_open==False) or ((chaser_old_z < 8.75 and chaser.position.z >= 8.75) and (chaser.position.x<3 or chaser.position.x>7 )):
        chaser_touch = True

    # se activeaza butonul dupa colectarea artefactelor
    if cube1d==True and cube2d==True and cube3d==True and cube4d==True and cube5d==True and cube6d==True:
        base.enable()
        button_red.enable()

    # daca player cade in gol sau se atinge de chaser, atunci joaca se opreste
    if distance(player.position, chaser.position) < 1.5 or player.position.y<=-10 :
        game_over_text.enabled = True
        player.enabled = False
        ambient_light.color = color.rgba(255, 0, 0, 0.8)
        try_again_button.enabled = True
        chaser_touch = True    # pentru ca chaser sa se opreasca

        # daca jucatorul ajunge pe platforma finala, opreste jocul si afiseaza mesajul
    if distance(player.position, final_platform.position) < 2:
        player.enabled = False
        you_won_text.enabled = True
        chaser_touch = True    #pentru ca chaser sa se opreasca



# platforme de sarit
platform_scale = (2, 0.3, 2)
platform_y = 0
start_x = 5
start_z = 40


for i in range(6):
    offset_x = (-2 if i % 2 == 0 else 2)
    x = start_x + offset_x
    z = start_z + i * 2
    Entity(
        model='cube',
        color=color.azure,
        texture='white_cube',
        scale=platform_scale,
        position=(x, platform_y, z),
        collider='box'
    )

# platforma finala
final_platform = Entity(
    model='cube',
    color=color.green,
    texture='white_cube',
    scale=(6, 0.5, 6),
    position=(5, platform_y, start_z + 6 * 2 + 2),
    collider='box'
)


you_won_text = Text(
    text='You Won the game!',
    origin=(0,0),
    scale=5,
    color=color.blue,
    enabled=False
)


game_over_text = Text(
    text='GAME OVER',
    origin=(0,0),
    scale=5,
    color=color.red,
    enabled=False
)

try_again_button = Button(
    text='Try Again',
    color=color.gray,
    scale=(0.3, 0.1),
    position=(0, -0.15),
    enabled=False
)

def reset_game():
    global cube1d, cube2d, cube3d, cube4d, cube5d, cube6d, chaser_touch, gate_open

    # resetare player
    player.position = (10, 1, 5)
    player.enabled = True

    # resetare chaser
    chaser.position = (4, 0, 12)
    chaser_touch = True

    # resetare artefacte colectabile
    for cube, base_y in [
        (cube1, cube1_base_y), (cube2, cube2_base_y), (cube3, cube3_base_y),
        (cube4, cube4_base_y), (cube5, cube5_base_y), (cube6, cube6_base_y)
    ]:
        cube.enable()
        cube.y = base_y

    cube1d = cube2d = cube3d = cube4d = cube5d = cube6d = False

    # dezactivare buton si baza
    base.disable()
    button_red.disable()

    # resetare poarta
    gate.position = gate_initial_pos
    gate_open = False

    # ascundere text si buton
    game_over_text.enabled = False
    try_again_button.enabled = False

    # resetare lumina ambientala
    ambient_light.color = color.rgba(20, 20, 20, 0.1)


try_again_button.on_click = reset_game


def input(key):
    global cube1d, cube2d, cube3d, cube4d, cube5d, cube6d
    if key == 'escape':
        application.quit()
    if key == 'e':
        if is_near(player, cube1):
            cube1.disable()
            cube1d = True
        elif is_near(player, cube2):
            cube2.disable()
            cube2d = True
        elif is_near(player, cube3):
            cube3.disable()
            cube3d = True
        elif is_near(player, cube4):
            cube4.disable()
            cube4d = True
        elif is_near(player, cube5):
            cube5.disable()
            cube5d = True
        elif is_near(player, cube6):
            cube6.disable()
            cube6d = True


app.run()
