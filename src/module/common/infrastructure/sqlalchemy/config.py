from typing import Self

from pydantic import BaseModel, ConfigDict


class DatabaseConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)

    url: str
    pool_size: int = 5
    enable_echo: bool = False
