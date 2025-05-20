import pygame, os, random
from pygame.locals import *
from sys import exit
from map_loader import Map
from timers import Timer
import math

WIDTH, HEIGHT = RESOLUTION = 350, 350
FPS = 30

print("Initializing Pygame...")
screen = pygame.display.set_mode(RESOLUTION, flags=pygame.SCALED | pygame.RESIZABLE | pygame.DOUBLEBUF)
display = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Banjo Rollout, A Short Trip in Australia")
pygame.display.set_icon(pygame.image.load("Assets/banjo/idle1.png"))

retrofont = pygame.font.Font('Fonts/retroville.ttf', 20)
retrofontmedium = pygame.font.Font('Fonts/retroville.ttf', 16)
retrofontsmall = pygame.font.Font('Fonts/retroville.ttf', 12)

jump_sfx = pygame.mixer.Sound("Sound/sfx/jump.wav")
slide_sfx = pygame.mixer.Sound("Sound/sfx/slide.wav")
stomp_sfx = pygame.mixer.Sound("Sound/sfx/stomp.wav")
climb_sfx = pygame.mixer.Sound("Sound/sfx/climb.wav")
spike_sfx = pygame.mixer.Sound("Sound/sfx/spike.wav")
start_sfx = pygame.mixer.Sound("Sound/sfx/start.wav")

logo_surf = pygame.image.load("Assets/logo.png").convert_alpha()
palm_tree_surf = pygame.image.load("Assets/palm tree.png").convert_alpha()
gdr_surf = pygame.image.load("Assets/great dividing range.png").convert_alpha()
clouds_surf = pygame.image.load("Assets/clouds.png").convert_alpha()
jc_surf = pygame.image.load("Assets/jenolan caves.png").convert_alpha()
speleothems_surf = pygame.image.load("Assets/speleothems.png").convert_alpha()
gdr2_surf = pygame.image.load("Assets/great dividing range 2.png").convert_alpha()


def maxint(int, max):
  if int > max: return max
  else: return int

def minint(int, min):
  if int < min: return min
  else: return int

def betweenint(int, min, max, only_for_max=False, only_for_min=False):
  if int: determined_int = 0
  else: determined_int = -1
  while (not ((int >= min or only_for_min) and (int <= max or only_for_max))) and determined_int != int:
    determined_int = int
    if int > max and not only_for_max: int = max - (int - min)
    if int < min and not only_for_min: int = max + (int - min)
  return int

def betweenint_nobacktrack(int, min, max, only_for_max=False, only_for_min=False):
  if int: determined_int = 0
  else: determined_int = -1
  while (not ((int >= min or only_for_min) and (int <= max or only_for_max))) and determined_int != int:
    determined_int = int
    if int > max and not only_for_max: int = min - (int - min)
    if int < min and not only_for_min: int = min + (int - min)
  return int

def snapint(int, snap_to): return round(int / snap_to) * snap_to

def resetint(int, down_to):
  while int > down_to: int -= down_to
  return int



