TEST_DATA_USER = {
    "name": "test_name_1",
    "telegram_id": 111,
    "steam_id": 1111,
    "steam_name": "test_steam_name_1",
}


TEST_DATA_ALL_GAMES_INFO = {
    12210: {
        "name": "Grand Theft Auto IV: The Complete Edition",
        "time": 1.0,
        "cost": 0,
    },
    214360: {"name": "Tower Wars", "time": 5.9, "cost": 18900},
    72850: {"name": "The Elder Scrolls V: Skyrim", "time": 57.3, "cost": 0},
    10: {"name": "Counter-Strike", "time": 0.9, "cost": 25900},
    20: {"name": "Team Fortress Classic", "time": 0, "cost": 20000},
    30: {"name": "Day of Defeat", "time": 0, "cost": 20000},
    40: {"name": "Deathmatch Classic", "time": 0, "cost": 20000},
    50: {"name": "Half-Life: Opposing Force", "time": 0, "cost": 20000},
    60: {"name": "Ricochet", "time": 0, "cost": 20000},
    70: {"name": "Half-Life", "time": 0, "cost": 25900},
    80: {"name": "Counter-Strike: Condition Zero", "time": 0, "cost": 25900},
    100: {
        "name": "Counter-Strike: Condition Zero Deleted Scenes",
        "time": 0,
        "cost": 25900,
    },
    130: {"name": "Half-Life: Blue Shift", "time": 0, "cost": 20000},
    220: {"name": "Half-Life 2", "time": 0, "cost": 38500},
    240: {"name": "Counter-Strike: Source", "time": 0, "cost": 38500},
    280: {"name": "Half-Life: Source", "time": 0, "cost": 38500},
    300: {"name": "Day of Defeat: Source", "time": 0, "cost": 38500},
    320: {"name": "Half-Life 2: Deathmatch", "time": 0, "cost": 20000},
    340: {"name": "Half-Life 2: Lost Coast", "time": 0, "cost": 0},
    360: {"name": "Half-Life Deathmatch: Source", "time": 0, "cost": 38500},
    380: {"name": "Half-Life 2: Episode One", "time": 0, "cost": 32000},
    400: {"name": "Portal", "time": 0, "cost": 38500},
    420: {"name": "Half-Life 2: Episode Two", "time": 0, "cost": 32000},
    500: {"name": "Left 4 Dead", "time": 0.1, "cost": 38500},
    550: {"name": "Left 4 Dead 2", "time": 0, "cost": 38500},
    620: {"name": "Portal 2", "time": 0, "cost": 38500},
    730: {"name": "Counter-Strike 2", "time": 2064.7, "cost": 0},
    252170: {"name": "Anomaly Warzone Earth Mobile Campaign", "time": 0, "cost": 2100},
    222900: {"name": "Dead Island: Epidemic", "time": 0.3, "cost": 0},
    316010: {"name": "Magic Duels", "time": 0, "cost": 0},
    257400: {"name": "Fuse", "time": 0.1, "cost": 0},
    489830: {
        "name": "The Elder Scrolls V: Skyrim Special Edition",
        "time": 130.1,
        "cost": 0,
    },
    304390: {"name": "For Honor", "time": 0, "cost": 0},
    654310: {"name": "For Honor - Public Test", "time": 0, "cost": 0},
}

