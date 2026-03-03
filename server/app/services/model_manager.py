import os
import json

MODELS_DIR = os.path.join(os.path.dirname(__file__), "../data/models")

class ModelManager:
    def __init__(self):
        # scan models folder at startup
        self.registry = {}  # model_name -> json_path
        self._build_registry()

    def _build_registry(self):
        files = os.listdir(MODELS_DIR)
        # only json files ending with _info.json
        for f in files:
            if f.endswith("_info.json"):
                model_name = f.replace("_info.json", "")
                self.registry[model_name] = os.path.join(MODELS_DIR, f)

    def get_info_by_name(self, model_name: str):
        path = self.registry.get(model_name)
        if not path or not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return json.load(f)

    def list_models(self):
        return list(self.registry.keys())

    def get_all_infos(self) -> list:
        """
        Returns a list of all model info JSON objects.
        """
        infos = []
        for model_name in self.list_models():
            info = self.get_info_by_name(model_name)
            if info:
                infos.append(info)
        return infos

# singleton instance
model_manager = ModelManager()