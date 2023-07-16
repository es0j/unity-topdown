
from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field,RootModel
from typing import Literal, Union
from .libmath import Vector2

class MsgType(IntEnum):
    Error = 0
    ClientHello = auto()
    ServerHello = auto()
    PlayerInfo = auto()
    PlayerEnter = auto()
    PlayerLeave = auto()
    PlayerStats = auto()
    Attack = auto()
    Shoot = auto()
    PlayerWeapon = auto()


class MsgError(BaseModel):
    type: Literal[MsgType.Error] = MsgType.Error
    msg: str


class MsgClientHello(BaseModel):
    type: Literal[MsgType.ClientHello] = MsgType.ClientHello
    


class MsgServerHello(BaseModel):
    type: Literal[MsgType.ServerHello] = MsgType.ServerHello
    name: str
    id: int


class MsgPlayerInfo(BaseModel):
    type: Literal[MsgType.PlayerInfo] = MsgType.PlayerInfo
    id: int
    x: float
    y: float
    rotation: float

class MsgPlayerEnter(BaseModel):
    type: Literal[MsgType.PlayerEnter] = MsgType.PlayerEnter
    id: int
    gid: int

class MsgPlayerLeave(BaseModel):
    type: Literal[MsgType.PlayerLeave] = MsgType.PlayerLeave
    id: int

class MsgPlayerStats(BaseModel):
    type: Literal[MsgType.PlayerStats] = MsgType.PlayerStats
    id: int
    health: float


class MsgAttack(BaseModel):
    type: Literal[MsgType.Attack] = MsgType.Attack
    id: int
    target: int

class MsgShoot(BaseModel):
    type: Literal[MsgType.Shoot] = MsgType.Shoot
    id: int
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    
class MsgPlayerWeapon(BaseModel):
    type: Literal[MsgType.PlayerWeapon] = MsgType.PlayerWeapon
    id: int
    weapon_id: int
    

class Msg(RootModel):
    root: Union[MsgError, MsgPlayerInfo, MsgPlayerStats, MsgAttack, MsgShoot, MsgPlayerWeapon] = Field(..., discriminator="type")
