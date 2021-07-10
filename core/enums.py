from enum import Enum
from colorama import Fore, Back

class ConsoleTheme(Enum):
    error   = Fore.RED
    success = Fore.GREEN
    warning = Fore.YELLOW
    info    = ''

class Emoji:
    error    = "<:error:856131306739335198>"
    warning  = "<:warning:856131306777608202>"
    info     = ":information_source:"
    lookup   = ":face_with_monocle:"
    neutral  = "<:neutral:856131307176067076>"
    success  = "<:success:856131306415718420>"
    settings = ":gear:"
    enabled  = ":green_circle:"
    disabled = ":red_circle:"
    channel  = ":hash:"

class Color:
    primary   = 10052333
    secondary = 8232447
    error     = 15417396
    warning   = 15763255
    info      = 4879080
    neutral   = 3092790
    success   = 5038123