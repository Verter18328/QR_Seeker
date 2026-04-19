from .database_connection import database_conn
from .global_config import global_config


class Player:
    def __init__(self, id=None, name=None, password_hash=None, token=None, points=None):
        self.id = id
        self.name = name
        self.password_hash = password_hash
        self.token = token
        self.points = points
    @staticmethod
    def get_player_by_token(token):
        query = "SELECT id, nickname, password_hash, token, points FROM players WHERE token = %s"
        result = database_conn.execute_query(query, (token,))
        if result:
            return Player(id=result[0]['id'], name=result[0]['nickname'], password_hash=result[0]['password_hash'], token=result[0]['token'], points=result[0]['points'])
        return None
    @staticmethod
    def get_player_by_name(name):
        query = "SELECT id, nickname, password_hash, token, points FROM players WHERE nickname = %s"
        result = database_conn.execute_query(query, (name,))
        if result:
            return Player(id=result[0]['id'], name=result[0]['nickname'], password_hash=result[0]['password_hash'], token=result[0]['token'], points=result[0]['points'])
        return None
    @staticmethod
    def get_leaderboard(limit):
        query = "SELECT nickname, points, RANK() OVER (ORDER BY points DESC) as rank FROM players LIMIT %s"
        result = database_conn.execute_query(query, (limit,))
        if result:
            leaderboard = [{"nickname": row["nickname"], "points": row["points"], "rank": row["rank"]} for row in result]
            return leaderboard
        return None
    def save_player(self):
        query = "INSERT INTO players (nickname, password_hash, token) VALUES (%s, %s, %s) RETURNING id"
        params = (self.name, self.password_hash, self.token)
        result = database_conn.execute_query(query, params)
        if result:
            self.id = result['id']
            return self
        return None
    def update_points(self, points):
        query = "UPDATE players SET points = points + %s WHERE id = %s"
        database_conn.execute_query(query, (points, self.id))
        self.points += points