class Main:
  def __init__(self):
    print("Running Game...")
    self.reset()

  def reset(self):
    self.gamestate = 0
    self.started = False
    self.timer = Timer()
    self.clouds_timer = Timer()
    self.droplet_timer = Timer()
    self.stalagtite_timer = Timer()
    self.gameover_timer = Timer()
    self.ending_timer = Timer()
    pygame.mixer_music.load("Sound/tracks/Lone Jungle.mp3")
    pygame.mixer_music.play(-1, 0.0)
    self.player = Player(150, 250)
    self.scroll = [0, 0]
    self.shake = [0, 0]
    self.droplets = []
    self.stalagtites = []
    self.map = "Great Dividing Range"
    self.vines = []
    self.animals = {"dingo": [], "python": [], "eagle": []}
    self.world = Map({}, os.listdir("Assets/tiles"), self)
    self.world_data = self.world.load_map(self.map)
    self.ending = False
    #pygame.mixer_music.set_volume(0)#oh ok

  def update(self):
    if self.gamestate == 0: self.menu()
    elif self.gamestate == 1: self.gameplay()
    elif self.gamestate == 2: self.gameover()
    #print(self.scroll[0], self.player.rect.x)
    run()
    
  def menu(self):
    display.blit(logo_surf, (0, 0 - (self.timer.tally * 2.25)))
    display.blit(retrofontmedium.render("Game by Tunari", False, "White"), ((WIDTH / 2) - (retrofontmedium.render("Game by Tunari", False, "White").get_width() / 2), 0 - (self.timer.tally * 2.25)))
    display.blit(retrofontmedium.render("Press START Button", False, "White"), ((WIDTH / 2) - (retrofontmedium.render("Press START Button", False, "White").get_width() / 2), (HEIGHT - 25) - (self.timer.tally * 2.25)))
    if get_buttons("start"): self.started = True
    if self.started: self.timer.nonstopcount(1, 0)
    if self.timer.tally * 5 > HEIGHT: self.start_game()

  def start_game(self): self.gamestate = 1; start_sfx.play(); self.load_map("Great Dividing Range")

  def load_map(self, map, player_x_spawn=150, player_y_spawn=250):
    self.world = Map({}, os.listdir("Assets/tiles"), self); self.world_data = self.world.load_map(map); self.map = map; self.player = Player(player_x_spawn, player_y_spawn); self.scroll = [0, 0]; self.stalagtites.clear(); self.animals["dingo"].clear(); self.animals["python"].clear(); self.animals["eagle"].clear()
    try: pygame.mixer_music.load("Sound/tracks/" + map + ".mp3"); pygame.mixer_music.play(-1, 0.0)
    except: pygame.mixer_music.load("Sound/tracks/Great Dividing Range.mp3"); pygame.mixer_music.play(-1, 0.0)

  def gameplay(self):
    if self.map == "Great Dividing Range":
      display.fill((100, 120, 200))
      self.clouds_timer.keep_count(1, 525, 0)
      for x in range(10):
        display.blit(gdr_surf, ((x * 525) - (self.scroll[0] / 30), 0))
      for x in range(10):
        display.blit(clouds_surf, ((x * 525) - (self.scroll[0] / 25) - self.clouds_timer.tally, 0))
      for x in range(10):
        display.blit(palm_tree_surf, ((x * WIDTH) - (self.scroll[0] / 3), 0))

        
    if self.map == "Great Dividing Range 2":
      display.fill((200, 120, 100))
      self.clouds_timer.keep_count(2, 525, 0)
      for x in range(10):
        display.blit(gdr2_surf, ((x * 525) - (self.scroll[0] / 30), 0))
      for x in range(10):
        display.blit(clouds_surf, ((x * 525) - (self.scroll[0] / 25) - self.clouds_timer.tally, 0))
      for x in range(10):
        display.blit(palm_tree_surf, ((x * WIDTH) - (self.scroll[0] / 3), 0))

    if self.map == "Jenolan Caves":
      display.fill((40, 50, 25))
      for x in range(10):
        display.blit(jc_surf, ((x * 525) - (self.scroll[0] / 10), 0))
      for x in range(10):
        display.blit(speleothems_surf, ((x * WIDTH) - (self.scroll[0] / 5), 0))
      for droplet in self.droplets:
        droplet.update()
        if droplet.rect.y > HEIGHT: self.droplets.remove(droplet)
      if self.droplet_timer.timer(FPS * 4): self.droplets.append(Droplet())

    self.world.tiles(self.world_data, Enemy, display, self.scroll)

    if self.map == "Jenolan Caves":
      for stalagtite in self.stalagtites: stalagtite.update()
      for stalagtite in self.stalagtites:
        if stalagtite.rect.y > HEIGHT: self.stalagtites.remove(stalagtite)
      if self.stalagtite_timer.timer((FPS * 4) - (self.player.rect.x / 100)): self.stalagtites.append(Stalagtite())
      if self.player.rect.x > 7850: self.load_map("Great Dividing Range 2")
      if self.scroll[0] > 7500: self.scroll[0] = 7500

    if self.map == "Great Dividing Range":
      if self.player.rect.x > 4350: self.load_map("Jenolan Caves")
      if self.scroll[0] > 4000: self.scroll[0] = 4000

    if self.map == "Great Dividing Range 2":
      if self.player.rect.x > 11725: self.scroll[0] = 11650; self.ending = True; self.player.movement = [0, 0]
      if self.ending:
        self.ending_timer.nonstopcount(1, 0)
        if self.ending_timer.tally < FPS: pygame.mixer_music.stop(); display.blit(retrofont.render("You Win!", False, "White"), ((WIDTH / 2) - (retrofont.render("You Win!", False, "White").get_width() / 2), 50))
        if self.ending_timer.tally == FPS: pygame.mixer_music.load("Sound/tracks/Homecoming.mp3"); pygame.mixer_music.play(1, 0.0)
        if self.ending_timer.tally > FPS:
          self.player.state = "win"; self.player.frame = self.player.timer.keep_count(4, 37, 1); display.blit(retrofont.render("Congratulations!", False, "White"), ((WIDTH / 2) - (retrofont.render("Congratulations!", False, "White").get_width() / 2), 50))
          if self.ending_timer.tally > FPS * 20 and not pygame.mixer_music.get_busy(): self.reset()


    for name in self.animals:
      for entity in self.animals[name]:
        entity.update()
  
    self.player.update()

    if get_buttons("back"): self.reset()

  def gameover(self):
    display.blit(retrofont.render("You Lost", False, "White"), ((WIDTH / 2) - (retrofont.render("You Lost", False, "White").get_width() / 2), 50))
    display.blit(retrofontmedium.render("START to give it another go", False, "White"), ((WIDTH / 2) - (retrofontmedium.render("START to give it another go", False, "White").get_width() / 2), 150))
    if get_buttons("a") or get_buttons("start"): self.reset(); self.start_game()
    if get_buttons("back"): self.reset()





