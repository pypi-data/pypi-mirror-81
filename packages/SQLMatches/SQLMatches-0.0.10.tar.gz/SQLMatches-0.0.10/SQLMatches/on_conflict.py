# -*- coding: utf-8 -*-

"""
GNU General Public License v3.0 (GPL v3)
Copyright (c) 2020-2020 WardPearce
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.dialects.postgresql import insert as postgresql_insert

from .tables import scoreboard
from .resources import Config


def player_insert_on_conflict_update():
    if Config.db_engine == "mysql":
        query_insert = mysql_insert(scoreboard)
        return query_insert.on_duplicate_key_update(
            name=query_insert.inserted.name,
            team=query_insert.inserted.team,
            alive=query_insert.inserted.alive,
            ping=query_insert.inserted.ping,
            kills=query_insert.inserted.kills,
            headshots=query_insert.inserted.headshots,
            assists=query_insert.inserted.assists,
            deaths=query_insert.inserted.deaths,
            shots_fired=query_insert.inserted.shots_fired,
            shots_hit=query_insert.inserted.shots_hit,
            mvps=query_insert.inserted.mvps,
            score=query_insert.inserted.score,
            disconnected=query_insert.inserted.disconnected
        )
    elif Config.db_engine == "psycopg2":
        query_insert = postgresql_insert(scoreboard)
        return postgresql_insert(scoreboard).on_conflict_do_update(
            set_=dict(
                name=query_insert.inserted.name,
                team=query_insert.inserted.team,
                alive=query_insert.inserted.alive,
                ping=query_insert.inserted.ping,
                kills=query_insert.inserted.kills,
                headshots=query_insert.inserted.headshots,
                assists=query_insert.inserted.assists,
                deaths=query_insert.inserted.deaths,
                shots_fired=query_insert.inserted.shots_fired,
                shots_hit=query_insert.inserted.shots_hit,
                mvps=query_insert.inserted.mvps,
                score=query_insert.inserted.score,
                disconnected=query_insert.inserted.disconnected
            )
        )
    else:
        return scoreboard.insert
