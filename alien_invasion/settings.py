class Settings():
	'''存储《外星人入侵》的所有设置类'''
	
	def __init__(self):
		'''初始化游戏的静态设置'''
		# self.max_row_number = max_row_number
		# self.max_col_number = max_col_number
		# 屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (54, 59, 64)
		
		# 飞船速度属性
		self.ship_limit = 3
		
		# 子弹设置
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 255,255,0
		self.bullets_allowed = 3
		
		# 外星人速度、行列数设置
		self.fleet_drop_speed = 10
		self.aliens_row_number = 1
		self.aliens_col_number = 1
		
		# 以什么样的速度加快游戏节奏
		self.speedup_scale = 1.1
		# 外星人点数的提高速度
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		'''初始化随游戏进行而变化的设置'''
		self.ship_speed_factor = 0.7
		self.bullet_speed_factor = 1.5
		self.alien_speed_factor = 0.5
		self.alien_points = 1.5
		
		# fleet_direction 1右移，-1左移
		self.fleet_direction = 1
		
	def increase_speed(self):
		'''提高速度设置、外星人个数和外星人分数'''
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
		#if self.max_row_number > self.aliens_row_number:
		#	self.aliens_row_number += 1
		#if self.max_col_number > self.aliens_col_number
		#	self.aliens_col_number += 1
		# 测试分数
		# print(self.alien_points)
		
