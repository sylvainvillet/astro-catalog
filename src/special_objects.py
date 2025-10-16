class SpecialObject:
    def __init__(self, *, numbers: list[int], x: int, y: int, width: int, height: int):
        self.numbers = numbers
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def cells(self) -> int:
        return self.width * self.height
    
    def objects(self) -> int:
        return len(self.numbers)

    def __repr__(self):
        return (f"SpecialObject(numbers={self.numbers}, x={self.x}, y={self.y}, "
                f"width={self.width}, height={self.height})")
    
    def to_dict(self) -> dict[str, list[int] | int]:
        return {
            "numbers": self.numbers,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
    
    @classmethod
    def from_dict(cls, d: dict[str, list[int] | int]) -> "SpecialObject":
        return cls(
            numbers=d.get("numbers", []),
            x=d.get("x", 0),
            y=d.get("y", 0),
            width=d.get("width", 1),
            height=d.get("height", 1),
        )