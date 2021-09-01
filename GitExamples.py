
"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://git.io/JOmFw.
"""
import Constants as Token
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler

# def start(update: Update, context: CallbackContext) -> None:
#     """Sends a message with three inline buttons attached."""
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data='1'),
#             InlineKeyboardButton("Option 2", callback_data='2'),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data='3')],
#     ]
#
#     reply_markup = InlineKeyboardMarkup(keyboard)
#
#     update.message.reply_text('Please choose:', reply_markup=reply_markup)
#
#
# def button(update: Update, context: CallbackContext) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query
#
#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()
#
#     query.edit_message_text(text=f"Selected option: {query.data}")
#
#
# def help_command(update: Update, context: CallbackContext) -> None:
#     """Displays info on how to use the bot."""
#     update.message.reply_text("Use /start to test this bot.")
#
#
# def main() -> None:
#     """Run the bot."""
#     # Create the Updater and pass it your bot's token.
#     updater = Updater(Token.API_KEY)
#
#     updater.dispatcher.add_handler(CommandHandler('start', start))
#     updater.dispatcher.add_handler(CallbackQueryHandler(button))
#     updater.dispatcher.add_handler(CommandHandler('help', help_command))
#
#     # Start the Bot
#     updater.start_polling()
#
#     # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT
#     updater.idle()

''' second example inline keyboard 2 '''

# # Stages
# FIRST, SECOND = range(2)
# # Callback data
# ONE, TWO, THREE, FOUR = range(4)
#
#
# def start(update: Update, context: CallbackContext) -> int:
#     """Send message on `/start`."""
#     # Get user that sent /start and log his name
#
#     # Build InlineKeyboard where each button has a displayed text
#     # and a string as callback_data
#     # The keyboard is a list of button rows, where each row is in turn
#     # a list (hence `[[...]]`).
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     # Send message with text and appended InlineKeyboard
#     update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
#     # Tell ConversationHandler that we're in state `FIRST` now
#     return FIRST
#
#
# def start_over(update: Update, context: CallbackContext) -> int:
#     """Prompt same text & keyboard as `start` does but not as new message"""
#     # Get CallbackQuery from Update
#     query = update.callback_query
#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     # Instead of sending a new message, edit the message that
#     # originated the CallbackQuery. This gives the feeling of an
#     # interactive menu.
#     query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
#     return FIRST
#
#
# def one(update: Update, context: CallbackContext) -> int:
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("3", callback_data=str(THREE)),
#             InlineKeyboardButton("4", callback_data=str(FOUR)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
#     )
#     return FIRST
#
#
# def two(update: Update, context: CallbackContext) -> int:
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("1", callback_data=str(ONE)),
#             InlineKeyboardButton("3", callback_data=str(THREE)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
#     )
#     return FIRST
#
#
# def three(update: Update, context: CallbackContext) -> int:
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
#             InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
#     )
#     # Transfer to conversation state `SECOND`
#     return SECOND
#
#
# def four(update: Update, context: CallbackContext) -> int:
#     """Show new choice of buttons"""
#     query = update.callback_query
#     query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("2", callback_data=str(TWO)),
#             InlineKeyboardButton("3", callback_data=str(THREE)),
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.edit_message_text(
#         text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
#     )
#     return FIRST
#
#
# def end(update: Update, context: CallbackContext) -> int:
#     """Returns `ConversationHandler.END`, which tells the
#     ConversationHandler that the conversation is over.
#     """
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(text="See you next time!")
#     return ConversationHandler.END
#
#
# def main() -> None:
#     """Run the bot."""
#     # Create the Updater and pass it your bot's token.
#     updater = Updater(Token.API_KEY)
#
#     # Get the dispatcher to register handlers
#     dispatcher = updater.dispatcher
#
#     # Setup conversation handler with the states FIRST and SECOND
#     # Use the pattern parameter to pass CallbackQueries with specific
#     # data pattern to the corresponding handlers.
#     # ^ means "start of line/string"
#     # $ means "end of line/string"
#     # So ^ABC$ will only allow 'ABC'
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#         states={
#             FIRST: [
#                 CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
#                 CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
#                 CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
#                 CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
#             ],
#             SECOND: [
#                 CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
#                 CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
#             ],
#         },
#         fallbacks=[CommandHandler('start', start)],
#     )
#
#     # Add ConversationHandler to dispatcher that will be used for handling updates
#     dispatcher.add_handler(conv_handler)
#
#     # Start the Bot
#     updater.start_polling()
#
#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()

