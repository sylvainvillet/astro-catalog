from src.special_objects import SpecialObject

messier_layout: list[SpecialObject] = [
    SpecialObject(numbers=[8, 20],       x=2, y=2, width=2, height=3),   # Lagoon Nebula
    SpecialObject(numbers=[16],          x=14, y=2, width=2, height=2),  # Eagle Nebula
    SpecialObject(numbers=[31, 32, 110], x=7, y=2, width=4, height=2),   # Andromeda
    SpecialObject(numbers=[33],          x=1, y=6, width=3, height=2),   # Triangulum Galaxy
    SpecialObject(numbers=[42, 43],      x=6, y=5, width=2, height=3),   # Orion Nebula
    SpecialObject(numbers=[45],          x=13, y=5, width=2, height=2),  # Pleiades
]

caldwell_layout: list[SpecialObject] = [
    SpecialObject(numbers=[20], x=1, y=1, width=3, height=2),   # North America Nebula
    SpecialObject(numbers=[33], x=14, y=1, width=2, height=3),  # Veil Nebula
    SpecialObject(numbers=[68], x=7, y=2, width=2, height=2),   # Helix Nebula
    SpecialObject(numbers=[70], x=2, y=4, width=3, height=2),   # NGC 300
    SpecialObject(numbers=[71], x=9, y=5, width=4, height=2),   # Large Magellanic Cloud
    SpecialObject(numbers=[72], x=0, y=7, width=3, height=2),   # Small Magellanic Cloud
    SpecialObject(numbers=[99], x=14, y=6, width=3, height=2),  # Coalsack Nebula
]
