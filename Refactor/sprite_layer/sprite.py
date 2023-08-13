import json


class SpriteData:
	def __init__(self, data_path):
		with open(data_path) as f:
			data = json.load(f)
		self.frame_width = data["frame_width"]
		self.frame_height = data["frame_height"]
		self.states = SpriteData.states_from_json(data["states"])

	@staticmethod
	def states_from_json(states):
		return {
			name: SpriteData.frames_from_json(frames)
			for name, frames in states.items()
		}

	@staticmethod
	def frames_from_json(frames):
		if isinstance(frames, list):
			return frames
		if isinstance(frames, dict):
			return [(row, col)
					for row in range(frames["row_start"], frames["row_end"]+1)
					for col in range(frames["col_start"], frames["col_end"]+1)]
		raise TypeError("Unexpected type for frames")


class Sprite:
	def __init__(self, sprite_data, pos=None):
		self.sprite_data = sprite_data
		self.pos = pos