''' third example poll and quies bot'''
# from telegram import (
#     Poll,
#     ParseMode,
#     KeyboardButton,
#     KeyboardButtonPollType,
#     ReplyKeyboardMarkup,
#     ReplyKeyboardRemove,
#     Update,
# )
# from telegram.ext import (
#     Updater,
#     CommandHandler,
#     PollAnswerHandler,
#     PollHandler,
#     MessageHandler,
#     Filters,
#     CallbackContext,
# )
#
#
# def start(update: Update, context: CallbackContext) -> None:
#     """Inform user about what this bot can do"""
#     update.message.reply_text(
#         'Please select /poll to get a Poll, /quiz to get a Quiz or /preview'
#         ' to generate a preview for your poll'
#     )
#
#
# def poll(update: Update, context: CallbackContext) -> None:
#     """Sends a predefined poll"""
#     questions = ["Good", "Really good", "Fantastic", "Great"]
#     message = context.bot.send_poll(
#         update.effective_chat.id,
#         "How are you?",
#         questions,
#         is_anonymous=False,
#         allows_multiple_answers=True,
#     )
#     # Save some info about the poll the bot_data for later use in receive_poll_answer
#     payload = {
#         message.poll.id: {
#             "questions": questions,
#             "message_id": message.message_id,
#             "chat_id": update.effective_chat.id,
#             "answers": 0,
#         }
#     }
#     context.bot_data.update(payload)
#
#
# def receive_poll_answer(update: Update, context: CallbackContext) -> None:
#     """Summarize a users poll vote"""
#     answer = update.poll_answer
#     poll_id = answer.poll_id
#     try:
#         questions = context.bot_data[poll_id]["questions"]
#     # this means this poll answer update is from an old poll, we can't do our answering then
#     except KeyError:
#         return
#     selected_options = answer.option_ids
#     answer_string = ""
#     for question_id in selected_options:
#         if question_id != selected_options[-1]:
#             answer_string += questions[question_id] + " and "
#         else:
#             answer_string += questions[question_id]
#     context.bot.send_message(
#         context.bot_data[poll_id]["chat_id"],
#         f"{update.effective_user.mention_html()} feels {answer_string}!",
#         parse_mode=ParseMode.HTML,
#     )
#     context.bot_data[poll_id]["answers"] += 1
#     # Close poll after three participants voted
#     if context.bot_data[poll_id]["answers"] == 3:
#         context.bot.stop_poll(
#             context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
#         )
#
#
# def quiz(update: Update, context: CallbackContext) -> None:
#     """Send a predefined poll"""
#     questions = ["1", "2", "4", "20"]
#     message = update.effective_message.reply_poll(
#         "How many eggs do you need for a cake?", questions, type=Poll.QUIZ, correct_option_id=2
#     )
#     # Save some info about the poll the bot_data for later use in receive_quiz_answer
#     payload = {
#         message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
#     }
#     context.bot_data.update(payload)
#
#
# def receive_quiz_answer(update: Update, context: CallbackContext) -> None:
#     """Close quiz after three participants took it"""
#     # the bot can receive closed poll updates we don't care about
#     if update.poll.is_closed:
#         return
#     if update.poll.total_voter_count == 3:
#         try:
#             quiz_data = context.bot_data[update.poll.id]
#         # this means this poll answer update is from an old poll, we can't stop it then
#         except KeyError:
#             return
#         context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])
#
#
# def preview(update: Update, context: CallbackContext) -> None:
#     """Ask user to create a poll and display a preview of it"""
#     # using this without a type lets the user chooses what he wants (quiz or poll)
#     button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
#     message = "Press the button to let the bot generate a preview for your poll"
#     # using one_time_keyboard to hide the keyboard
#     update.effective_message.reply_text(
#         message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
#     )
#
#
# def receive_poll(update: Update, context: CallbackContext) -> None:
#     """On receiving polls, reply to it by a closed poll copying the received poll"""
#     actual_poll = update.effective_message.poll
#     # Only need to set the question and options, since all other parameters don't matter for
#     # a closed poll
#     update.effective_message.reply_poll(
#         question=actual_poll.question,
#         options=[o.text for o in actual_poll.options],
#         # with is_closed true, the poll/quiz is immediately closed
#         is_closed=True,
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#
# def help_handler(update: Update, context: CallbackContext) -> None:
#     """Display a help message"""
#     update.message.reply_text("Use /quiz, /poll or /preview to test this bot.")
#
#
# def main() -> None:
#     """Run bot."""
#     # Create the Updater and pass it your bot's token.
#     updater = Updater(Token.API_KEY)
#     dispatcher = updater.dispatcher
#     dispatcher.add_handler(CommandHandler('start', start))
#     dispatcher.add_handler(CommandHandler('poll', poll))
#     dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))
#     dispatcher.add_handler(CommandHandler('quiz', quiz))
#     dispatcher.add_handler(PollHandler(receive_quiz_answer))
#     dispatcher.add_handler(CommandHandler('preview', preview))
#     dispatcher.add_handler(MessageHandler(Filters.poll, receive_poll))
#     dispatcher.add_handler(CommandHandler('help', help_handler))
#
#     # Start the Bot
#     updater.start_polling()
#
#     # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT
#     updater.idle()

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using nested ConversationHandlers.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


