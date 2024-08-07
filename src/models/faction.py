class Faction:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"Name: {self.name}\nDescription: {self.description}"

    def __repr__(self) -> str:
        return f"Faction(name={self.name}, description={self.description})"
