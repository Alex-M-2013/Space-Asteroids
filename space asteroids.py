from ursina import *
from random import randint

app = Ursina()

window.exit_button.disable()
window.collider_counter.disable()
window.entity_counter.disable()
window.fps_counter.disable()
window.cog_button.disable()

camera.orthographic = True
camera.fov = 12
camera.position = (0, 0)

score = 0

score_display = Text(
    text=f"Score: {int(score)}",
    z=0.1,
    y=0.428,
    scale=2,
    origin=(0,0),
    color=color.white,
    x=-0.75,
)

background = Entity(
    model="quad",
    scale=(30,15),
    texture="assets/bg.png",
    z=0.1
)

background2 = Entity(
    model="quad",
    scale=(30,15),
    texture="assets/bg.png",
    x=30,
    z=0.1
)

player = Entity(
    model='quad',
    texture='assets/rocket.png',
    scale=(1.6, 1.6), 
    z=-0.3,
)
player.collider = BoxCollider(player, size=Vec3(0.75, 0.75, 0.75))

left_wall = Entity(
    model='quad',
    scale=(1, 12),
    x=-11.2,
    z=-0.29
)
left_wall.collider = BoxCollider(left_wall)

right_wall = Entity(
    model='quad',
    scale=(1, 12),
    x=11.2,
    z=-0.29
)
right_wall.collider = BoxCollider(right_wall)

game_started = False

score_display.disable()
background.disable()
background2.disable()
player.disable()
left_wall.disable()
right_wall.disable()


main_menu = Text(
    text="Main Menu",
    color=color.white,
    scale=4,
    origin=(0,0),
    x=0,
    y=0.3,
    z=0.1,
)

start_button = Button(
    text="Start",
    color=color.dark_gray,
    text_size=4,
    x=0,
    y=0.03,
    z=0.1,
    scale=(0.25, 0.1),
)


def start_game():
    global game_started
    
    score_display.enable()
    background.enable()
    background2.enable()
    player.enable()
    left_wall.enable()
    right_wall.enable()

    main_menu.disable()
    start_button.disable()

    game_started = True
    spawn_asteroids()

start_button.on_click = (start_game)

asteroids = []

def spawn_asteroids():
    global asteroids, game_over, game_started


    if game_over or not game_started:
        return

    y_pos = randint(-5, 5)
     
    asteroid = Entity(
        model='quad',
        color=color.white,
        scale=(2.5, 2.5),
        position=Vec3(20, y_pos, -0.2),
        texture='assets/asteroid.png',
    )
    
    asteroid.collider = BoxCollider(asteroid, size=Vec3(0.4, 0.3, 0.4))

    asteroids.append(asteroid)
    
    invoke(spawn_asteroids, delay=2)     

game_over = False

death_text = Text(
    text='GAME OVER',
    color=color.white,
    origin=(0,0),
    y=0.2,
    scale=5,
    z=-0.5,
)

retry_button = Button(
    text='Retry',
    text_size=5,
    y=-0.1,
    scale=8,
)

death_text.disable()
retry_button.disable()

def reset_game():
    global asteroid_spawn_delay, asteroids, game_over, score

    for asteroid in asteroids:
        destroy(asteroid)

    asteroids.clear()
    asteroid_spawn_delay = 1

    player.x = 0
    player.y = 0

    death_text.disable()
    retry_button.disable()

    score = 0
    score_display.enable()
    score_display.text = f"Score: {int(score)}"

    game_over = False
    spawn_asteroids()

retry_button.on_click = (reset_game)

def show_death_screen():
    
    score_display.disable()

    death_text.enable()
    retry_button.enable()

def update():
    global game_over, game_started, score

    if game_over or not game_started:
        return

    score += 15 * time.dt
    score_display.text = f"Score: {int(score)}"

    background.x -= 1 * time.dt
    background2.x -= 1* time.dt
    
    if background.x < -30:
        background.x += 60
    
    if background2.x < -30:
        background2.x += 60
    
    if held_keys['up arrow'] or held_keys['w']:
        player.y += 15 * time.dt
    elif held_keys['down arrow'] or held_keys['s']:
        player.y -= 15 * time.dt
    elif held_keys ['left arrow'] or held_keys['a']:
        player.x -= 15 * time.dt
    elif held_keys ['right arrow'] or held_keys['d']:
        player.x += 15 * time.dt

    if player.intersects(left_wall).hit:
        player.x += 15 * time.dt
    elif player.intersects(right_wall).hit:
        player.x -= 15 * time.dt

    if player.y > 6:
        player.y = -6
    elif player.y < -6:
        player.y = 6

    for asteroid in asteroids:
        asteroid.x -= 1.5 * time.dt
        
        if player.intersects(asteroid).hit:
            game_over = True
            show_death_screen()
            break

        if asteroid.intersects(left_wall).hit:
            destroy(asteroid)
            asteroids.remove(asteroid)
            
spawn_asteroids()

app.run()