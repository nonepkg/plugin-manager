import os
import json

_DATA_PATH = os.path.join("data", "manager", "setting.json")

# 更新默认设置
def update_default_setting(plugin_list: list):
    if os.path.exists(_DATA_PATH):
        old_setting = load_setting(0)
        new_setting = {}
        for plugin in plugin_list:
            if plugin in old_setting:
                new_setting[plugin] = old_setting[plugin]
            else:
                new_setting[plugin] = True
        update_setting(0, new_setting)
    else:
        os.makedirs(os.path.dirname(_DATA_PATH), exist_ok=True)
        full_setting = {"0": {}}
        for plugin in plugin_list:
            full_setting["0"][plugin] = True
        json.dump(
            full_setting,
            open(_DATA_PATH, "w", encoding="utf-8"),
            indent=4,
            separators=(",", ": "),
        )


# 获取指定群的设置，如果获取不到则采用默认设置
def load_setting(group_id: int) -> dict:
    full_setting = json.load(open(_DATA_PATH, "r", encoding="utf-8"))
    if str(group_id) not in full_setting:
        return full_setting["0"]
    return full_setting[str(group_id)]


# 更新指定群的设置
def update_setting(group_id: int, setting: dict):
    full_setting = json.load(open(_DATA_PATH, "r", encoding="utf-8"))
    full_setting[str(group_id)] = setting
    json.dump(
        full_setting,
        open(_DATA_PATH, "w", encoding="utf-8"),
        indent=4,
        separators=(",", ": "),
    )
