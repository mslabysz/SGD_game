import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
FPS = 60

bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")

#game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0
sound_on = True
red = (255, 0, 0)
green = (0, 255, 0)
font = pygame.font.SysFont('Bauhaus 93', 26)

#load images
background_img = pygame.image.load('img/background/background.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
panel_img = pygame.image.load('img/background/bottom_pannel.png').convert_alpha()
panel_img = pygame.transform.scale(panel_img, (screen_width, bottom_panel))
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()

# background music
pygame.mixer.music.load('sounds/bg_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  #looped

# sound effects
sound_hit = pygame.mixer.Sound('sounds/hit.mp3')
sound_dead = pygame.mixer.Sound('sounds/dead.mp3')
sound_potion = pygame.mixer.Sound('sounds/potion.mp3')
sound_sword_knight = pygame.mixer.Sound('sounds/sword_knight.mp3')
sound_sword_bandit = pygame.mixer.Sound('sounds/sword_bandit.mp3')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
def draw_background():
    screen.blit(background_img, (0, 0))

def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    # Knight
    left_x = 30
    base_y = screen_height - bottom_panel + 20
    draw_text(f'{knight.name}', font, red, left_x, base_y)
    draw_text(f'HP: {knight.hp}/{knight.max_hp}', font, red, left_x, base_y + 35)
    # Knight health bar
    knight_health_bar.x = left_x
    knight_health_bar.y = base_y + 65
    # potions
    potion_icon_x = left_x + 150 + 20
    potion_icon_y = base_y + 55
    potion_button.rect.topleft = (potion_icon_x, potion_icon_y)
    # potions left
    draw_text(str(knight.potions), font, (255, 255, 255), potion_button.rect.x + 70, potion_button.rect.y + 20)
    # Enemies
    right_x1 = 400
    right_x2 = 560
    bandit_y = base_y
    # Bandit 1
    draw_text(f'{bandit_list[0].name}', font, red, right_x1, bandit_y)
    draw_text(f'HP: {bandit_list[0].hp}/{bandit_list[0].max_hp}', font, red, right_x1, bandit_y + 35)
    bandit1_health_bar.x = right_x1
    bandit1_health_bar.y = bandit_y + 65
    # Bandit 2
    draw_text(f'{bandit_list[1].name}', font, red, right_x2, bandit_y)
    draw_text(f'HP: {bandit_list[1].hp}/{bandit_list[1].max_hp}', font, red, right_x2, bandit_y + 35)
    bandit2_health_bar.x = right_x2
    bandit2_health_bar.y = bandit_y + 65

class Fighter():
    def __init__(self, x , y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0 = Idle, 1 = Attack, 2 = Hit, 3 = Dead
        self.update_time = pygame.time.get_ticks()

        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

    def idle(self):
        #setting variables for idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        #random damage addition
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage

        #attack sound effect
        if sound_on:
            if self.name == 'Knight':
                sound_sword_knight.play()
            else:
                sound_sword_bandit.play()
        #hit sound effect
        if sound_on:
            sound_hit.play()
        #enemy hurt animation
        target.hurt()
        #check if target is dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()

        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #setting variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        #setting variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #setting variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        # death sound effect
        if sound_on:
            sound_dead.play()
        self.alive = False
        self.hp = 0

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 100
        #handle animation
        #update the image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
             if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
             else:
                self.idle()

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #move the text up
        self.rect.y -= 1
        #delete the text after few sec
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()

#create knight and bandits
knight = Fighter(120, 325, 'Knight', 30, 10, 3)
bandit1 = Fighter(500, 335, 'Bandit', 20, 6, 1)
bandit2 = Fighter(630, 335, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

#create health bars
knight_health_bar = HealthBar(30, screen_height - bottom_panel + 120, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(500, screen_height - bottom_panel + 80, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(500, screen_height - bottom_panel + 140, bandit2.hp, bandit2.max_hp)

#create buttons
potion_button = button.Button(screen, 180, screen_height - bottom_panel + 85, potion_img, 64,64)
restart_button = button.Button(screen, 340,120,restart_img,120,30)
sound_button_img = pygame.image.load('img/Icons/mute.png').convert_alpha()
sound_button = button.Button(screen, 720, screen_height - bottom_panel + 85, sound_button_img, 64,64 )

run = True
while run:
    clock.tick(FPS)
    draw_background()
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    #draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #reset action variables
    #control player action
    attack = False
    potion = False
    target = None
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()

    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive:
                attack = True
                target = bandit_list[count]
    if potion_button.draw():
        potion = True
    #check if game is over
    if game_over == 0:
        #player action
        if knight.alive:
            if current_fighter ==1:
                action_cooldown +=1
                if action_cooldown>= action_wait_time:
                    #check for action
                    #attack
                    if attack == True and target != None:
                        #attack enemy
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #use potion
                    if potion == True:
                        #check if knight has potions
                        if knight.potions > 0:
                            #check if potion will heal over maxhp
                            if knight.max_hp - knight.hp> potion_effect:
                                 heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            if sound_on:
                                sound_potion.play()
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        #enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #check if bandit needs to heal
                        if (bandit.hp/bandit.max_hp) < 0.5 and bandit.potions>0:
                            # check if potion will heal over maxhp
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            if sound_on:
                                sound_potion.play()
                            current_fighter += 1
                            action_cooldown = 0
                        else:
                            #attack
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1
        #reset if all fighters have acted
        if current_fighter > total_fighters:
            current_fighter = 1

    #check if all bandits are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1
    #check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250,50))
        if game_over == -1:
            screen.blit(defeat_img, (290,50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0
    #sound button
    if sound_button.draw():
        sound_on = not sound_on
        if sound_on:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                sound_on = not sound_on
                if sound_on:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

    pygame.display.update()

pygame.quit()
