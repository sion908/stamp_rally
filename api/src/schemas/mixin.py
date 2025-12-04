from pydantic import Field


class ForOrm():

    class Config:
        """
        Pydantic's orm_mode will tell the Pydantic model to read the data
        even if it is not a dict,
        but an ORM model (or any other arbitrary object with attributes).
        dbからのデータ流入がやりやすくなるパラメータ
        """
        orm_mode = True


class FromLiff():

    lineToken: str = Field(..., description="liff用のToken")