class Player:
  def __init__(self, x, y):
    self.rect = pygame.Rect((x, y), (17, 25))
    self.state = "idle"
    self.frame = 1
    self.movement = [0, 0] #the movement of player vector speed
    self.vertical_power = -6
    self.horizontal_power = 10
    self.wall_sliding = False
    self.vine_climbing = False
    self.friction = 0.2
    self.x_momentum = 0 #speed verticle
    self.y_momentum = 0 #speed verticle
    self.air_timer = 0 #sees how much time spent in air (for jumping purposes)
    self.jump_force = -6
    self.speed = 4
    self.jumps = 0
    self.ready_jump = False
    self.hit = False
    self.mid_air = False
    self.collision_type = {"top": False, "bottom": False, "right": False, "left": False}
    self.lobster_timer = 0
    self.flipped = False
    self.timer = Timer()
    self.started_walking = False
    self.attack_angle = "down"
    self.alive = True

  def collision_test(self, tiles):#let's do jumping
      self.hit_list = []
      for tile in tiles:
        if self.rect.colliderect(tile): self.hit_list.append(tile)
      return self.hit_list
  
  def update(self):
    try: self.image = pygame.transform.flip(pygame.image.load("Assets/banjo/" + self.state + str(self.frame) + ".png").convert_alpha(), self.flipped, False)
    except: self.image = pygame.transform.flip(pygame.image.load("Assets/banjo/idle1.png").convert_alpha(), self.flipped, False)
    display.blit(self.image, (self.rect.x - main.scroll[0] - 4, self.rect.y - main.scroll[1]))
    
    if self.rect.x - main.scroll[0] > (250 * 0.75): main.scroll[0] += 4
    if self.rect.x - main.scroll[0] < (100 * 0.75): main.scroll[0] -= 4
    #if self.rect.y - main.scroll[1] > (250 * 0.75): main.scroll[1] += 5
    #if self.rect.y - main.scroll[1] < (100 * 0.75): main.scroll[1] -= 5

    if self.alive: tiles = main.world.tile_rect
    else: tiles = []
    self.collision_type, self.rect = self.move(tiles)
    if self.alive and not main.ending: self.control()
    
    if not self.vine_climbing: self.gravity()


    #Things Banjo is vulnerable to! ↓
    dead = False
    if self.rect.y > HEIGHT + main.scroll[1]: dead = True
    for stalagtite in main.stalagtites:
      if self.rect.colliderect(stalagtite.rect): dead = True
    if self.alive: main.stalagtites = [stalagtite for stalagtite in main.stalagtites if not self.rect.colliderect(stalagtite.rect)]


    if self.y_momentum >= 8 and not self.alive: main.gamestate = 2
    if dead and self.alive: self.alive = False; self.timer.reset(); pygame.mixer_music.stop(); self.x_momentum = 0; self.y_momentum = 0; self.timer.reset(); self.frame = 1
    if not self.alive:
      self.state = "defeat"; self.movement[0] = 0; main.gameover_timer.nonstopcount(1, 0); self.wall_sliding = False; self.vine_climbing = False
      if main.gameover_timer.tally < FPS // 2: self.movement[1] = 0
      elif main.gameover_timer.tally == FPS // 2: self.y_momentum = self.vertical_power * 1.5; pygame.mixer_music.load("Sound/tracks/Game Over.mp3"); pygame.mixer_music.play(1, 0.0)
      else: self.frame = self.timer.keep_count(2, 3, 1)

    elif self.state != "attack" and not self.collision_type["bottom"]: self.state = "jump"; self.frame = maxint(self.timer.count(4, 2, 1), 2); self.started_walking = False
    if self.alive and self.state != "attack" and not main.ending: self.wall_slide(); self.vine_climb()

    if self.state == "attack":
      self.movement[1] = 10
      for animal in ["dingo", "python", "eagle"]:
        for enemy in main.animals[animal]:
          if self.rect.colliderect(enemy.rect): enemy.alive = False
      if self.attack_angle == "right": self.movement[0] = 6
      if self.attack_angle == "left": self.movement[0] = -6
      if self.attack_angle == "down": self.movement[0] = 0
      if self.collision_type["bottom"]:
        if self.timer.time == 0: main.shake[1] = 2; stomp_sfx.play(); self.x_momentum = 0
        else: main.shake[1] *= -1
        self.movement = [0, 0]
        self.attack_angle = "down"
        if self.timer.timer(7): self.state = "idle"; self.frame = 1; main.shake[1] = 0

    if self.collision_type["bottom"]: self.y_momentum = 1
    
    if abs(self.movement[0]) < 5:
      if self.x_momentum > self.speed: self.x_momentum = self.speed
      if self.x_momentum < -self.speed: self.x_momentum = -self.speed
      if not self.wall_sliding: self.movement[0] = self.x_momentum
    
    if abs(self.movement[0]) > 5 and not self.wall_sliding:
      if self.x_momentum > self.speed: self.x_momentum = self.speed; self.movement[0] = self.speed
      if self.x_momentum < -self.speed: self.x_momentum = -self.speed; self.movement[0] = -self.speed

    if self.collision_type["left"] and self.wall_sliding and not self.flipped: self.movement[0] = 0
    if self.collision_type["right"] and self.wall_sliding and self.flipped: self.movement[0] = 0


  def control(self):
    if self.state != "attack" and not self.vine_climbing:
      if self.lobster_timer == 1: self.movement[0] = 0; self.x_momentum = 0
      if self.lobster_timer > 0: self.lobster_timer -= 1
      else:
        if get_buttons("right"):
            self.flipped = False
            if self.wall_sliding and self.collision_type["right"]: self.movement[0] = 6
            else: self.x_momentum += 1
            if self.collision_type["bottom"]:
              if not self.started_walking: self.state = "walkstart"; self.frame = self.timer.count(3, 4, 1)
              if self.state == "walkstart" and self.frame == 4: self.started_walking = True; self.timer.reset()
              if self.started_walking: self.state = "walk"; self.frame = self.timer.keep_count(4, 5, 1)

        elif get_buttons("left"):
            self.flipped = True
            if self.wall_sliding and self.collision_type["left"]: self.movement[0] = -6
            else: self.x_momentum -= 1
            if self.collision_type["bottom"]:
              if not self.started_walking: self.state = "walkstart"; self.frame = self.timer.count(3, 4, 1)
              if self.state == "walkstart" and self.frame == 4: self.started_walking = True; self.timer.reset()
              if self.started_walking: self.state = "walk"; self.frame = self.timer.keep_count(4, 5, 1)
        else:
          if self.x_momentum > 0: self.x_momentum -= 1
          if self.x_momentum < 0: self.x_momentum += 1
          self.movement[0] = 0; self.started_walking = False
          if self.collision_type["bottom"]: self.timer.reset(); self.state = "idle"; self.frame = 1
      
      if get_buttons("up") or get_buttons("a"):
        if self.air_timer == 0: self.y_momentum = self.vertical_power
        if self.collision_type["bottom"]:
          self.timer.reset()
          if k_up or k_a: jump_sfx.play()
      
      if k_down:
        if not self.wall_sliding:
          if not self.collision_type["bottom"]:
            if self.movement[0] > 0: self.attack_angle = "right"
            elif self.movement[0] < 0: self.attack_angle = "left"
            elif self.movement[0] == 0: self.attack_angle = "down"
            self.state = "attack"; self.frame = 1; self.timer.reset()
      
  
  def move(self, tiles): #collision and moving the player
    self.collision_type = {"top":False, "bottom":False, "right":False, "left":False} #this is the collision reletive to the entity
    self.rect.x += self.movement[0]
    hit_list = self.collision_test(tiles)
    for tile in hit_list:
      if self.movement[0] > 0:
        self.rect.right = tile.left
        self.collision_type["right"] = True

      elif self.movement[0] < 0:
        self.rect.left = tile.right
        self.collision_type["left"] = True
    
    self.rect.y += self.movement[1]
    hit_list = self.collision_test(tiles)
    for tile in hit_list:
      if self.movement[1] > 0:
        self.rect.bottom = tile.top
        self.collision_type["bottom"] = True

      elif self.movement[1] < 0:
        self.rect.top = tile.bottom
        self.collision_type["top"] = True
    
    return self.collision_type, self.rect
  
  
  def gravity(self):
    self.y_momentum += 0.4
    if self.y_momentum > 8: self.y_momentum = 8
    
    self.movement[1] = self.y_momentum
    if self.collision_type["bottom"]:
      self.air_timer = 0
      self.jumps = 0
        
    else:
      self.mid_air = False
      self.air_timer += 1   
  
  
  def wall_slide(self):
    if self.collision_type["left"] and self.movement[0] < 0:
      self.wall_sliding = True; self.air_timer = 0
      self.state = "slide"; self.frame = 1; self.timer.reset()
      self.x_momentum = 0; slide_sfx.play()
      self.vine_climbing = False
    elif self.collision_type["right"] and self.movement[0] > 0:
      self.wall_sliding = True; self.air_timer = 0
      self.state = "slide"; self.frame = 1; self.timer.reset()
      self.x_momentum = 0; slide_sfx.play()
      self.vine_climbing = False
    else: self.wall_sliding = False
        
    if self.wall_sliding: self.movement[1] *= self.friction
    
    if self.wall_sliding and (get_buttons("up") or get_buttons("a")):
        
      if self.collision_type["left"]:
        self.movement[0] = self.horizontal_power
        jump_sfx.play()
          
      elif self.collision_type["right"]:
        self.movement[0] = -self.horizontal_power
        jump_sfx.play()
          
      self.lobster_timer = 5 
      self.y_momentum = self.vertical_power
      self.wall_sliding = False
      self.x_momentum = 0

  def vine_climb(self):
    for vine in main.vines:
      if vine.rect.colliderect(self.rect):
        if not self.vine_climbing: self.timer.reset(); self.frame = 1
        self.vine_climbing = True
        self.wall_sliding = False
        if not get_buttons("a"):
          if get_buttons("right"): self.flipped = True
          if get_buttons("left"): self.flipped = False
          if self.flipped: self.rect.x = vine.rect.x
          else: self.rect.x = vine.rect.x - 12
          self.state = "climb"

    if self.vine_climbing:
      if get_buttons("a"):
        if self.flipped: self.movement[0] = self.horizontal_power
        else: self.movement[0] = -self.horizontal_power
        if k_a: jump_sfx.play()
        self.y_momentum = self.vertical_power
        self.lobster_timer = 5
        self.x_momentum = 0
        self.vine_climbing = False

      if get_buttons("up"): self.movement[1] = -2; self.frame = self.timer.keep_count(4, 3, 1); climb_sfx.play()
      elif get_buttons("down"): self.movement[1] = 2; self.frame = self.timer.keep_count(4, 3, 1); climb_sfx.play()
      else: self.movement[1] = 0






