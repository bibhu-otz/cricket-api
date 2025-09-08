from pydantic import BaseModel
class Player(BaseModel):
  id: int
  name: str
  role: str
  batting_style: str
  bowling_style: str
  matches: int
  runs: int
  average: float
  strike_rate: float
  image_url: str