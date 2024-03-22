import unittest
import requests
import xmltodict
from fastapi import FastAPI
from enum import auto, Enum
import logging
import uvicorn

import ssl
from typing import Union
from pydantic import BaseModel

# class RemoteUtils(object):
#     _ssl_context = ssl._create_unverified_context()
#
#     @classmethod
#     def download_to(cls, url, decode='utf-8', fnout=None):
#         with request.urlopen(url, context=cls._ssl_context) as response, open(fnout, 'w') as fout:
#             fout.write(response.read().decode(decode))
#
#     @classmethod
#     def read_from_url(cls, url, decode='utf-8'):
#         data = None
#         with request.urlopen(url, context=cls._ssl_context) as response:
#             data = response.read().decode(decode)
#         return data
#
#     @staticmethod
#     def is_url(url):
#       try:
#         result = urlparse(url)
#         return all([result.scheme, result.netloc])
#       except ValueError:
#         return False

class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    # pylint: disable=no-self-argument
    # The first argument to this function is documented to be the name of the
    # enum member, not `self`:
    # https://docs.python.org/3.6/library/enum.html#using-automatic-values
    def _generate_next_value_(name, *_):
        return name


class ServiceName(StrEnum):
    AstroSpace = auto()


SERVICE_KEYS = {
    ServiceName.AstroSpace: 'RLrJxlv43gHUxjUue9AI73BjrvCgyghV8BXfj/h78Yc9UcwolvBETVJlvNXAzWMhIon2KWTQo8C0fQRBlxWWuw=='
}

END_POINTS = {
    ServiceName.AstroSpace: 'http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService'
}

app = FastAPI()

###
# Logger
logging.config.fileConfig('../config/logging.conf')
logger = logging.getLogger('apibridge')

@app.get(f"/{ServiceName.AstroSpace}")
async def root_as():
    return f"Root of {ServiceName.AstroSpace}"


@app.get(f"/{ServiceName.AstroSpace}/getLunCalInfo")
async def getLunCalInfo(syear: str, smonth: str, sday: str):
    endpoint = END_POINTS[ServiceName.AstroSpace]
    service_key = SERVICE_KEYS[ServiceName.AstroSpace]
    url = (f"{endpoint}/getLunCalInfo?solYear={syear}&solMonth={smonth}&solDay={sday}&ServiceKey={service_key}")
    data = xmltodict.parse(requests.get(url).content)
    logger.debug(f"items: {data['response']['body']['items']['item']}")
    lyear = data['response']['body']['items']['item']['lunYear']
    lmonth = data['response']['body']['items']['item']['lunMonth']
    lday = data['response']['body']['items']['item']['lunDay']
    result = {"lunYear": lyear, "lunMonth": lmonth, "lunDay": lday}
    logger.debug(f"result: {result}")
    return {"lunYear": lyear, "lunMonth": lmonth, "lunDay": lday}

# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#
#
# @app.get("/")
# async def read_root():
#     return "This is root path from MyAPI"
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
#
#
# @app.post("/items/")
# async def create_item(item: Item):
#     return item
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     result = {"item_id": item_id, **item.dict()}
#
#
# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     return {"deleted": item_id}

# if __name__ == '__main__':
#     uvicorn.run(app,
#                 host='0.0.0.0',
#                 port=8000,
#                 ssl_keyfile='../config/ssl/private.key',
#                 ssl_certfile='../config/ssl/cert_with_chain.crt')