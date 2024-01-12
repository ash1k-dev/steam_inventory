TEST_DATA_STEAM_ID_CASE_1 = {"response": {"steamid": "76561198044176118", "success": 1}}

RESULT_TEST_STEAM_ID_CASE_1 = 76561198044176118

TEST_DATA_STEAM_ID_CASE_2 = {"response": {"steamid": "76561199004706307", "success": 1}}

RESULT_TEST_STEAM_ID_CASE_2 = 76561199004706307


LIST_STEAM_ID = [
    (
        TEST_DATA_STEAM_ID_CASE_1,
        RESULT_TEST_STEAM_ID_CASE_1,
    ),
    (
        TEST_DATA_STEAM_ID_CASE_2,
        RESULT_TEST_STEAM_ID_CASE_2,
    ),
]

TEST_DATA_STEAM_NAME_CASE_1 = {
    "response": {
        "players": [
            {
                "steamid": "76561198155948643",
                "communityvisibilitystate": 3,
                "profilestate": 1,
                "personaname": "ash",
                "commentpermission": 1,
                "profileurl": "https://steamcommunity.com/profiles/76561198155948643/",
                "avatar": "https://avatars.steamstatic.com/113073803ab5e610b12694d977910e934f780f0d.jpg",
                "avatarmedium": "https://avatars.steamstatic.com/113073803ab5e610b12694d977910e934f780f0d_medium.jpg",
                "avatarfull": "https://avatars.steamstatic.com/113073803ab5e610b12694d977910e934f780f0d_full.jpg",
                "avatarhash": "113073803ab5e610b12694d977910e934f780f0d",
                "lastlogoff": 1677856308,
                "personastate": 0,
                "primaryclanid": "103582791456313482",
                "timecreated": 1411663899,
                "personastateflags": 0,
            }
        ]
    }
}

RESULT_TEST_STEAM_NAME_CASE_1 = "ash"

TEST_DATA_STEAM_NAME_CASE_2 = {
    "response": {
        "players": [
            {
                "steamid": "76561198044176118",
                "communityvisibilitystate": 3,
                "profilestate": 1,
                "personaname": "Deny_X one",
                "commentpermission": 1,
                "profileurl": "https://steamcommunity.com/id/denykill/",
                "avatar": "https://avatars.steamstatic.com/2dcb3ad9460375e70bb95d98c1467059e0cb4f34.jpg",
                "avatarmedium": "https://avatars.steamstatic.com/2dcb3ad9460375e70bb95d98c1467059e0cb4f34_medium.jpg",
                "avatarfull": "https://avatars.steamstatic.com/2dcb3ad9460375e70bb95d98c1467059e0cb4f34_full.jpg",
                "avatarhash": "2dcb3ad9460375e70bb95d98c1467059e0cb4f34",
                "lastlogoff": 1704584568,
                "personastate": 0,
                "primaryclanid": "103582791456313482",
                "timecreated": 1309189616,
                "personastateflags": 0,
                "loccountrycode": "RU",
                "locstatecode": "71",
                "loccityid": 43379,
            }
        ]
    }
}

RESULT_TEST_STEAM_NAME_CASE_2 = "Deny_X one"

TEST_DATA_STEAM_NAME_CASE_3 = {
    "response": {
        "players": [
            {
                "steamid": "76561199004706307",
                "communityvisibilitystate": 3,
                "profilestate": 1,
                "personaname": "LOLIBOOMKA",
                "commentpermission": 1,
                "profileurl": "https://steamcommunity.com/id/loliboomka/",
                "avatar": "https://avatars.steamstatic.com/de74427bfb640e47567f9d5808a2d786203f723f.jpg",
                "avatarmedium": "https://avatars.steamstatic.com/de74427bfb640e47567f9d5808a2d786203f723f_medium.jpg",
                "avatarfull": "https://avatars.steamstatic.com/de74427bfb640e47567f9d5808a2d786203f723f_full.jpg",
                "avatarhash": "de74427bfb640e47567f9d5808a2d786203f723f",
                "lastlogoff": 1704486552,
                "personastate": 0,
                "realname": "Ksusha",
                "primaryclanid": "103582791456313482",
                "timecreated": 1574277183,
                "personastateflags": 0,
                "loccountrycode": "RU",
            }
        ]
    }
}

RESULT_TEST_STEAM_NAME_CASE_3 = "LOLIBOOMKA"


LIST_STEAM_NAME = [
    (
        TEST_DATA_STEAM_NAME_CASE_1,
        RESULT_TEST_STEAM_NAME_CASE_1,
    ),
    (
        TEST_DATA_STEAM_NAME_CASE_2,
        RESULT_TEST_STEAM_NAME_CASE_2,
    ),
    (
        TEST_DATA_STEAM_NAME_CASE_3,
        RESULT_TEST_STEAM_NAME_CASE_3,
    ),
]
