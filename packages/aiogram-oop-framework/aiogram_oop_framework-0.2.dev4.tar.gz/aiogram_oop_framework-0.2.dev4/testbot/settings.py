from pathlib import Path
import typing
import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram_oop_framework.core.project import Project, ProjectStructure
from aiogram.contrib.fsm_storage.memory import MemoryStorage

PATH = Path("C:/Users/admin/Desktop/projects/aiogram_oop_extender")
PROJECT_NAME = "testbot"
pr: Project = Project(PROJECT_NAME, PATH)
struc: ProjectStructure = ProjectStructure(pr)
struc.include('views')
pr.structure = struc

PROJECT: Project = pr

AUTO_REGISTER_VIEWS = True


TELEGRAM_BOT_TOKEN: str = "923071573:AAF8TU3QubN9QsXh2bXk6HUWQLjb1j5OJtg"

MIDDLEWARES: typing.List[BaseMiddleware.__class__] = []

BOT_STORAGE = MemoryStorage()
MEMORY_STORAGE = BOT_STORAGE  # needed for backward compatibility, will be removed

PARSE_MODE = types.ParseMode.HTML
