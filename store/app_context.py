from typing import Any


class AppContext:
    def __init__(self) -> None:
        self.data = {}

    def set_config(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get_config(self, key: str) -> Any:
        return self.data.get(key)

    def get_configs(self) -> Any:
        return self.data


# Create a global context
app_context: AppContext = AppContext()
