from enum import Enum

# Will be used to specify whether to create a cartoon-y avatar or something less fun :/
class Mood(Enum):
    FUN = "fun"
    OFFICIAL = "official"

class HeadShape(Enum):
    OVAL = 'oval'
    ROUND = 'round'
    SQUARE = 'square'
    HEART = 'heart'
    TRIANGULAR = 'triangular'

class SkinTone(Enum):
    FAIR = 'fair'
    MEDIUM = 'medium'
    DARK = 'dark'

class SmileType(Enum):
    WIDE = 'wide'
    FULL = 'full'
    CLOSED_LIP = 'closed-lip'
    OPEN_LIP = 'open-lip'
    TEETH_BARING = 'teeth-baring'
    SMIRK = 'smirk'

class NoseType(Enum):
    STRAIGHT = 'straight'
    ROMAN = 'roman'
    BUTTON = 'button'
    SNUB = 'snub'
    WIDE = 'wide'
    NARROW = 'narrow'

class EyeColor(Enum):
    BROWN = 'brown'
    BLUE = 'blue'
    AMBER = 'amber'
    HAZEL = 'hazel'
    GREEN = 'green'
    GREY = 'grey'