TEST_DATA_GAMES = [
    (550, "Left 4 Dead 2", 38500, 0, 38500),
    (620, "Portal 2", 38500, 0, 38500),
    (220, "Half-Life 2", 38500, 0, 38500),
    (240, "Counter-Strike: Source", 38500, 0, 38500),
    (280, "Half-Life: Source", 38500, 0, 38500),
    (300, "Day of Defeat: Source", 38500, 0, 38500),
    (360, "Half-Life Deathmatch: Source", 38500, 0, 38500),
    (400, "Portal", 38500, 0, 38500),
    (500, "Left 4 Dead", 38500, 0, 38500),
    (380, "Half-Life 2: Episode One", 32000, 0, 32000),
    (420, "Half-Life 2: Episode Two", 32000, 0, 32000),
    (100, "Counter-Strike: Condition Zero Deleted Scenes", 25900, 0, 25900),
    (70, "Half-Life", 25900, 0, 25900),
    (80, "Counter-Strike: Condition Zero", 25900, 0, 25900),
    (10, "Counter-Strike", 25900, 0, 25900),
    (320, "Half-Life 2: Deathmatch", 20000, 0, 20000),
    (130, "Half-Life: Blue Shift", 20000, 0, 20000),
    (60, "Ricochet", 20000, 0, 20000),
    (40, "Deathmatch Classic", 20000, 0, 20000),
    (50, "Half-Life: Opposing Force", 20000, 0, 20000),
    (20, "Team Fortress Classic", 20000, 0, 20000),
    (30, "Day of Defeat", 20000, 0, 20000),
    (214360, "Tower Wars", 18900, 5, 18900),
    (252170, "Anomaly Warzone Earth Mobile Campaign", 2100, 0, 2100),
    (654310, "For Honor - Public Test", 0, 0, 0),
    (72850, "The Elder Scrolls V: Skyrim", 0, 57, 0),
    (340, "Half-Life 2: Lost Coast", 0, 0, 0),
    (730, "Counter-Strike 2", 0, 2064, 0),
    (222900, "Dead Island: Epidemic", 0, 0, 0),
    (316010, "Magic Duels", 0, 0, 0),
    (257400, "Fuse", 0, 0, 0),
    (489830, "The Elder Scrolls V: Skyrim Special Edition", 0, 130, 0),
    (304390, "For Honor", 0, 0, 0),
    (12210, "Grand Theft Auto IV: The Complete Edition", 0, 1, 0),
]

TEST_DATA_GAMES_INFO = [(34, 675100, 2257)]

TEST_DATA_GAMES_COUNT = 34

TEST_DATA_GAMES_ADD = {
    2143601: {"name": "Tower Wars", "cost": 8900},
    101: {"name": "Counter-Strike", "cost": 5900},
    701: {"name": "Half-Life", "cost": 5900},
}

LIST_GAMES_CRUD = [
    (
        TEST_DATA_USER,
        TEST_DATA_ALL_GAMES_INFO,
        TEST_DATA_GAMES,
        TEST_DATA_GAMES_INFO,
        TEST_DATA_GAMES_COUNT,
        TEST_DATA_GAMES_ADD,
    )
]


TEST_DATA_ALL_TRACKING_GAMES_INFO = {
    214360: {"name": "Tower Wars", "time": 5.9, "first_cost": 18900, "cost": 8900},
    10: {"name": "Counter-Strike", "time": 0.9, "first_cost": 25900, "cost": 5900},
    70: {"name": "Half-Life", "time": 0, "first_cost": 25900, "cost": 5900},
}

TEST_DATA_TRACKING_GAMES_LONG = 3


TEST_DATA_TRACKING_GAMES_CHANGES = [
    ("Tower Wars", 214360, 18900, 8900),
    ("Counter-Strike", 10, 25900, 5900),
    ("Half-Life", 70, 25900, 5900),
]

TEST_DATA_TRACKING_GAMES_COST_BEFORE_DECREASE = {214360: 18900, 10: 25900, 70: 25900}

TEST_DATA_TRACKING_GAMES_NAME = {
    214360: "Tower Wars",
    10: "Counter-Strike",
    70: "Half-Life",
}


LIST_TRACKING_GAMES_CRUD = [
    (
        TEST_DATA_USER,
        TEST_DATA_ALL_TRACKING_GAMES_INFO,
        TEST_DATA_TRACKING_GAMES_LONG,
        TEST_DATA_TRACKING_GAMES_CHANGES,
    )
]
