# coding: utf-8
import json
import socket
import datetime

from logor.utils import *
from logor.core.socket_manager import SocketManager


def check_log_level(level: int = None):
    def wrapper(*args, **kwargs):
        def _wrapper(entry, msg: str):
            if level < GlobalAttr.level:  # check log level
                return
            entry.send_msg(msg, level)

        return _wrapper

    return wrapper


class GlobalAttr:
    level = INFO
    stdMode = "text"  # text/json


class Entry:

    def __init__(self, module: str = None, sock: socket.socket = None):
        self.module = module
        self.fields = dict()
        self.text_fields = ""
        self.sock = sock or SocketManager.get_client()

    def setFields(self, fields: dict):
        self.fields = fields
        text_fields = ""
        for key, value in self.fields.items():
            text_fields += f"{key}={value} "
        self.text_fields = text_fields
        return self

    def withFields(self, fields: dict):
        self.fields.update(fields)
        text_fields = ""
        for key, value in self.fields.items():
            text_fields += f"{key}={value} "
        self.text_fields = text_fields
        return self

    def send(self, msg: str, level: int) -> None:
        self.sock.send(encode_msg(msg, level))

    def json_msg(self, msg: str, level: int) -> None:
        json_msg = {
            "time": f"{datetime.datetime.now()}",
            "level": level_map.get(level, "unknown"),
            "msg": msg,
        }
        json_msg.update(self.fields)
        self.send(json.dumps(json_msg, ensure_ascii=False), level)

    def text_msg(self, msg: str, level: int) -> None:
        text_msg = f'time="{datetime.datetime.now()}" level={level_map.get(level, "unknown")} msg="{msg}" {self.text_fields}'
        self.send(text_msg, level)

    def send_msg(self, msg: str, level: int) -> None:
        if GlobalAttr.stdMode == FORMAT.TEXT:
            self.text_msg(msg, level)
        else:
            self.json_msg(msg, level)

    @check_log_level(level=DEBUG)
    def debug(self, msg: str):
        raise NotImplementedError

    @check_log_level(level=INFO)
    def info(self, msg: str):
        raise NotImplementedError

    @check_log_level(level=WARNING)
    def warning(self, msg: str):
        raise NotImplementedError

    @check_log_level(level=ERROR)
    def error(self, msg: str):
        raise NotImplementedError


class EntryMap:
    entryMap = dict()

    @classmethod
    def get(cls, module: str = None) -> Entry:
        if module is None:
            return Entry(None)
        if module not in cls.entryMap:
            SocketManager.init_socketpair()
            cls.entryMap[module] = Entry(module)
        return cls.entryMap[module]
