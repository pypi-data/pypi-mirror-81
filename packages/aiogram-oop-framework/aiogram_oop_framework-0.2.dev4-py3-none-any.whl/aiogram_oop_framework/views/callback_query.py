import logging

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext, Dispatcher

from .base import BaseView


class CallbackQueryView(BaseView):
    @classmethod
    async def execute(cls, q: CallbackQuery, state: FSMContext = None, **kwargs):
        raise NotImplementedError

    @classmethod
    async def _execute(cls, q: CallbackQuery, state: FSMContext = None, **kwargs):

        # remove with execute_in_<chat_type> removing
        chat_type = q.message.chat.type
        if hasattr(cls, f'execute_in_{chat_type}'):
            logging.warning("execute_in_<chat_type> is deprecated in version 0.2.dev0, "
                            "use decorator filters.filter_execute() instead: "
                            "`filters.filter_execute(chat_type=<chat_type>)`")
            in_chat_method = cls.__dict__[f'execute_in_{chat_type}']
            func = in_chat_method.__func__
            if hasattr(func, "__execute_filters__"):
                fltrs = func.__execute_filters__
            else:
                fltrs = []
            if fltrs.chat_type is None:
                fltrs.chat_type = chat_type
                func.__execute_filters__ = fltrs
        # remove with execute_in_<chat_type> removing

        await super()._execute(q, state, **kwargs)

    @classmethod
    def register(cls, dp: Dispatcher):
        callback = cls._execute
        kwargs = cls.register_kwargs if cls.register_kwargs else {}
        custom_filters = cls.custom_filters if cls.custom_filters else []
        dp.register_callback_query_handler(callback, *custom_filters, state=cls.state(),
                                           run_task=cls.run_task, **kwargs)
