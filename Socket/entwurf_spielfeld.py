import pygame, time, math, random

pygame.init()
screen = pygame.display.set_mode([832,512])
clock = pygame.time.Clock()
pygame.display.set_caption("Bomberman")
pygame.mouse.set_visible(1)
pygame.key.set_repeat(1, 30)

done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	#screen.fill((255,0,0))
	pygame.draw.rect(screen,(0,0,0),(65,65,64,64))

pygame.quit()