class Enemy(Player):
  def __init__(self, x, y, animal):
    super().__init__(x,y)
    self.alert = False
    self.animal = animal
    self.timer2 = Timer()
    self.timer3 = Timer()
    self.index = []
    self.state = "idle"#inshallah, okay bro did you do the tally thing? You gotta do it with me it's what making that dingo not move

  def update(self): #uhm
    self.get_alerted()
    try: self.image = pygame.transform.flip(pygame.image.load("Assets/" + self.animal + "/" + self.state + str(self.frame) + ".png").convert_alpha(), self.flipped, False)
    except: self.image = pygame.transform.flip(pygame.image.load("Assets/" + self.animal + "/idle1.png").convert_alpha(), self.flipped, False)
    display.blit(self.image, (self.rect.x - main.scroll[0] - 3, self.rect.y - main.scroll[1]))
    # self.state = "wake"

    #print("STATE " + self.state)
    #print("frames " + str(self.frame))
    if self.alive: tiles = main.world.tile_rect
    else: tiles = []
    self.collision_type, self.rect = self.move(tiles)
    self.gravity()

    if self.y_momentum >= 8 and not self.alive: main.animals[self.animal].remove(self)
    if self.rect.y > HEIGHT + main.scroll[1] and self.alive: self.alive = False; self.timer.reset(); self.x_momentum = 0; self.y_momentum = 0; self.frame = 1; self.movement[1] = 0; self.y_momentum = self.vertical_power * 1.5
    if not self.alive: self.state = "defeat"
  
    if self.collision_type["bottom"]:
      self.y_momentum = 1

    if self.collision_type["bottom"]: #what are you doing man did you make the dingo wake up and do his things
      if self.animal == "python": self.y_momentum = self.vertical_power; self.gravity()
    if self.animal == "python": self.frame = self.timer.keep_count(2, 5, 1); self.state = "idle"
  

  def get_distance(self, target):
      return math.sqrt((self.rect.x - target.rect.x) ** 2 + (self.rect.y - target.rect.y) ** 2)

  def get_alerted(self):
    self.radius = self.get_distance(main.player)
    
    if self.radius <= 75:
      self.alert = True
      if self.alert:
        if self.state == "idle":
          self.state = "wake"

        if self.state == "wake": 
          self.frame = self.timer3.keep_count(4, 3, 1) #because this doesn't go up
            
          if self.timer3.tally == 3:# because this never reaches to 3
            self.state = "run"
      
    
      if self.state == "run":
        if main.player.rect.x > self.rect.x:  # Player at right
          self.movement[0] = 5
          self.flipped = False#The thing is, running is not even happening
          self.frame = self.timer2.keep_count(3, 4, 1)

        if main.player.rect.x < self.rect.x:  # Player at left
          self.movement[0] = -5
          self.flipped = True
          self.frame = self.timer2.keep_count(3, 4, 1)

      #else: self.state = "idle"; self.frame = self.timer.keep_count(FPS / 2, 3, 1)
