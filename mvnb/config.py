from importlib.metadata import version
from pathlib import Path
from shlex import split
from sys import executable

from mvnb import _bootstrap, _preprocessor
from mvnb.data import Data
from mvnb.option import Parser, option


class Config(Data):
    def __init__(self, args):
        super().__init__(**_parser.parse(args))

    @option(help="show help", action="help")
    def help(self, _):
        pass  # pragma: no cover

    @option(help="show version", action="version")
    def version(self, _):
        return version(_package)

    @option(help="notebook path", metavar="<path>")
    def path(self, raw):
        return Path(raw) if raw else None

    @option(help="server address", metavar="<addr>")
    def addr(self, raw):
        return raw or "0.0.0.0"

    @option(help="server port", metavar="<port>")
    def port(self, raw):
        return int(raw or 8000)

    @option(help="repl command", metavar="<cmd>")
    def repl_command(self, raw):
        return raw or executable

    @option(help="repl arguments", metavar="<args>")
    def repl_arguments(self, raw):
        return split(raw) if raw else ["-i", _bootstrap.__file__]

    @option(help="preprocessor command", metavar="<cmd>")
    def preproc(self, raw):
        return split(raw) if raw else [executable, _preprocessor.__file__]

    @option(help="before-run code", metavar="<code>")
    def before_run(self, raw):
        return self._text_or_file(raw)

    @option(help="after-run code", metavar="<code>")
    def after_run(self, raw):
        return self._text_or_file(raw)

    @option(help="fork code", metavar="<code>")
    def fork(self, raw):
        default = f"__mvnb_fork('{self.fork_addr}')"
        return self._text_or_file(raw) or default

    @option(help="fork address placeholder", metavar="<text>")
    def fork_addr(self, raw):
        return raw or "__address__"

    @option(help="sidechannel code", metavar="<code>")
    def sidechannel(self, raw):
        url, id = self.sidechannel_url, self.sidechannel_cell_id
        default = f"__sidechannel = __mvnb_sidechannel('{url}', '{id}')"
        return self._text_or_file(raw) or default

    @option(help="sidechannel url placeholder", metavar="<text>")
    def sidechannel_url(self, raw):
        return raw or "__url__"

    @option(help="sidechannel cell id placeholder", metavar="<text>")
    def sidechannel_cell_id(self, raw):
        return raw or "__id__"

    @option(help="callback code", metavar="<code>")
    def callback(self, raw):
        default = f"__mvnb_callback('{self.callback_url}', '{self.callback_payload}')"
        return self._text_or_file(raw) or default

    @option(help="callback url placeholder", metavar="<text>")
    def callback_url(self, raw):
        return raw or "__url__"

    @option(help="callback payload placeholder", metavar="<text>")
    def callback_payload(self, raw):
        return raw or "__payload__"

    @option(help="fromfile prefix", metavar="<text>")
    def fromfile_prefix(self, raw):
        return raw or "@"

    def _text_or_file(self, raw):
        if raw is None:
            return None
        if raw.startswith(self.fromfile_prefix):
            path = raw[len(self.fromfile_prefix) :]
            return Path(path).read_text()
        return raw


_package = __package__.split(".")[0]

_parser = Parser(_package, Config)
