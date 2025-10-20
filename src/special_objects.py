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
        numbers = d.get("numbers", [])
        if isinstance(numbers, int):
            numbers = [numbers]
        # No need to check for list, as numbers will be a list or int

        def safe_int(d: dict[str, list[int] | int], key: str, default: int) -> int:
            val = d.get(key, default)
            if isinstance(val, int):
                return val
            if len(val) > 0:
                return val[0]
            return default

        return cls(
            numbers=numbers,
            x=safe_int(d, "x", 1),
            y=safe_int(d, "y", 1),
            width=safe_int(d, "width", 1),
            height=safe_int(d, "height", 1),
        )