from typing import Tuple, Dict, Any

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)


# State definitions for top level conversation
SELECTING_ACTION, ADDING_MEMBER, ADDING_SELF, DESCRIBING_SELF = map(chr, range(4))
# State definitions for second level conversation
SELECTING_LEVEL, SELECTING_GENDER = map(chr, range(4, 6))
# State definitions for descriptions conversation
SELECTING_FEATURE, TYPING = map(chr, range(6, 8))
# Meta states
STOPPING, SHOWING = map(chr, range(8, 10))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(
    PARENTS,
    CHILDREN,
    SELF,
    GENDER,
    MALE,
    FEMALE,
    AGE,
    NAME,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
) = map(chr, range(10, 22))


# Helper
def _name_switcher(level: str) -> Tuple[str, str]:
    if level == PARENTS:
        return 'Father', 'Mother'
    return 'Brother', 'Sister'


# Top level conversation callbacks
def start(update: Update, context: CallbackContext) -> str:
    """Select an action: Adding parent/child or show data."""
    text = (
        "You may choose to add a family member, yourself, show the gathered data, or end the "
        "conversation. To abort, simply type /stop."
    )

    buttons = [
        [
            InlineKeyboardButton(text='Add family member', callback_data=str(ADDING_MEMBER)),
            InlineKeyboardButton(text='Add yourself', callback_data=str(ADDING_SELF)),
        ],
        [
            InlineKeyboardButton(text='Show data', callback_data=str(SHOWING)),
            InlineKeyboardButton(text='Done', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(
            "Hi, I'm Family Bot and I'm here to help you gather information about your family."
        )
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION


def adding_self(update: Update, context: CallbackContext) -> str:
    """Add information about yourself."""
    context.user_data[CURRENT_LEVEL] = SELF
    text = 'Okay, please tell me about yourself.'
    button = InlineKeyboardButton(text='Add info', callback_data=str(MALE))
    keyboard = InlineKeyboardMarkup.from_button(button)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return DESCRIBING_SELF


def show_data(update: Update, context: CallbackContext) -> str:
    """Pretty print gathered data."""

    def prettyprint(user_data: Dict[str, Any], level: str) -> str:
        people = user_data.get(level)
        if not people:
            return '\nNo information yet.'

        text = ''
        if level == SELF:
            for person in user_data[level]:
                text += f"\nName: {person.get(NAME, '-')}, Age: {person.get(AGE, '-')}"
        else:
            male, female = _name_switcher(level)

            for person in user_data[level]:
                gender = female if person[GENDER] == FEMALE else male
                text += f"\n{gender}: Name: {person.get(NAME, '-')}, Age: {person.get(AGE, '-')}"
        return text

    user_data = context.user_data
    text = f"Yourself:{prettyprint(user_data, SELF)}"
    text += f"\n\nParents:{prettyprint(user_data, PARENTS)}"
    text += f"\n\nChildren:{prettyprint(user_data, CHILDREN)}"

    buttons = [[InlineKeyboardButton(text='Back', callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    user_data[START_OVER] = True

    return SHOWING


def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')

    return END


def end(update: Update, context: CallbackContext) -> int:
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)

    return END


# Second level conversation callbacks
def select_level(update: Update, context: CallbackContext) -> str:
    """Choose to add a parent or a child."""
    text = 'You may add a parent or a child. Also you can show the gathered data or go back.'
    buttons = [
        [
            InlineKeyboardButton(text='Add parent', callback_data=str(PARENTS)),
            InlineKeyboardButton(text='Add child', callback_data=str(CHILDREN)),
        ],
        [
            InlineKeyboardButton(text='Show data', callback_data=str(SHOWING)),
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_LEVEL


def select_gender(update: Update, context: CallbackContext) -> str:
    """Choose to add mother or father."""
    level = update.callback_query.data
    context.user_data[CURRENT_LEVEL] = level

    text = 'Please choose, whom to add.'

    male, female = _name_switcher(level)

    buttons = [
        [
            InlineKeyboardButton(text=f'Add {male}', callback_data=str(MALE)),
            InlineKeyboardButton(text=f'Add {female}', callback_data=str(FEMALE)),
        ],
        [
            InlineKeyboardButton(text='Show data', callback_data=str(SHOWING)),
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_GENDER


def end_second_level(update: Update, context: CallbackContext) -> int:
    """Return to top level conversation."""
    context.user_data[START_OVER] = True
    start(update, context)

    return END


# Third level callbacks
def select_feature(update: Update, context: CallbackContext) -> str:
    """Select a feature to update for the person."""
    buttons = [
        [
            InlineKeyboardButton(text='Name', callback_data=str(NAME)),
            InlineKeyboardButton(text='Age', callback_data=str(AGE)),
            InlineKeyboardButton(text='Done', callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we collect features for a new person, clear the cache and save the gender
    if not context.user_data.get(START_OVER):
        context.user_data[FEATURES] = {GENDER: update.callback_query.data}
        text = 'Please select a feature to update.'

        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # But after we do that, we need to send a new message
    else:
        text = 'Got it! Please select a feature to update.'
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_FEATURE


def ask_for_input(update: Update, context: CallbackContext) -> str:
    """Prompt user to input data for selected feature."""
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    text = 'Okay, tell me.'

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return TYPING


def save_input(update: Update, context: CallbackContext) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data[FEATURES][user_data[CURRENT_FEATURE]] = update.message.text

    user_data[START_OVER] = True

    return select_feature(update, context)


def end_describing(update: Update, context: CallbackContext) -> int:
    """End gathering of features and return to parent conversation."""
    user_data = context.user_data
    level = user_data[CURRENT_LEVEL]
    if not user_data.get(level):
        user_data[level] = []
    user_data[level].append(user_data[FEATURES])

    # Print upper level menu
    if level == SELF:
        user_data[START_OVER] = True
        start(update, context)
    else:
        select_level(update, context)

    return END


def stop_nested(update: Update, context: CallbackContext) -> str:
    """Completely end conversation from within nested conversation."""
    update.message.reply_text('Okay, bye.')

    return STOPPING


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(Token.API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Set up third level ConversationHandler (collecting features)
    description_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                select_feature, pattern='^' + str(MALE) + '$|^' + str(FEMALE) + '$'
            )
        ],
        states={
            SELECTING_FEATURE: [
                CallbackQueryHandler(ask_for_input, pattern='^(?!' + str(END) + ').*$')
            ],
            TYPING: [MessageHandler(Filters.text & ~Filters.command, save_input)],
        },
        fallbacks=[
            CallbackQueryHandler(end_describing, pattern='^' + str(END) + '$'),
            CommandHandler('stop', stop_nested),
        ],
        map_to_parent={
            # Return to second level menu
            END: SELECTING_LEVEL,
            # End conversation altogether
            STOPPING: STOPPING,
        },
    )

    # Set up second level ConversationHandler (adding a person)
    add_member_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_level, pattern='^' + str(ADDING_MEMBER) + '$')],
        states={
            SELECTING_LEVEL: [
                CallbackQueryHandler(select_gender, pattern=f'^{PARENTS}$|^{CHILDREN}$')
            ],
            SELECTING_GENDER: [description_conv],
        },
        fallbacks=[
            CallbackQueryHandler(show_data, pattern='^' + str(SHOWING) + '$'),
            CallbackQueryHandler(end_second_level, pattern='^' + str(END) + '$'),
            CommandHandler('stop', stop_nested),
        ],
        map_to_parent={
            # After showing data return to top level menu
            SHOWING: SHOWING,
            # Return to top level menu
            END: SELECTING_ACTION,
            # End conversation altogether
            STOPPING: END,
        },
    )

    # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the second level
    # conversation, we need to make sure the top level conversation can also handle them
    selection_handlers = [
        add_member_conv,
        CallbackQueryHandler(show_data, pattern='^' + str(SHOWING) + '$'),
        CallbackQueryHandler(adding_self, pattern='^' + str(ADDING_SELF) + '$'),
        CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SHOWING: [CallbackQueryHandler(start, pattern='^' + str(END) + '$')],
            SELECTING_ACTION: selection_handlers,
            SELECTING_LEVEL: selection_handlers,
            DESCRIBING_SELF: [description_conv],
            STOPPING: [CommandHandler('start', start)],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
