class SkillNotFoundError(Exception):
    def __init__(self, identifier: str | int):
        super().__init__(f"Skill with identifier '{identifier}' not found.")

class SkillAlreadyExistsError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Skill with name '{name}' already exists.")