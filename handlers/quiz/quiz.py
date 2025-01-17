from question import QUESTIONS

class Form(StatesGroup):
    waiting_for_response = State()
    asking_questions = State()

@dataclass
class Answer:
    """
    Represents an answer to a question.
    """
    text: str
    """The answer text"""
    sensomotorika: int = 0
    defectolog: int = 0
    """Indicates if the answer is correct"""

@dataclass
class Question:
    text: str
    """The question text"""
    answers: list[Answer]
    """List of answers"""
    answer: str = field(init=False)
    sensomotorika: int = 0
    defectolog: int = 0

    def __post_init__(self):
        self.answer = next(answer.text for answer in self.answers if answer.sensomotorika>=0)

quiz_router = Router()

class DiagnoseScene(Scene, state="asking_questions"):
    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> Any:
        if not step:
            await message.answer("Welcome to the quiz!")

        try:
            quiz = QUESTIONS[step]
        except IndexError:
            return await self.wizard.exit()

        markup = ReplyKeyboardBuilder()
        markup.add(*[KeyboardButton(text=answer.text) for answer in quiz.answers])


        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS[step].text,
            reply_markup=markup.adjust(2).as_markup(resize_keyboard=True),
        )

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        answers = data.get("answers", {})

        sensomotorika = 0
        defectolog = 0
        user_answers = []
        for step, quiz in enumerate(QUESTIONS):
            answer = answers.get(step)
            s, d = [(i.sensomotorika, i.defectolog) for i in quiz.answers if i.text==answer][0]
            print(d)
            if s == 1:
                sensomotorika += s
                icon = ""
            else:
                defectolog += d
                icon = ""
            if answer is None:
                answer = "no answer"
            user_answers.append(f"{quiz.text} ({icon} {html.quote(answer)})")

        content = as_list(
            as_section(
                Bold("Your answers:"),
                as_numbered_list(*user_answers),
            ),
            "",
            as_section(
                Bold("Summary:"),
                as_list(
                    as_key_value("sensomotorika", sensomotorika),
                    as_key_value("defectolog", defectolog),
                ),
            ),
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Проанализируй ответы человека и дай первоначальный диагноз для специалиста на РАС."},
                {"role": "user", "content": "".join(user_answers)}
            ]
        )

        # Получаем ответ от ChatGPT
        bot_reply = completion.choices[0].message.content
        await message.answer(bot_reply)

        await message.answer(**content.as_kwargs(), reply_markup=ReplyKeyboardRemove())
        await state.set_data({})

    

    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        """
        Method triggered when the user selects an answer.

        It stores the answer and proceeds to the next question.

        :param message:
        :param state:
        :return:
        """
        data = await state.get_data()
        step = data["step"]
        answers = data.get("answers", {})
        answers[step] = message.text
        await state.update_data(answers=answers)

        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self, message: Message) -> None:
        """
        Method triggered when the user sends a message that is not a command or an answer.

        It asks the user to select an answer.

        :param message: The message received from the user.
        :return: None
        """
        await message.answer("Please select an answer.")

