import psycopg2

# Database connection configuration
db_config = {
    'dbname': 'esport',
    'user': 'miza1',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# SQL statements for table creation
sql_statements = [
    """
    CREATE TABLE public.players (
        id SERIAL PRIMARY KEY,
        Name VARCHAR(100),
        Kda FLOAT,
        openRating FLOAT,
        pistolRating FLOAT,
        rating FLOAT
    );
    """,
    """
    CREATE TABLE public.teams (
        id SERIAL PRIMARY KEY,
        Team_name VARCHAR(100)
    );
    """,
    """
    CREATE TABLE public.teamplayers (
        player_id INT,
        team_id INT,
        PRIMARY KEY (player_id, team_id),
        FOREIGN KEY (player_id) REFERENCES public.players(id),
        FOREIGN KEY (team_id) REFERENCES public.teams(id)
    );
    """,
    """
    CREATE TABLE public.teamstats (
        id SERIAL PRIMARY KEY,
        team_id INT UNIQUE,
        kda FLOAT,
        last10matches FLOAT,
        openRating FLOAT,
        pistolRating FLOAT,
        Rating FLOAT,
        FOREIGN KEY (team_id) REFERENCES public.teams(id)
    );
    """,
    """
    CREATE TABLE public.matches (
        id SERIAL PRIMARY KEY,
        team1_id INT,
        team2_id INT,
        scoreTeam1 INT,
        scoreTeam2 INT,
        FOREIGN KEY (team1_id) REFERENCES public.teams(id),
        FOREIGN KEY (team2_id) REFERENCES public.teams(id)
    );
    """
]

# Connect to the database and execute the SQL statements
try:
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            for sql in sql_statements:
                cursor.execute(sql)
            print("Tables created successfully!")
except Exception as e:
    print("An error occurred:", e)