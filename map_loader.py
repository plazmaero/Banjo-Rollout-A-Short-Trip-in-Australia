import pygame
import os
import json
pygame.init()
#Oh alright I will download that workspace then
#I gotta go eat
class Map():
  def __init__(self, tile_database, tile_list, main):
    self.main = main
    self.tile_database = tile_database
    self.tile_list = tile_list
    self.collidables = []
    self.tile_rect = []
    self.rects = {}
    self.get_tiles()
    self.rects_data = self.get_col()
    self.decoy = ["dingo.png", "python.png", "eagle.png"]
        
    
  def get_tiles(self):
    for tile in self.tile_list:
      img = pygame.image.load('Assets/tiles/' + tile).convert_alpha()
      img.set_colorkey((255, 255, 255))
      self.tile_database[tile] = img.copy()
    
    return self.tile_database
        
        

  def get_col(self,):
    with open('data.json', 'r') as f:
      data = json.load(f)
      meta_data = data["collidables"]
      
      for tile in self.tile_database:
        for col in meta_data:
          if tile == col: self.collidables.append(tile)
      
      for name in self.collidables: self.rects[name] = pygame.Rect(meta_data[name][0], meta_data[name][1], meta_data[name][2], meta_data[name][3])
    
    return self.rects
        
        
    
    
  def load_map(self, path):
    with open(f'{path}.json', 'r') as f: data = json.load(f); tile_map = data['map']
    return tile_map



  def tiles(self, world_data, Entity ,display, scroll):#we alread
    self.tile_rect = []

    #should I clear the list? like in self.tile_rect? the vines list
    #well we gotta clear it everytime this function is finished
    self.main.vines.clear()
    self.main.animals["dingo"].clear()
    self.main.animals["eagle"].clear()
    #self.main.animals["python"].clear()

    # layers #Oh okay let's see if this works but hold on
    for i, layer in sorted(enumerate(world_data), reverse=True):#w
      # tiles
      for j, tile in sorted(enumerate(world_data[layer]), reverse=True):
        loc = tile.split(':')
        tile_data = world_data[layer][tile]

        if tile_data[4] == "vines.png":#should this be main.vines?
#so we don't have infinity vines appending inside the list, if the position has already a vine, it will not append
          vines_exists = any(vine.rect.x == int(loc[0]) and vine.rect.y == int(loc[1]) for vine in self.main.vines)# i have better idea
          if not vines_exists:
            self.main.vines.append(Vine(int(loc[0]), int(loc[1])))

        #Stuff vunerable to entities　下
        dingo_exists = False
        python_exists = False
        eagle_exists = False
        if tile_data[4] == "dingo.png":

          for dingo in self.main.animals["dingo"]:
            if dingo.rect.x == int(loc[0]) and dingo.rect.y == int(loc[1]):
              dingo_exists = True #okay so I rewrote the method of checking wiether someone taking the loc or nah
            dingo.index.append([dingo.rect.x, dingo.rect.y])  #every time we go throug a dingo in that list we append his location here
            #because look index[0] is the first list       
          if not dingo_exists:
            self.main.animals["dingo"].append(Entity(int(loc[0]), int(loc[1]), "dingo"))

        if tile_data[4] == "python.png":
          for python in self.main.animals["python"]:
            python_exists = any(python.rect.x == int(loc[0]) and python.rect.y == int(loc[1]) for python in self.main.animals["python"])
            if not python_exists:
              python.index += 1

              self.main.animals["python"].append(Entity(int(loc[0]), int(loc[1]), "python"))

        if tile_data[4] == "eagle.png":
          for eagle in self.main.animals["eagle"]:

            eagle_exists = any(eagle.rect.x == int(loc[0]) and eagle.rect.y == int(loc[1]) )
            if not eagle_exists:
              eagle.index += 1

              self.main.animals["eagle"].append(Entity(int(loc[0]), int(loc[1]), "eagle"))

        if tile_data[4] not in self.decoy:

          display.blit(self.tile_database[tile_data[4]], (int(loc[0]) - int(scroll[0]), int(loc[1]) - int(scroll[1])))

        if tile_data[4] in self.collidables:
          self.tile_rect.append(
              pygame.Rect(
                  int(loc[0]) + self.rects[tile_data[4]].x,
                  int(loc[1]) + self.rects[tile_data[4]].y,
                  self.rects_data[tile_data[4]].width,
                  self.rects_data[tile_data[4]].height,
              )
          )
#w
#main.update got all the game Oh okay
#or no no player.update
class Vine: #
  def __init__(self, x, y):#why did crash man
    self.rect = pygame.Rect((x + 8, y), (5, 25))
    #self.image = pygame.image.load("Assets/tiles/vidid ines.png")

  #def update(self, screen, scroll):#Why tho its already blited via tiles
    #pygame.draw.rect(screen, "Red", (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))
    #screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    
            
                    
                
#uhh still working on that I will be doing it now

#I am gonna make save settings now
