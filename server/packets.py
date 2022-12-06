
from enum import IntEnum, auto
from json import load as json_load
from pydantic import BaseModel, Field
from vec import Vector2
from typing import Literal, Union

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
    

class MsgPlayerEnter(BaseModel):
    type: Literal[MsgType.PlayerEnter] = MsgType.PlayerEnter
    id: int
    x: float
    y: float
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



class Msg(BaseModel):
    __root__: Union[MsgError, MsgPlayerInfo, MsgPlayerStats, MsgAttack, MsgShoot] = Field(..., discriminator="type")
