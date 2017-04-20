#CSCI 1300 Project 1 - Monster Battle Game
#by Zachary Passarelli
#All art used in this program was created by me.

import pygame
from pygame.locals import *
import os, random

def main():
	print("Welcome brave hero! \n")
	playAgain = "y"
	winStreak = 0
	#loop for play again functionality
	while playAgain == "y":
		#status dictionary will hold data and pass it all through the functions
		status = {}
		print("Before you begin your journey, choose an element to charge your weapon!")
		#loop to display element choices
		for i in range(1,4):
			print(i,"for",element(i))
		pElement = input(">>>")
		#while loop to counter incorrect input
		while pElement != "1" and pElement != "2" and pElement != "3":
			print("Try again, hero!")
			pElement = input(">>>")
		print("With your",element(pElement),"infused sword, you venture forth!\nEncounter!")
		#add player element to status dictionary
		status.update({'pElement':pElement})

		#add player health points to status dictionary
		status.update({'pHP':200})
		#call monster generator function and add all of its details to status dictionary
		monster_generator(status)
		#call matchup function to compare player element and monster element and add data to status dictionary
		matchup(status)

		#-----
		#background image is chosen at random
		background_key = random.randint(1,3)
		if background_key == 1:
			selectBg = "loc_plain.png"
		elif background_key == 2:
			selectBg = "loc_cave.png"
		else:
			selectBg = "loc_volcano.png"

		#if statements to find out which monster image to obtain for this instance
		if status['mType'] == 'dragon':
			selectMon = "dragon"
		elif status['mType'] == 'slime':
			selectMon = "slime"
		else:
			selectMon = "crow"
		if status['mElement'] == 1:
			selectMon += "_fire"
		elif status['mElement'] == 2:
			selectMon += "_water"
		else:
			selectMon += "_tree"
		selectMon += ".png"

		#if statements to obtain attack meter based on matchup data
		if status['matchup'] == 0:
			selectMeter = "bar_feeble.png"
		elif status['matchup'] == 2:
			selectMeter = "bar_super.png"
		else:
			selectMeter = "bar_normal.png"

		#gotta initialize this thing
		pygame.init()
		#create a surface, sized 500 x 375px
		screen = pygame.display.set_mode((500,375))
		pygame.display.set_caption("Monster Battle")
		#initialize clock and frame rate
		clock = pygame.time.Clock()
		fps = 30
		#loading background image
		background = pygame.image.load(os.path.join('art',selectBg))
		#loading player images
		player_idle = pygame.image.load(os.path.join('art','knight_idle.png'))
		player_move = pygame.image.load(os.path.join('art','knight_move.png'))
		player_rdy = pygame.image.load(os.path.join('art','knight_rdy.png'))
		player_atk = pygame.image.load(os.path.join('art','knight_atk.png'))
		player_miss = pygame.image.load(os.path.join('art','knight_miss.png'))
		player_dmg = pygame.image.load(os.path.join('art','knight_dmg.png'))
		#set player location
		player_x, player_y = 20, 220

		#loading monster images
		monster = pygame.image.load(os.path.join('art',selectMon))
		selectMonDmg = selectMon[:-4] + "_dmg.png"
		monster_dmg = pygame.image.load(os.path.join('art',selectMonDmg))
		#set monster location
		monster_x, monster_y = 340, 220

		#loading attack meter and marker images
		meter = pygame.image.load(os.path.join('art',selectMeter))
		marker = pygame.image.load(os.path.join('art','bar_marker.png'))
		#set attack meter location
		meter_x, meter_y = 280, 100
		#create meter and market Rect objects to be used later
		meterRect = pygame.Rect((meter_x,meter_y),(200,25))
		markerRect = pygame.Rect((meter_x,meter_y),(10,25))
		#setting marker speed for later use, randomly generated to mix things up
		speed_x = random.randint(5,9)

		#drawing initial scene
		screen.blit(background,(0,0))
		screen.blit(player_idle,(player_x,player_y))
		screen.blit(monster,(monster_x,monster_y))
		pygame.display.flip()
		#-------

		#call show status function to give information to player
		show_status(status)
		#addional information based on matchup data
		if status['matchup'] == 2:
			print("You have the advantage!")
		elif status['matchup'] == 0:
			print("You are at a disadvantage..")

		#begin game loop
		while True:

			print("Press SPACE to attack!")
			#call wait for user function to pause game until user input
			wait_for_user()
			#-----player attack animation
			for x in range(0, 50, 5):
				player_x += x
				screen.blit(background,(0,0))
				screen.blit(player_move,(player_x,player_y))
				screen.blit(monster,(monster_x,monster_y))
				pygame.display.flip()
				clock.tick(fps)
			#-----
			#-----strike moment and meter animation
			print("Press S to make your strike!")
			while True:
				#initialize event watchers I suppose
				user_input = pygame.event.get()
				keys = pygame.key.get_pressed()
				screen.blit(background,(0,0))
				screen.blit(player_rdy,(player_x,player_y))
				screen.blit(monster,(monster_x,monster_y))
				screen.blit(meter,(meter_x,meter_y))
				#marker moves back and forth over meter, infinite until player input
				markerRect=markerRect.move(speed_x,0)
				if markerRect.left < meterRect.left or markerRect.right > meterRect.right:
					speed_x = -speed_x
				screen.blit(marker, markerRect)
				pygame.display.update(meterRect)
				clock.tick(fps)
				#pressing S will end the loop and thus decide where the player stopped the marker
				if keys[K_s]:
					break
			#-----
			#save location of center of marker
			marker_x = markerRect.center[0]
			#call meter reader function to analyze meter interaction and add data to status dictionary
			meter_reader(status, marker_x)
			#if player dealt damage, attack animation
			if status['atkValue'] > 0:
				#-----attack animation
				screen.blit(background,(0,0))
				screen.blit(player_atk,(player_x,player_y))
				screen.blit(monster_dmg,(monster_x,monster_y))
				pygame.display.flip()
				#-----
				#call damage calc to compute damage and remaining monster hp and update status dictionary
				damage_calc(status,"player attack")
			#if player missed, miss animation
			else:
				#-----miss animation
				screen.blit(background,(0,0))
				screen.blit(player_miss,(player_x,player_y))
				screen.blit(monster,(monster_x,monster_y))
				pygame.display.flip()
				#-----
				print("You missed..")
			#delay for visual effect
			pygame.time.delay(1500)
			#check monster health points
			if status['mHP'] < 1:
				#-----monster death animation
				for x in range(0, 50, 1):
					monDie = pygame.transform.scale(monster_dmg,(50-x,50-x))
					screen.blit(background,(0,0))
					screen.blit(player_idle,(player_x,player_y))
					screen.blit(monDie,(monster_x,monster_y))
					pygame.display.flip()
					clock.tick(fps)
				#-----
				#boolean to determine next step
				monsterLive = False
			else:
				#-----player reset position animation
				for x in range(0, 50, 5):
					if x == 0:
						return_player = pygame.transform.flip(player_move, 1, 0)
					player_x -= x
					screen.blit(background,(0,0))
					screen.blit(return_player,(player_x,player_y))
					screen.blit(monster,(monster_x,monster_y))
					pygame.display.flip()
					clock.tick(fps)
				screen.blit(background,(0,0))
				screen.blit(player_idle,(player_x,player_y))
				screen.blit(monster,(monster_x,monster_y))
				pygame.display.flip()
				#-----
				monsterLive = True
			#monster gets a turn if they survive, this statement is passed if monster dies
			if monsterLive == True:
				show_status(status)
				print("Press SPACE to continue..")
				#wait for user input
				wait_for_user()
				#-----monster attack animation
				for x in range(0, 55, 5):
					monster_x -= x
					screen.blit(background,(0,0))
					if x >= 45:
						screen.blit(player_dmg,(player_x,player_y))
					else:
						screen.blit(player_idle,(player_x,player_y))
					screen.blit(monster,(monster_x,monster_y))
					pygame.display.flip()
					clock.tick(fps)
				#-----
				#call damage calc to compute damage and remaining player health and add to status dictionary
				damage_calc(status,"monster attack")
				#delay for visual effect
				pygame.time.delay(1200)
				#check player health points
				if status['pHP'] < 1:
					#-----player death animation
					for x in range(0, 50, 1):
						playerDie = pygame.transform.scale(player_dmg,(80-x,80-x))
						screen.blit(background,(0,0))
						screen.blit(playerDie,(player_x,player_y))
						screen.blit(monster,(monster_x,monster_y))
						pygame.display.flip()
						clock.tick(fps)
					#-----
					playerLive = False
				#we're not out yet
				else:
					#-----monster reset position
					for x in range(0, 55, 5):
						if x == 0:
							return_monster = pygame.transform.flip(monster, 1, 0)
						monster_x += x
						screen.blit(background,(0,0))
						screen.blit(player_idle,(player_x,player_y))
						screen.blit(return_monster,(monster_x,monster_y))
						pygame.display.flip()
						clock.tick(fps)
					screen.blit(background,(0,0))
					screen.blit(player_idle,(player_x,player_y))
					screen.blit(monster,(monster_x,monster_y))
					pygame.display.flip()
					#-----
					playerLive = True
				if playerLive == True:
					show_status(status)
					#start from the beginning of game loop for next player turn
					continue
				else:
					print("GAME OVER.")
					#reset win streak and end game loop
					winStreak = 0
					break
			else:
				print("You are victorious!")
				#add to win streak and end game loop
				winStreak += 1
				break
		#-----cleanup animation
		pygame.quit()
		#-----
		print("Win streak:",winStreak)
		#ask user for play again input
		playAgain = input("Do you wish to play again? (y or n)")
		#loop to catch incorrect input
		while playAgain != "y" and playAgain != "n":
			print("Try again, hero!")
			playAgain = input("Do you wish to play again? (y or n)")

