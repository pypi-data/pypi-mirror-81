# coding: utf-8
"""
i want try to fragmentation log information, you may see:
user-A: "hello, my name is user-a, i'm 24"
user-B: "hello, my name is user-b, i'm 24 too"
...

so, you have to use it by print("user-A: 'hello, my name is user-a', i'm 24"),
or logger.info("user-A: 'hello, my name is user-a', i'm 24 too")
there are so much irrelevant information or fields in msg, if don't think so, let's see like this:
withFields({
    "name": "user-A",
    "Age": 24,
}).info("hello")
"""

import sys
import threading
import multiprocessing

from logor.hooks import register_hook
from logor.core import log_serve
from logor.core.entry import *
from logor.core.socket_manager import SocketManager


def withFields(fields: dict) -> Entry:
    entry = EntryMap.get()
    entry.setFields(fields)
    return entry


def getLogger(module) -> Entry:
    return EntryMap().get(module)


def setLevel(level: int):
    assert level in level_map, "please ensure your level valid"
    GlobalAttr.level = level


def setFormat(format: str = FORMAT.TEXT):
    assert format in ("text", "json"), "format should be text/json"
    GlobalAttr.stdMode = format


class Logor:

    def add_hooks(self, level: int, hooks: list):
        for hook in hooks:
            register_hook(level, hook)

    def __init__(self, thread: bool = True, process: bool = False,
                 level: int = INFO, format: str = FORMAT.TEXT, **kwargs):
        setLevel(level)
        setFormat(format)
        self.start_thread = thread
        self.start_process = process
        self.add_hooks(0, kwargs.get("basic_hooks", ["logor.hooks.console.StdoutHook"]))
        self.add_hooks(DEBUG, kwargs.get("debug_hooks", []))
        self.add_hooks(INFO, kwargs.get("info_hooks", []))
        self.add_hooks(WARNING, kwargs.get("warning_hooks", []))
        self.add_hooks(ERROR, kwargs.get("error_hooks", []))

    def __enter__(self):
        server = SocketManager.get_server()
        if self.start_process:
            p = multiprocessing.Process(target=log_serve, args=(server,), daemon=False)
            p.start()
            thread_or_process.append(p)
        elif self.start_thread:
            t = threading.Thread(target=log_serve, args=(server,), daemon=True)
            t.start()
            thread_or_process.append(t)
        else:
            raise Exception("not point log start mode")

    def __exit__(self, exc_type, exc_val, exc_tb):
        client = SocketManager.get_client()
        for top in thread_or_process:
            if hasattr(top, "terminate"):
                client.send(STOP)


def execute(argv: str = None):
    argv = argv or f"{sys.argv[1:]}"
    with Logor():
        withFields({
            "Module": "Logor",
        }).info(argv)
        withFields({
            "Module": "Console.Argv",
        }).info(argv)
