# -*- coding: utf-8 -*- 
"""
========================================================================================================================
@project : my-sanic
@file: myDataUtils
@Author: mengying
@email: 652044581@qq.com
@date: 2023/3/23 15:54
@desc: 数据的处理类
========================================================================================================================
"""
import jmespath


class JsonLocator:
    """
    json数据指定位置的快速查询
    使用教程参见： https://blog.csdn.net/be5yond/article/details/118976017
    """

    def __init__(self, json_data):
        self.json_data = json_data

    def locate(self, query):
        return jmespath.search(query, self.json_data)


class JsonEditor:
    """json数据指定位置的快速修改"""

    def __init__(self, json_data):
        self.json_data = json_data

    def edit(self, path, new_value):
        keys = path.split('.')
        data = self.json_data
        for index, key in enumerate(keys):
            if key.isdigit():
                keys[index] = int(key)
        for key in keys[:-1]:
            data = data[key]
        data[keys[-1]] = new_value


class JsonModifier:
    """json数据删除value的bool值是false的值, indent为True只控制第一层级，False删除json全部层级"""

    @staticmethod
    def deleteBoolKey(json_data, indent=True):
        if isinstance(json_data, dict):
            for key, value in list(json_data.items()):
                if not bool(value):
                    del json_data[key]
                    if indent:
                        return json_data
                else:
                    JsonModifier.deleteBoolKey(value)
        elif isinstance(json_data, list):
            for item in json_data:
                JsonModifier.deleteBoolKey(item)
        return json_data


class JsonValidator:
    """校验json数据是否包含列表字段"""

    def __init__(self, json_data, fields_list):
        self.json_data = json_data
        self.fields_list = fields_list

    def validate(self):
        for field in self.fields_list:
            if field not in self.json_data:
                return False
        return True


class JsonComparator:
    """比较2个json数据是否包含"""

    def __init__(self, big_json, small_json):
        self.big_json = big_json
        self.small_json = small_json

    def compare(self):
        for key, value in self.small_json.items():
            if key not in self.big_json:
                return False
            if isinstance(value, dict):
                if not JsonComparator(self.big_json[key], value).compare():
                    return False
            elif self.big_json[key] != value:
                return False
        return True


class JsonDiff:
    """比较2个json数据，返回json diff的差异数据"""

    def __init__(self, origin_json, diff_json):
        self.origin_json = origin_json
        self.diff_json = diff_json
        self.container = {}

    def compare(self):
        for key, value in self.origin_json.items():
            diff_value = self.diff_json.get(key)
            if diff_value is not None and value != diff_value:
                self.container[key] = value
        return self.container


class JsonRemover:
    """删除指定列表，json里面的key"""

    def __init__(self, json_data):
        self.json_data = json_data

    def remove_fields(self, fields_to_remove):
        json_keys = self.json_data.keys()
        for field in fields_to_remove:
            if field in json_keys:
                self.json_data.pop(field, None)
        return self.json_data


class JsonKeeper:
    """只保留指定列表，json里面的key"""

    def __init__(self, json_data):
        self.json_data = json_data
        self.container = {}

    def keeper_fields(self, fields_to_keeper):
        json_keys = self.json_data.keys()
        for field in fields_to_keeper:
            if field in json_keys:
                self.container[field] = self.json_data[field]
        return self.container


class JsonSwap:
    """交换json的键值的位置"""

    def __init__(self, json_data):
        self.json_data = json_data

    def swap(self):
        return {v: k for k, v in self.json_data.items()}


class ListFilter:
    """过滤数据结构 list[dict]中dict满足某种条件的数据"""

    def __init__(self, data, condition):

        self.data = data
        self.condition = condition
        self.keeper = []
        self.filter = []

    def filter(self, reverse=False):
        for item in self.data:
            threshold = JsonComparator(big_json=item, small_json=self.condition).compare()
            if not threshold:
                self.keeper.append(threshold)
            else:
                self.filter.append(threshold)
        return self.keeper if reverse else self.filter


