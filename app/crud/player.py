from typing import List,Dict,Any 
import psycopg2 

def player_to_dict(row: tuple)->Dict [str, Any]: return {     
  "id": row [0],
  "name": row [1],
  "role": row [2],
  "batting_style": row [3],
  "bowling_style": row [4],
  "matches": row [5],
  "runs": row [6],
  "average": row [7],
  "strike_rate": row [8],
  "image_url": row [9] } 

def create_player(player: Dict [str, Any], conn)->Dict [str,Any]: 
  try: 
    print(player)
    with conn.cursor() as cur: 
      cur.execute("""INSERT INTO players (id, name, role, batting_style,bowling_style, matches, runs, average, strike_rate, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
      RETURNING *
      """,(
      player ["id"],
      player ["name"],
      player ["role"],
      player ["batting_style"],
      player ["bowling_style"],
      player ["matches"],
      player ["runs"],
      player ["average"],
      player ["strike_rate"],
      player ["image_url"]
      )
    ) 
    new_player = cur.fetchone() 
    conn.commit() 
    return player_to_dict(new_player)
  except Exception as e: 
    print(e)
    conn.rollback() 
  raise 
  
  
def get_players(conn)->List [Dict[str, Any]]:
 try:
  with conn.cursor() as cur:
    cur.execute("SELECT * FROM players")
    players = cur.fetchall()
    return [player_to_dict(player) for player in players]
 except Exception as e: 
  raise 

def get_player(player_id:  int, conn)->Dict [str, Any]: 
  try: 
    with conn.cursor() as cur: cur.execute(
    "SELECT * FROM players WHERE id = %s",
    (player_id,)) 
    player = cur.fetchone() 
    if player: return player_to_dict(player) 
    return None
  except Exception as e: 
    raise 
  

def update_player(player_id: int, player: Dict [str, Any], conn)->Dict [str, Any]: 
    try: 
      with conn.cursor() as cur: cur.execute(""" UPDATE   players SET
          name = %s,
          role = %s,
          batting_style = %s,
          bowling_style = %s,
          matches = %s,
          runs = %s,
          average = %s,
          strike_rate = %s,
          image_url = %s
          WHERE id = %s
          RETURNING *
          """,
          (
            player ["name"],
            player ["role"],
            player ["batting_style"],
            player ["bowling_style"],
            player ["matches"],
            player ["runs"],
            player ["average"],
            player ["strike_rate"],
            player ["image_url"],
            player_id
            )
          ) 
      updated_player = cur.fetchone() 
      conn.commit() 
      if updated_player: 
        return player_to_dict(updated_player) 
      return None
    except Exception as e: conn.rollback() 
    raise 
  
def delete_player(player_id: int, conn)->bool: 
    try: 
      with conn.cursor() as cur: cur.execute(
      "DELETE FROM players WHERE id = %s",
        (player_id,)
      ) 
      conn.commit() 
      return cur.rowcount > 0
    except Exception as e: conn.rollback() 
    raise