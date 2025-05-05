from typing import Annotated
from fastapi import Depends

from ..config import Settings, get_settings

SettingDep = Annotated[Settings, Depends(get_settings)]
