#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Nosov Mikhail, viver_117, Konstantin Guk
# Consultant: grishnan
# E-mails: mikhail1920@mail.com, viver12366@gmail.com, 1996artes@mail.ru, grishnan@gmail.com
# License: GNU GPL v3.0
# Description by Eng: Program «Collection picture»
# Description by Rus: Программа «Собери картинку»


import sizefield
import pygame
from classes import LevelButton
from consts import update_consts



pygame.init(); pygame.font.init(); # добавил инициализацию шрифта чтоб рисовались цифры на начальном экране

levelButtons = [LevelButton(100 + 200 * (i % 2), 100 + 200 * (i // 2), 150, i+2) for i in range(1, 4)]
# инициализация массива с объектами LevelButton, это наши кнопки выбора уровня	

# 


screen = pygame.display.set_mode((550, 550)) # создаю экран выбора уровня
SIZE_FIELD = 0 # делаю пока заглушку для переменной размера поля 
choosingLevel = True 
while choosingLevel:
  screen.fill((255, 255, 255))
  for button in levelButtons: button.draw(screen); # отрисовываю все кнопки из массива levelButtons
  for event in pygame.event.get(): 
  	if event.type == pygame.QUIT: pygame.quit(); sys.exit();
  	if event.type == pygame.MOUSEBUTTONDOWN: # если происходит клик по полю, пробегаюсь по массиву кнопок, чтобы понять на какую нажали
  		for button in levelButtons:
  			if button.collides(event): # и если на какую-то нажали
  				# print(button.n) 
  				update_consts(button.n); # обновляю константы в файле const.py чтоб сменить потом разрешение окна
  				SIZE_FIELD = button.n; # приравниваю размер игрового поля к номеру кнопки, например к 2
  				choosingLevel = False; # выхожу из цикла выбора уровня
  				break
  pygame.display.update()

from consts import * # импортирую измененные ранее константы из файла const.py
from classes import * # испортирую класс Field только на этом этапе программы, чтобы он считался уже с измененными константами из const.py

# далее почти везде оригинальный код 
pygame.display.set_mode((SIZE_SCREEN, SIZE_SCREEN)) # изменяю размер окна на нужный
pygame.display.set_caption("Collection picture")

field = Field(SIZE_FIELD) # отправляю в конструктор параметр размера поля, потому что теперь это переменное значение, соответственно и конструктор класса Field переписан, обратите внимание

gotoGame = True
while gotoGame:
  
  ''' обработчик событий '''
  for event in pygame.event.get():
    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN: gotoGame = False
      
  screen.fill(WHITE)
  field.drawField(screen)
  field.assignment(screen)
  (gx, gy) = field.fromLocalToGlobal(SIZE_FIELD - 1, SIZE_FIELD - 1)
  screen.blit(field.pics[-1], (gx, gy, SIZE_CHIP, SIZE_CHIP))

  pygame.display.update()

field.randomMix()

while True:
  
  ''' обработчик событий '''
  for event in pygame.event.get():
    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mousex, mousey = event.pos
      field.makeMove(mousex, mousey)
      #print(field.matrix)
  
  ''' отрисовка игрового поля '''
  screen.fill(WHITE)
  field.drawField(screen)
  field.assignment(screen)

  pygame.display.update()