#it will keep reseting back to idle man it will keepit will keep
#but it is needed







#old stuff
  #def update(self):
    #try: self.image = pygame.transform.flip(pygame.image.load("Assets/" + self.animal + "/" + self.state + str(self.frame) + ".png").convert_alpha(), self.flipped, False)
    #except: self.image = pygame.transform.flip(pygame.image.load("Assets/" + self.animal + "/idle1.png").convert_alpha(), self.flipped, False)
    #screen.blit(self.image, (self.rect.x - main.scroll[0] - 3, self.rect.y - main.scroll[1]))
    
    #if self.alive: tiles = main.world.tile_rect
    #else: tiles = []
    #self.collision_type, self.rect = self.move(tiles)
    #if self.alive: self.control()
    #self.gravity()
    #self.get_alerted()

    #if self.y_momentum >= 8 and not self.alive: main.animals[self.animal].remove(self)
    #if self.rect.y > HEIGHT + main.scroll[1] and self.alive: self.alive = False; self.timer.reset(); self.x_momentum = 0; self.y_momentum = 0; self.frame = 1; self.movement[1] = 0; self.y_momentum = self.vertical_power * 1.5
    #if not self.alive: self.state = "defeat"
    
    #if self.collision_type["bottom"]: self.y_momentum = 1
    
  #def get_distance(self, target):
    #return abs(self.rect.x - target.rect.x)

  #def get_direction(self, target):
   # rel_Y, rel_X =  target.rect.y - self.rect.y, target.rect.x - self.rect.x
    #self.angle = math.atan2(rel_Y, rel_X)
    #return math.degrees(self.angle)
    
  #def get_alerted(self):
    #if self.get_distance(main.player) <= 75:
     # self.alert = True

    #if self.alert:
      #if self.state == "wake":
      #  self.frame = self.timer.count(4, 3, 1)

     # if self.timer.tally == 3:
        #self.state = "run"
       # self.frame = self.timer2.keep_count(3, 3, 1)
      #else:
       # self.state = "wake" #bro when are we setting it to wake?

      #if self.state == "run":
        #if self.player.rect.x > self.rect.x:  # Player at right
         # self.movement[0] = 5
        #  self.flipped = False

       # if self.player.rect.x < self.rect.x:  # Player at left
      #    self.movement[0] = -5
     #     self.flipped = True




