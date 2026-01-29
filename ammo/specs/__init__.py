from .basic import DATA as B
from .elements import DATA as E
from .beams import DATA as BE
from .wind import DATA as W
from .venom import DATA as V
from .needle import DATA as ND
from .toast import DATA as TST
from .pollen import DATA as POL
from .wood import DATA as WOOD
from .secret import DATA as SEC
from .magic import DATA as MAG
from .melee import DATA as MEL
from .extensions import DATA as EXT_AMMO
AMMO_DATA = {**B, **E, **BE, **W, **V, **ND, **TST, **POL, **WOOD, **SEC, **MAG, **MEL, **EXT_AMMO}