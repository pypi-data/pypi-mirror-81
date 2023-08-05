from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.chat_member import ChatMemberStatus
from aiogram.dispatcher.filters.builtin import IsReplyFilter

from aiogram_oop_framework.views import MessageView, CallbackQueryView
from aiogram_oop_framework.filters.filters import filter_execute


class Example(MessageView):

    @staticmethod
    async def execute(m: types.Message, state: FSMContext = None, **kwargs):
        print(m)
        await m.answer('undef')

    @classmethod
    @filter_execute(IsReplyFilter(True), is_chat_admin=True, chat_type=['private', 'supergroup'])
    @filter_execute(IsReplyFilter(True), is_chat_admin=True, chat_type=['private', 'supergroup'])
    async def execute_for_reply(cls, m: types.Message, state: FSMContext = None, **kwargs):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('gg', callback_data='gg'))
        await m.answer('gg reply and admin brr', reply_markup=kb)

    @classmethod
    @filter_execute(entities='mention')
    async def execute_for_admin(cls, m: types.Message, state: FSMContext = None, **kwargs):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('gg', callback_data='gg'))
        await m.answer('gg admin brr', reply_markup=kb)

    @classmethod
    @filter_execute(chat_member_status=ChatMemberStatus.CREATOR)
    async def execute_for_creators(cls, m: types.Message, state: FSMContext = None, **kwargs):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('gg', callback_data='gg'))
        await m.answer('gg creator brr', reply_markup=kb)


class Example1(CallbackQueryView):

    @classmethod
    async def execute(cls, q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('undef')

    @classmethod
    @filter_execute(chat_member_status=ChatMemberStatus.ADMINISTRATOR)
    async def execute_for_admins(cls, q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('gg ADMIN brr')

    @classmethod
    @filter_execute(chat_member_status=ChatMemberStatus.CREATOR)
    async def execute_for_creators(cls, q: types.CallbackQuery, state: FSMContext = None, **kwargs):
        await q.answer('gg CREATOR brr')