#element is a simple function that takes in a number to return an element
def element(e):
	e = str(e)
	if e == "1":
		return "fire"
	elif e == "2":
		return "water"
	elif e == "3":
		return "leaf"
	else:
		return "broken"

#show status displays key information from the status dictionary when called
def show_status(status):
	print("Hero -",status['pHP'],"HP\n"+element(status['mElement']).title(),status['mType'].title(),"-",status['mHP'],"HP")

#wait for user pauses the program and waits for user input
def wait_for_user():
	while True:
		pygame.event.wait()
		key = pygame.key.get_pressed()
		if key[K_SPACE]:
			break

#monster generator creates a monster with a few attributes using a series of random numbers
def monster_generator(status):
	#creates a probability, lower chance for difficult monsters to appear
	difficultySelector = random.randint(0,100)
	if difficultySelector > 80:
		monsterType = "dragon"
		monsterHP = random.randint(900,1500)
	elif difficultySelector <= 50:
		monsterType = "slime"
		monsterHP = random.randint(500,800)
	else:
		monsterType = "crow"
		monsterHP = random.randint(700,1100)
	monsterElement = random.randint(1,3)
	#add all data to status dictionary
	status.update({'mType':monsterType,'mElement':monsterElement,'mHP':monsterHP})
	return status