class List2Dict:
    """把list[dict]合并成dict, 注：如果dict里面存在相同字段会被覆盖，特定数据结构使用"""

    def __init__(self, data_list):
        self.data_list = data_list
        self.container = {}

    def merge(self):
        for d in self.data_list:
            self.container.update(d)
        return self.container


class TreeBuilder:
    """列表数据根据指定的parentId和字数的id组装成关系树"""

    def __init__(self, data):
        self.data: list = data
        self.tree: dict = {}

    def build(self, parentKey: str = "parentId", ownerKey: str = "id", topParent: str = None):
        node_dict = {item[ownerKey]: item for item in self.data}
        for item in self.data:
            if item[parentKey] is topParent:
                self.tree[item[ownerKey]] = item
            else:
                parent = node_dict.get(item[parentKey])
                if parent:
                    if 'children' not in parent:
                        parent['children'] = []
                    parent['children'].append(item)
        return self.tree


if __name__ == '__main__':
    # Example 1  JsonLocator
    json_data = {
        "name": {
            "first": "John",
            "last": "Doe"
        },
        "age": 25,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345"
        }
    }

    locator = JsonLocator(json_data)
    print(locator.locate("name.first"))  # Output: John

    # Example 1  JsonEditor
    json_data = {
        "name": "John",
        "age": 30,
        "cars": {
            "car1": "Ford",
            "car2": "BMW",
            "car3": "Fiat"
        }
    }
    editor = JsonEditor(json_data)
    editor.edit('cars.car2', 'Mercedes')
    print(json_data)

    # Example 2  JsonEditor
    json_data = {
        "name": "John",
        "age": 30,
        "cars": [
            {"name": "Ford", "models": ["Fiesta", "Focus", "Mustang"]},
            {"name": "BMW", "models": ["320", "X3", "X5"]},
            {"name": "Fiat", "models": ["500", "Panda"]}
        ]
    }
    editor = JsonEditor(json_data)
    editor.edit('cars.1.models.2', 'X6')
    print(json_data)

    # Example 3  JsonEditor
    json_data = {
        "name": "John",
        "age": 30,
        "address": {
            "street": "Main Street",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        }
    }
    editor = JsonEditor(json_data)
    editor.edit('address.zip', '10002')
    print(json_data)

    # Example 1  JsonModifier
    json_data = {
        "name": "John",
        "age": 30,
        "married": "",
        "pets": [
            {
                "animal": "1",
                "name": "Fido",
                "is_alive": True
            },
            {
                "animal": "cat",
                "name": "Fluffy",
                "is_alive": {}
            }
        ]
    }

    json_data = JsonModifier.deleteBoolKey(json_data, indent=False)
    print(json_data)

    data = [{'id': '1739096268195635200', 'parentId': '0', 'component': 'Layout', 'hidden': False, 'path': '/system', 'name': 'System', 'redirect': 'noRedirect', 'meta': {'icon': 'system', 'link': '', 'noCache': False, 'title': '系统管理'}}, {'id': '1739096268195635201', 'parentId': '1739096268195635200', 'component': '0', 'hidden': False, 'path': 'user', 'name': 'User', 'redirect': 'noRedirect', 'meta': {'icon': 'user', 'link': '', 'noCache': False, 'title': '用户管理'}}, {'id': '1739096268195635202', 'parentId': '1739096268195635200', 'component': '0', 'hidden': False, 'path': 'role', 'name': 'Role', 'redirect': 'noRedirect', 'meta': {'icon': 'peoples', 'link': '', 'noCache': False, 'title': '角色管理'}}, {'id': '1739096268195635203', 'parentId': '1739096268195635200', 'component': '0', 'hidden': False, 'path': 'menu', 'name': 'Menu', 'redirect': 'noRedirect', 'meta': {'icon': 'tree-table', 'link': '', 'noCache': False, 'title': '菜单管理'}}, {'id': '1739096268195635204', 'parentId': '1739096268195635200', 'component': '0', 'hidden': False, 'path': 'dept', 'name': 'Dept', 'redirect': 'noRedirect', 'meta': {'icon': 'tree', 'link': '', 'noCache': False, 'title': '部门管理'}}]
    print(TreeBuilder(data).build(parentKey="parentId", ownerKey="id", topParent="0"))
