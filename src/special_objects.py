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