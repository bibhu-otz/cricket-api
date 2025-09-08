from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.player import Player
from app.crud.player import create_player,get_players,get_player,update_player,delete_player

from app.core.database import get_db_connection
router = APIRouter()


@router.post("/", response_model=Player, status_code=201)
async def create_player_endpoint(player: Player,
conn=Depends(get_db_connection)):
  try:
    
    new_player = create_player(player.model_dump(), conn)
    return new_player
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))



@router.get("/", response_model=List[Player])
async def get_players_endpoint(conn=Depends(get_db_connection)):
  try:
    return get_players(conn)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))



@router.get("/{id}", response_model=Player)
async def get_player_endpoint(id: int,
conn=Depends(get_db_connection)):
  try:
    player = get_player(id, conn)
    if player:
      return player
      raise HTTPException(status_code=404, detail="Player not found")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.put("/{id}", response_model=Player)    
async def update_player_endpoint(id: int, player: Player,
  conn=Depends(get_db_connection)):
  try:
    updated_player = update_player(id, player.model_dump(),conn)
    if updated_player:
      return updated_player
      raise HTTPException(status_code=404, detail="Player not found")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
    
    
@router.delete("/{id}")
async def delete_player_endpoint(id: int,conn=Depends(get_db_connection)):
  try:
    deleted = delete_player(id, conn)
    if deleted:
      return  {"message": "Player deleted successfully"}
    raise HTTPException(status_code=404, detail="Player not found")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))