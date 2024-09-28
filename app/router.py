from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.payments import get_quick_pay, check_quick_pay

router = Router()


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Подписка ⭐️")]],
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    await message.answer("Добро пожаловать!", reply_markup=markup)


@router.message(F.text == "Подписка ⭐️")
async def subscribe_request(message: types.Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    if user_data.get("is_subscribed"):
        await message.answer("У вас уже оформлена подписка. Приятного пользования :)")
        return

    pay = get_quick_pay()
    await state.update_data(pay_state=pay.label)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти к оплате", url=pay.redirected_url)],
            [InlineKeyboardButton(text="Проверить платеж", callback_data="btn:claim")],
        ]
    )

    await message.answer(
        '<b>Оформление подписки</b>\n\nСтоимость подписки: 100 руб.\nНажмите на кнопку "Перейти к '
        'оплате", после успешной оплаты нажмите "Проверить платеж" 🤑',
        reply_markup=markup,
    )


@router.callback_query(F.data == "btn:claim")
async def check_payment(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    if user_data.get("is_subscribed"):
        await callback.answer(
            "У вас уже оформлена подписка. Приятного пользования :)"
        )
        return
    pay_state = user_data.get("pay_state")
    if not pay_state:
        await callback.answer("Ошибка, попробуйте ещё раз")
        return
    if check_quick_pay(pay_state):
        await state.update_data(is_subscribed=True)
        await callback.message.answer("Подписка успешно оформлена!")
    else:
        await callback.message.answer(
            "Оплата не удалась. Попробуйте проверить позже или повторите попытку."
        )
    await callback.answer()
