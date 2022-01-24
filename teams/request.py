import sqlite3
import json
from models import Team, TeamScore, Player


def get_teams(filters):
    with sqlite3.connect("./flagons.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        teams = {}

        if filters is None:
            db_cursor.execute("""
            SELECT
                t.id,
                t.name
            FROM Teams t
            """)

            dataset = db_cursor.fetchall()

            teams = []
            for row in dataset:
                team = Team(row['id'], row['name'])
                teams.append(team.__dict__)

            return json.dumps(teams)

        else:
            if "_embed" in filters:
                for related_resource in filters['_embed']['resources']:
                    if related_resource == "teamScores":
                        db_cursor.execute("""
                        SELECT
                            t.id,
                            t.name,
                            ts.id score_id,
                            ts.teamId,
                            ts.score,
                            ts.timeStamp
                        FROM Teams t
                        LEFT JOIN TeamScore ts ON ts.teamId = t.id
                        """)

                        dataset = db_cursor.fetchall()

                        for row in dataset:
                            if row['id'] not in teams:
                                team = Team(row['id'], row['name'])
                                teams[row['id']] = team
                            else:
                                team = teams[row['id']]

                            score = int(
                                row['score']) if row['score'] is not None else 0
                            if score > 0:
                                team_score = TeamScore(
                                    row['score_id'], row['teamId'], score, row['timeStamp'])
                            team.scores.append(team_score.__dict__)

                    elif related_resource == "players":
                        db_cursor.execute("""
                        SELECT
                            t.id,
                            t.name,
                            p.id player_id,
                            p.firstName,
                            p.lastName,
                            p.teamId
                        FROM Teams t
                        JOIN Players p ON p.teamId = t.id
                        """)

                        dataset = db_cursor.fetchall()

                        for row in dataset:
                            if row['id'] not in teams:
                                team = Team(row['id'], row['name'])
                                teams[row['id']] = team
                            else:
                                team = teams[row['id']]

                            player = Player(
                                row['player_id'], row['firstName'], row['lastName'], row['teamId'])
                            team.players.append(player.__dict__)

            json_teams = []
            for team in teams.values():
                json_teams.append(team.__dict__)
            return json.dumps(json_teams)


def add_player(new_player):
    with sqlite3.connect("./flagons.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO players
            (firstName, lastName, teamId)
        VALUES
            (?, ?, ?)
        """, (new_player['firstName'], new_player['lastName'], new_player['teamId']))

        id = db_cursor.lastrowid
        new_player['id'] = id

        return json.dumps(new_player)


def add_team(new_team):
    with sqlite3.connect("./flagons.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO teams
            (name)
        VALUES
            (?)
        """, (new_team['name'], ))

        id = db_cursor.lastrowid
        new_team['id'] = id

        return json.dumps(new_team)


def delete_team(id):
    with sqlite3.connect("./flagons.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM teams
        WHERE id = ?
        """, (id, ))
        db_cursor.execute("""
        DELETE FROM teamscores
        WHERE teamId = ?
        """, (id, ))
        db_cursor.execute("""
        DELETE FROM players
        WHERE teamId = ?
        """, (id, ))
