from uuid import uuid4

from mvnb.data.data import Data
from mvnb.util.record import field


class Message(Data):
    @field
    def id(self, raw):
        return raw or uuid4().hex


class Request(Message):
    @field
    def cell(self, raw):
        return raw


class CreateCell(Request):
    @field
    def parent(self, raw):
        return raw


class UpdateCell(Request):
    @field
    def code(self, raw):
        return raw


class RunCell(Request):
    pass


class Response(Message):
    @field
    def request(self, raw):
        return raw


class DidCreateCell(Response):
    pass


class DidUpdateCell(Response):
    pass


class DidRunCell(Response):
    pass


class Output(Message):
    @field
    def cell(self, raw):
        return raw


class Stdout(Output):
    @field
    def text(self, raw):
        return raw