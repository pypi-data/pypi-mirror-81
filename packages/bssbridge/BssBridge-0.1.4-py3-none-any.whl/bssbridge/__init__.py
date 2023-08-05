# -*- coding: utf-8 -*-

__version__ = '0.1.4'

from importlib import reload
import sys
import codecs
from typing import Any, Optional, Callable

import orjson
from clikit.api.io import flags as LogLevel

__all__ = ["LogLevel"]

from pydantic import BaseModel


def json_dumps(obj: Any, *, default: Optional[Callable[[Any], Any]] = None, option: Optional[int] = None, ) -> str:
  return orjson.dumps(
    obj, default=default,
    option=option or 0 | orjson.OPT_INDENT_2 | orjson.OPT_OMIT_MICROSECONDS | orjson.OPT_STRICT_INTEGER
  ).decode(encoding='utf-8')


BaseModel.Config.json_dumps = json_dumps
BaseModel.Config.json_loads = orjson.loads


def setup_console(sys_enc="utf-8"):
  reload(sys)
  try:
    # для win32 вызываем системную библиотечную функцию
    if sys.platform.startswith("win"):
      import ctypes
      enc = "cp%d" % ctypes.windll.kernel32.GetOEMCP()  # TODO: проверить на win64/python64
    else:
      # для Linux всё, кажется, есть и так
      enc = (sys.stdout.encoding if sys.stdout.isatty() else
             sys.stderr.encoding if sys.stderr.isatty() else
             sys.getfilesystemencoding() or sys_enc)

    # кодировка для sys
    #sys.setdefaultencoding(sys_enc)

    # переопределяем стандартные потоки вывода, если они не перенаправлены
    if sys.stdout.isatty() and sys.stdout.encoding != enc:
      sys.stdout = codecs.getwriter(enc)(sys.stdout, 'replace')

    if sys.stderr.isatty() and sys.stderr.encoding != enc:
      sys.stderr = codecs.getwriter(enc)(sys.stderr, 'replace')

  except BaseException as exc:
    pass  # Ошибка? Всё равно какая - работаем по-старому...


def main() -> None:
  import tracemalloc
  import warnings

  tracemalloc.start()
  setup_console()
  warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

  from cleo import Application
  from bssbridge.commands.dbf import ftp2odata as dbf_ftp2odata
  Application(name="bb", version=__version__, complete=True).add(command=dbf_ftp2odata()).run()
