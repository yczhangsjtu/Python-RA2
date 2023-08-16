import json
from Refactor.render_layer.element import Element


class SpriteData:
	def __init__(self, data_path):
		"""
		:param data_path: Path to the JSON file with sprite data
		"""
		with open(data_path) as f:
			data = json.load(f)
		self.frame_width = data["frame_width"]
		self.frame_height = data["frame_height"]
		self.image_path = data["img"]
		self.default_state = data["default_state"]
		self.states = SpriteData.states_from_json(data["states"])

	@staticmethod
	def states_from_json(states):
		"""
		:param states: Dict of state names to frames
		:return: Dict of state names to frames
		"""
		return {
			state["name"]: SpriteData.frames_from_json(state["frames"])
			for state in states
		}

	@staticmethod
	def frames_from_json(frames):
		"""
		:param frames: List of frames or dict of frames
		:return: List of frames
		"""
		if isinstance(frames, list):
			return frames
		# If frames is dict, it means it's a state with multiple frames specified by
		# starting row and ending row, starting column and ending column
		if isinstance(frames, dict):
			return [(row, col)
					for row in range(frames["row_start"], frames["row_end"]+1)
					for col in range(frames["col_start"], frames["col_end"]+1)]
		raise TypeError(f"Unexpected type for frames: {type(frames)}")
	
	def get_coordinate(self, name, index):
		"""
		:param name: Name of the state
		:param index: Index of the frame
		:return: (row, col), coordinate of this frame
		"""
		assert name in self.states, f"State name {name} not found"
		frames = self.states[name]
		assert index < len(frames), f"Index out of bounds, there are {len(frames)} in {name}, got {index}"
		return frames[index]
	
	def get_area(self, name, index):
		"""
		:param name: Name of the state
		:param index: Index of the frame
		:return: (x, y, w, h), area of this frame in the sprite sheet
		"""
		row, col = self.get_coordinate(name, index)
		
		return (col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)


class Sprite:
	def __init__(self, sprite_data, pos=None):
		"""
		:param sprite_data: SpriteData instance
		:param pos: (x, y)
		"""
		self.sprite_data = sprite_data
		self.pos = pos
		self.state_name = sprite_data.default_state
		self.frame_index = 0
	
	@property
	def image_path(self):
		return self.sprite_data.image_path
	
	@property
	def frame_width(self):
		return self.sprite_data.frame_width
	
	@property
	def frame_height(self):
		return self.sprite_data.frame_height
	
	def set_pos(self, x, y):
		self.pos = (x, y)
	
	def generate_render_element(self):
		if self.pos == None:
			return None
		return Element(
			self.pos,
			"Refactor/render_layer/img/" + self.image_path,
			self.get_area()
		)
	
	def get_area(self):
		return self.sprite_data.get_area(self.state_name, self.frame_index)