class Stalagtite:
  def __init__(self): self.rect = pygame.Rect((random.randrange(0, WIDTH) + main.scroll[0], -(HEIGHT // 2)), (25, 19)); self.velocity = 0; self.dropping = False
  def update(self):
    if self.rect.y < -25: self.rect.y += 5; pygame.draw.line(display, (75, 0, 0), (self.rect.x - main.scroll[0] + 9, 0), (self.rect.x - main.scroll[0] + 9, HEIGHT), 3)
    else:
      if not self.dropping: spike_sfx.play()
      self.dropping = True; self.rect.y += self.velocity; self.velocity += 0.5; display.blit(pygame.image.load("Assets/stalagtite.png").convert_alpha(), (self.rect.x - main.scroll[0] - 3, self.rect.y))

class Droplet:
  def __init__(self): self.rect = pygame.Rect((random.randrange(0, WIDTH), -5), (1, 5)); self.velocity = 0
  def update(self): self.rect.y += self.velocity; self.velocity += 1; pygame.draw.rect(display, (240, 245, 255), self.rect)




def get_buttons(button):
  kb = pygame.key.get_pressed()
  if button == "a": return kb[pygame.K_SPACE] or kb[pygame.K_e] or kb[pygame.K_z] or kb[pygame.K_KP6]
  if button == "b": return kb[pygame.K_q] or kb[pygame.K_x] or kb[pygame.K_BACKSPACE] or kb[pygame.K_KP2]
  if button == "x": return kb[pygame.K_o] or kb[pygame.K_c] or kb[pygame.K_KP8]
  if button == "y": return kb[pygame.K_p] or kb[pygame.K_v] or kb[pygame.K_KP4]
  if button == "right": return kb[pygame.K_RIGHT] or kb[pygame.K_d]
  if button == "left": return kb[pygame.K_LEFT] or kb[pygame.K_a]
  if button == "up": return kb[pygame.K_UP] or kb[pygame.K_w]
  if button == "down": return kb[pygame.K_DOWN] or kb[pygame.K_s]
  if button == "l": return kb[pygame.K_MINUS]
  if button == "r": return kb[pygame.K_EQUALS] #I made wall sliding and jumping do you think it will work come
  if button == "select": return kb[pygame.K_i]
  if button == "start": return kb[pygame.K_RETURN]
  if button == "back": return kb[pygame.K_ESCAPE]


k_a, k_b, k_x, k_y, k_right, k_left, k_up, k_down, k_l, k_r, k_select, k_start, k_back = False, False, False, False, False, False, False, False, False, False, False, False, False

def run():
  global k_a, k_b, k_x, k_y, k_right, k_left, k_up, k_down, k_l, k_r, k_select, k_start, k_back
  k_a, k_b, k_x, k_y, k_right, k_left, k_up, k_down, k_l, k_r, k_select, k_start, k_back = False, False, False, False, False, False, False, False, False, False, False, False, False
  clock.tick(FPS)
  pygame.display.update()
  screen.blit(display, main.shake)
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (get_buttons("back") and main.gamestate == 0):
      pygame.quit()
      exit()
      
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE or event.key == pygame.K_e or event.key == pygame.K_z or event.key == pygame.K_KP6: k_a = True
      if event.key == pygame.K_q or event.key == pygame.K_x or event.key == pygame.K_BACKSPACE or event.key == pygame.K_KP2: k_b = True
      if event.key == pygame.K_o or event.key == pygame.K_c or event.key == pygame.K_KP8: k_x = True
      if event.key == pygame.K_p or event.key == pygame.K_v or event.key == pygame.K_KP4: k_y = True
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = True
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = True
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = True
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = True
      if event.key == pygame.K_MINUS: k_l = True
      if event.key == pygame.K_EQUALS: k_r = True
      if event.key == pygame.K_i: k_select = True
      if event.key == pygame.K_RETURN: k_start = True
      if event.key == pygame.K_ESCAPE: k_back = True
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_SPACE or event.key == pygame.K_e or event.key == pygame.K_z or event.key == pygame.K_KP6: k_a = False
      if event.key == pygame.K_q or event.key == pygame.K_x or event.key == pygame.K_BACKSPACE or event.key == pygame.K_KP2: k_b = False
      if event.key == pygame.K_o or event.key == pygame.K_c or event.key == pygame.K_KP8: k_x = False
      if event.key == pygame.K_p or event.key == pygame.K_v or event.key == pygame.K_KP4: k_y = False
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d: k_right = False
      if event.key == pygame.K_LEFT or event.key == pygame.K_a: k_left = False
      if event.key == pygame.K_UP or event.key == pygame.K_w: k_up = False
      if event.key == pygame.K_DOWN or event.key == pygame.K_s: k_down = False
      if event.key == pygame.K_MINUS: k_l = False
      if event.key == pygame.K_EQUALS: k_r = False
      if event.key == pygame.K_i: k_select = False
      if event.key == pygame.K_RETURN: k_start = False
      if event.key == pygame.K_ESCAPE: k_back = False
  if k_down and k_up and pygame.mouse.get_pressed(): pygame.image.save(display, "screenshot.png")
  display.fill("Black")


main = Main()

while True: main.update()