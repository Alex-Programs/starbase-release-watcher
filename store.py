import requests


def get_game_info(appid):
    r = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    data = r.json()[appid]
    return data


def is_released(appid):
    info = get_game_info(appid)
    return info["data"]["release_date"]["coming_soon"] == False


if __name__ == "__main__":
    print(str(is_released("454120")))
