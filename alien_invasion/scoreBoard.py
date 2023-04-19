import pygame.font
from pygame.sprite import Sprite
from ship import Ship
from pygame.sprite import Group

class ScoreBoard():
	'''显示得分信息的类'''
	
	def __init__(self, ai_settings, screen, stats):
		'''初始化显示得分涉及的属性'''
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		# 显示得分信息用的字体设置
		self.text_color = (255,255,224)
		self.font = pygame.font.SysFont('Segoe Script', 28)
		
		# 准备初始化得分和最高分图像
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		
		
	def prep_ships(self):
		'''显示还有多少艘飞船'''
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
		
	def prep_level(self):
		'''将等级渲染为图像'''
		self.level_image = self.font.render('Lv:' + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
		
		# 将等级放在得分下方
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_score(self):
		'''将得分转化为一张渲染的图像'''
		# round 小数精确到小数点多少位 负数表示圆整到最近的10,100,1000等整数倍
		rounded_score = int(round(self.stats.score, 0))
		# 转化为字符串时插入逗号
		score_str = 'points:' + "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
		
		# 将得分放在屏幕右上角
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def prep_high_score(self):
		'''将最高分转化为一张渲染的图像'''
		high_score = int(round(self.stats.high_score, 0))
		high_score_str = 'max:' + "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
		
		# 将最高分放在屏幕左上角
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.center = self.screen_rect.center
		self.high_score_rect.top = 20
		
		
	def show_score(self):
		'''在屏幕上显示得分、最高分和等级'''
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)
