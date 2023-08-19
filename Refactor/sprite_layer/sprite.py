import json
from Refactor.render_layer.element import Element


class SpriteData:
	"""
	Class that represents sprite data.
	Sprite data consists of the resources that are common in all the sprites
	of the same type, including the image resources, the states and the frames
	of each state.
	"""
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
	"""
	Class that represents a sprite. A sprite is a piece of sprite data with a particular
	state and frame specified.
	"""
	
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
	
	def get_frame_count(self):
		return self.get_state_frame_count(self.state_name)
	
	def get_state_names(self):
		return self.sprite_data.states.keys()
	
	def get_state_frame_count(self, state_name):
		return len(self.sprite_data.states[state_name])
	
	def set_state(self, state_name):
		assert state_name in self.get_state_names(), f"State name {state_name} not found"
		self.state_name = state_name
	
	def set_frame(self, frame_index):
		assert frame_index < self.get_frame_count(), f"Frame index {frame_index} out of bounds"
		self.frame_index = frame_index
	
	def get_frame_index(self):
		return self.frame_index
	
	def get_state_name(self):
		return self.state_name
	
	def next_frame(self):
		self.set_frame((self.get_frame_index() + 1) % self.get_frame_count())
	
	def prev_frame(self):
		self.set_frame((self.get_frame_index() - 1) % self.get_frame_count())
	
	def get_progress(self):
		return self.get_frame_index() / self.get_frame_count()
	
	def set_progress(self, progress):
		assert 0 <= progress <= 1, f"Progress {progress} out of bounds"
		self.set_frame(min(int(progress * self.get_frame_count()), self.get_frame_count()-1))