#matchup compares monster and player elements to determine a matchup value
def matchup(status):
	p = int(status['pElement'])
	m = status['mElement']
	#fire
	if p == 1:
		#fire has an advantage over leaf
		if m == 3:
			a = 2
		#fire has a disadvantage over water
		elif m == 2:
			a = 0
		#fire is neutral against itself
		else:
			a = 1
	#water
	elif p == 2:
		#water has an advantage over fire
		if m == 1:
			a = 2
		#water has a disadvantage over leaf
		elif m == 3:
			a = 0
		#water is neutral against itself
		else:
			a = 1
	#leaf
	elif p == 3:
		#leaf has an advantage over water
		if m == 2:
			a = 2
		#leaf has a disadvantage over fire
		elif m == 1:
			a = 0
		#leaf is neutral against itself
		else:
			a = 1
	#add data to status dictionary
	status.update({'matchup':a})
	return status

#damage calc uses data from meter reader and status dictionary to calculate damage dealt
def damage_calc(status, situation):
	#random bonus damage value for variation
	bonusDamage = random.randint(0,100)
	#player attack keyword allows function to focus on player attack and monster hp
	if situation == "player attack":
		damage = status['atkValue'] + bonusDamage
		print("You dealt",damage,"damage!")
		status['mHP'] -= damage
	#monster attack keyword allows function to focus on monster attack and player hp
	elif situation == "monster attack":
		monster = status['mType']
		if monster == "dragon":
			damage = 110 + bonusDamage
		elif monster == "slime":
			damage = 1 + bonusDamage
		else:
			damage = 30 + bonusDamage
		print("You were hit for",damage,"damage!")
		status['pHP'] -= damage
	else:
		pass
	return status

#meter reader takes in data from the meter interaction and determines an attack value
def meter_reader(status, marker_x):
	#the meter to be analyzed depends on the matchup data
	meterType = status['matchup']
	#account for meter being in the same location as marker
	meterOffset = 280
	normDmg, superDmg, miss = 500, 1000, 0
	if meterType == 0:
		#feeble
		if (meterOffset + 90) <= marker_x <= (meterOffset + 109):
			attack = normDmg
		else:
			attack = miss
	elif meterType == 2:
		#super
		if (meterOffset + 26) <= marker_x <= (meterOffset + 173):
			attack = superDmg
		else:
			attack = normDmg
	else:
		#normal
		if (meterOffset + 90) <= marker_x <= (meterOffset + 109):
			attack = superDmg
		elif (meterOffset + 26) <= marker_x <= (meterOffset + 89) or (meterOffset + 110) <= marker_x <= (meterOffset + 173):
			attack = normDmg
		else:
			attack = miss
	status.update({'atkValue':attack})
	return status

main()
