TEST_DATA_USER = [
    {"name": "test_name_1", "telegram_id": 111},
    {"name": "test_name_2", "telegram_id": 222},
    {"name": "test_name_3", "telegram_id": 333},
]

TEST_DATA_TELEGRAM_ID_USER_NOT_EXIST = 444

TEST_RESULT_TEST_USERS_CRUD_LEN = 3


LIST_USER_CRUD = [
    (
        TEST_DATA_USER,
        TEST_RESULT_TEST_USERS_CRUD_LEN,
        TEST_DATA_TELEGRAM_ID_USER_NOT_EXIST,
    ),
]


TEST_DATA_STEAM_ID = [
    {"steam_name": "test_name_1", "steam_id": 1111, "telegram_id": 111},
    {"steam_name": "test_name_2", "steam_id": 2222, "telegram_id": 111},
    {"steam_name": "test_name_3", "steam_id": 3333, "telegram_id": 111},
]

TEST_RESULT_TEST_STEAM_ID_CRUD_LEN_BEFORE_DELETE = 3

TEST_RESULT_TEST_STEAM_ID_CRUD_LEN_AFTER_DELETE = 2

TEST_DATA_STEAM_ID_NOT_EXIST = 444

LIST_STEAM_ID_CRUD = [
    (
        TEST_DATA_STEAM_ID,
        TEST_RESULT_TEST_STEAM_ID_CRUD_LEN_BEFORE_DELETE,
        TEST_RESULT_TEST_STEAM_ID_CRUD_LEN_AFTER_DELETE,
        TEST_DATA_STEAM_ID_NOT_EXIST,
    ),
]


TEST_DATA_INVENTORY = {
    "name": "test_name_1",
    "steam_name": "test_steam_name_1",
    "steam_id": 1111,
    "telegram_id": 111,
}


TEST_DATA_INVENTORY_ALL_GAMES_INFO = {
    12210: {
        "name": "Grand Theft Auto IV: The Complete Edition",
        "time": 1.0,
        "cost": 0,
    },
    214360: {"name": "Tower Wars", "time": 5.9, "cost": 18900},
    72850: {"name": "The Elder Scrolls V: Skyrim", "time": 57.3, "cost": 0},
    10: {"name": "Counter-Strike", "time": 0.9, "cost": 25900},
    70: {"name": "Half-Life", "time": 0, "cost": 25900},
    730: {"name": "Counter-Strike Global", "time": 41.7, "cost": 0},
}

TEST_RESULT_INVENTORY_LEN_ALL_GAMES_INFO_BEFORE_DELETE = len(
    TEST_DATA_INVENTORY_ALL_GAMES_INFO
)

TEST_RESULT_INVENTORY_LEN_ALL_GAMES_INFO_AFTER_DELETE = 0

TEST_DATA_INVENTORY_NOT_EXIST = 1555

LIST_INVENTORY_CRUD = [
    (
        TEST_DATA_INVENTORY,
        TEST_DATA_INVENTORY_ALL_GAMES_INFO,
        TEST_RESULT_INVENTORY_LEN_ALL_GAMES_INFO_BEFORE_DELETE,
        TEST_RESULT_INVENTORY_LEN_ALL_GAMES_INFO_AFTER_DELETE,
        TEST_DATA_INVENTORY_NOT_EXIST,
    ),
]
