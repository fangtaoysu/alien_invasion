import sys
import pygame
import game_functions as gf # 管理方法

from settings import Settings # 管理参数
from game_stats import GameStats # 管理游戏信息
from ship import Ship
from alien import Alien
from button import Button
from scoreBoard import ScoreBoard
from pygame.sprite import Group


def run_game():
	# 初始化游戏pygame、设置和屏幕对象【初始化逻辑】
	pygame.init()
	ai_settings = Settings() # new一个设置对象
	
	# screen: surface, 每一个屏幕对象都是surface 设置屏幕宽和高
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion") # 设置程序名
	stats = GameStats(ai_settings) # new一个用于统计游戏信息的对象
	sb = ScoreBoard(ai_settings, screen, stats)
	# 创建一艘飞船、一个子弹编组和一个外星人编组
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	
	# 创建ufo群
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# 创建Play按钮
	play_button = Button(ai_settings, screen, "play")
	
	# 读历史最高分
	stats.high_score = gf.read_max_file(stats.high_score)
	
	# 开始游戏的主循环
	while True:
		gf.check_events(ai_settings, stats, sb, screen, play_button, ship, aliens, bullets)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets) # 对编组调用update，编组会对每个sprite调用update
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
		
		gf.update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button)

run_game()
