class ProjectNotFoundError(Exception):
    def __init__(self, identifier: str):
        super().__init__(f"Project with identifier '{identifier}' not found.")