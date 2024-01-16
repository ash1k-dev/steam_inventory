from core.tests.test_steam.test_games.games_test_data import RESULT_TEST_ALL_GAMES_INFO

TEST_DATA_USER_CRUD = [
    {"name": "test_name_1", "telegram_id": 111},
    {"name": "test_name_2", "telegram_id": 222},
    {"name": "test_name_3", "telegram_id": 333},
]

TEST_DATA_TELEGRAM_ID_USER_NOT_EXIST = 444

RESULT_TEST_USERS_CRUD_LEN = 3


LIST_USER_CRUD = [
    (
        TEST_DATA_USER_CRUD,
        RESULT_TEST_USERS_CRUD_LEN,
        TEST_DATA_TELEGRAM_ID_USER_NOT_EXIST,
    ),
]


TEST_DATA_STEAM_ID_CRUD = [
    {"steam_name": "test_name_1", "steam_id": 1111, "telegram_id": 111},
    {"steam_name": "test_name_2", "steam_id": 2222, "telegram_id": 111},
    {"steam_name": "test_name_3", "steam_id": 3333, "telegram_id": 111},
]

RESULT_TEST_STEAM_ID_CRUD_LEN_BEFORE_DELETE = 3

RESULT_TEST_STEAM_ID_CRUD_LEN_AFTER_DELETE = 2

TEST_DATA_STEAM_ID_NOT_EXIST = 444

LIST_STEAM_ID_CRUD = [
    (
        TEST_DATA_STEAM_ID_CRUD,
        RESULT_TEST_STEAM_ID_CRUD_LEN_BEFORE_DELETE,
        RESULT_TEST_STEAM_ID_CRUD_LEN_AFTER_DELETE,
        TEST_DATA_STEAM_ID_NOT_EXIST,
    ),
]


TEST_DATA_INVENTORY_CRUD = {
    "steam_name": "test_name_1",
    "steam_id": 1111,
    "telegram_id": 111,
}


TEST_DATA_INVENTORY_ALL_GAMES_INFO = RESULT_TEST_ALL_GAMES_INFO

TEST_DATA_INVENTORY_LEN_ALL_GAMES_INFO_BEFORE_DELETE = len(RESULT_TEST_ALL_GAMES_INFO)

TEST_DATA_INVENTORY_LEN_ALL_GAMES_INFO_AFTER_DELETE = 0

TEST_DATA_INVENTORY_NOT_EXIST = 1555

LIST_INVENTORY_CRUD = [
    (
        TEST_DATA_INVENTORY_CRUD,
        TEST_DATA_INVENTORY_ALL_GAMES_INFO,
        TEST_DATA_INVENTORY_LEN_ALL_GAMES_INFO_BEFORE_DELETE,
        TEST_DATA_INVENTORY_LEN_ALL_GAMES_INFO_AFTER_DELETE,
        TEST_DATA_INVENTORY_NOT_EXIST,
    ),
]
