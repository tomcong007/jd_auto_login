import json
class JSONUtil():
    @staticmethod
    def prettty_format(dict):
        return json.dumps(dict, indent=4, ensure_ascii=False)
