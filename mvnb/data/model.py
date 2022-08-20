from functools import singledispatchmethod

from mvnb.data import message
from mvnb.data.data import Data
from mvnb.util.record import field


class Model(Data):
    pass


class Notebook(Model):
    def __init__(self, **values):
        super().__init__(**values)
        self._index = {}

    @field
    def cells(self, raw):
        return raw or []

    def cell(self, name):
        return self._index.get(name)

    def name(self, worker):
        for c in self.cells:
            if c.worker is worker:
                return c.name

    @singledispatchmethod
    def update(self, _):
        pass

    @update.register(message.DidCreateCell)
    def _(self, msg):
        cell = Cell(name=msg.request.cell, parent=msg.request.parent)
        self.cells.append(cell)
        self._index[cell.name] = cell

    @update.register(message.DidUpdateCell)
    def _(self, msg):
        cell = self.cell(msg.request.cell)
        cell.code = msg.request.code

    @update.register(message.Stdout)
    def _(self, msg):
        cell = self.cell(msg.cell)
        result = Output(type="text", data=msg.text)
        cell.results.append(result)


class Cell(Model):
    def __init__(self, **values):
        super().__init__(**values)
        self.worker = None

    @field
    def name(self, raw):
        return raw

    @field
    def code(self, raw):
        return raw

    @field
    def parent(self, raw):
        return raw

    @field
    def results(self, raw):
        return raw or []


class Output(Model):
    @field
    def type(self, raw):
        return raw

    @field
    def data(self, raw):
        return raw