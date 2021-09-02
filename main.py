from datetime import datetime
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    Filters,
)

import tabulate
import sqlite3
import string
import random

# change this part to use this code in your bot
import Constants
seconder_token = Constants.API_KEY
admin_list = ['396700044']


def generate_random_password():
    # characters to generate password from
    characters = list(string.ascii_letters + string.digits)
    # length of password from the user
    length = 6
    # shuffling the characters
    random.shuffle(characters)
    # picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    # shuffling the resultant password
    random.shuffle(password)
    # converting the list to string
    # printing the list
    return "".join(password)


# Model data class Code
class CodeData:
    def __init__(self, data: str, username: str = 'None', active_mode: int = 1):
        self.data = data
        self.username = username
        self.active_mode = active_mode

    @staticmethod
    # turning a list of code data to  a list of object(CodeData Class)
    def modeling_code(code_list):
        new_code_list = []
        for code in code_list:
            new_code = CodeData(data=code[0], username=code[1], active_mode=code[2])
            new_code_list.append(new_code)
        return new_code_list


# user name data class -> save passwords binned to chat id
class UserData:
    def __init__(self, username: str, user_id: str = 'None', block_mode: int = 0):
        self.username = username
        self.user_id = user_id
        self.block_mode = block_mode

    @staticmethod
    # turning a list of user data to  a list of object(USerData)
    def modeling_user(user_list):
        new_user_list = []
        for user in user_list:
            new_user = UserData(username=user[0], user_id=user[1], block_mode=user[2])
            new_user_list.append(new_user)
        return new_user_list


# DataBase Functional class
class CodeDataBase:
    def __init__(self):
        self.conn = sqlite3.connect("CODE_DATABASE")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS codes(
                            data TEXT PRIMARY KEY ,
                            username TEXT,
                            active_mode INTEGER
                            )""")
        self.conn.commit()

    def insert_data(self, code: CodeData):
        try:
            self.cur.execute("INSERT INTO codes VALUES (?, ?, ?)", (code.data, code.username, code.active_mode))
            self.conn.commit()
            return "Code Successfully Added"
        except:
            return "frequented code"

    def update_data(self, code: CodeData):
        self.remove_data(code)
        self.insert_data(code)
        # self.cur.execute("""UPDATE codes SET username = ? AND active_mode = ?
        #                     WHERE data = ? """, (code.username, code.active_mode, code.data))
        self.conn.commit()

    def remove_data(self, code: CodeData):
        self.cur.execute("""DELETE FROM codes
                            WHERE data = ?
                            """, (code.data,))
        self.conn.commit()
        return "Code removed successfully"

    def pop_data(self, user: UserData):
        self.cur.execute("""SELECT * FROM codes
                            WHERE active_mode = 1
                            LIMIT 1
                            """)
        data = self.cur.fetchone()[0]
        new_code_data = CodeData(data=data, username=user.username, active_mode=0)
        self.update_data(new_code_data)
        return new_code_data

    def remove_expired_data(self):
        self.cur.execute("""DELETE FROM codes
                            WHERE active_mode = 0
                            """)
        self.conn.commit()
        return "all Deactivated code removed successfully"

    def show_all_data(self):
        self.cur.execute("""SELECT data FROM codes
                            WHERE active_mode = 1
                            """)
        return self.cur.fetchall()

    def show_daily_report(self):
        self.cur.execute("""SELECT username,data FROM codes
                            WHERE active_mode = 0
                            ORDER BY username
                            """)
        return self.cur.fetchall()


# DataBase Functional class
class UserDataBase:
    def __init__(self):
        self.conn = sqlite3.connect("CODE_DATABASE")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            username TEXT PRIMARY KEY ,
                            user_id TEXT,
                            block_mode INTEGER
                            )""")
        self.conn.commit()

    def insert_data(self, user: UserData):
        try:
            self.cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user.username, user.user_id, user.block_mode))
            self.conn.commit()
            return "UserName Successfully Added"
        except:
            self.update_data(user)
            return "frequented UserName"

    def update_data(self, user: UserData):
        self.remove_username(user)
        self.insert_data(user)
        # self.cur.execute("""UPDATE users SET user_id = :id AND block_mode = :block
        #                     WHERE username = :username """,
        #                  {"username": user.user_id, "id": user.block_mode, "block": user.username})
        self.conn.commit()

    def remove_username(self, user: UserData):
        self.cur.execute("""DELETE FROM users
                            WHERE username = ?
                            """, (user.username,))
        self.conn.commit()
        return "Username removed successfully"

    def get_username(self, userid: str):
        self.cur.execute("""SELECT * FROM users ORDER BY block_mode DESC """)
        new_user_list = self.cur.fetchall()
        for user in new_user_list:
            if user[1] == userid:
                return UserData(user[0], user[1], user[2])
        random_password = generate_random_password()
        return UserData(random_password, userid, block_mode=1)

    def get_userid(self, username: str):
        self.cur.execute("""SELECT * FROM users ORDER BY block_mode DESC """)
        new_user_list = self.cur.fetchall()
        for user in new_user_list:
            if user[0] == username:
                return UserData(user[0], user[1], user[2])
        random_password = generate_random_password()
        return UserData(username, random_password, block_mode=1)

    def set_userid(self, user: UserData):
        self.cur.execute("""SELECT * FROM users ORDER BY block_mode DESC""")
        new_user_list = self.cur.fetchall()
        for users in new_user_list:
            if users[0] == user.username:
                self.update_data(UserData(username=user.username,
                                          user_id=user.user_id,
                                          block_mode=users[2]))
                if users[2] == 1:
                    return "access Denied"
                else:
                    return "successfully Registered"
        return "Registration failed"

    def show_all_username(self):
        self.cur.execute("""SELECT username,user_id FROM users
                            WHERE block_mode = 0
                            """)
        return self.cur.fetchall()

    def show_all_blocked(self):
        self.cur.execute("""SELECT username,user_id FROM users
                            WHERE block_mode = 1
                            """)
        return self.cur.fetchall()


# app will know the use case of input
RESPOND_STATE = "default"


def responses(input_text):
    user_message = str(input_text).split()
    global RESPOND_STATE

    if RESPOND_STATE == "add_code":
        RESPOND_STATE = 'default'
        result = ''
        code_database = CodeDataBase()
        for purchase_code in user_message:
            new_code = CodeData(purchase_code)
            result += code_database.insert_data(new_code)
            result += '\n'
        return result

    if RESPOND_STATE == "add_user":
        RESPOND_STATE = 'default'
        user_database = UserDataBase()
        result = ''
        for user in user_message:
            new_user = UserData(username=user)
            result += user_database.insert_data(new_user)
            result += '\n'
        return result

    if RESPOND_STATE == "remove_user":
        RESPOND_STATE = 'default'
        result = ''
        user_database = UserDataBase()
        for user in user_message:
            new_user = UserData(username=user)
            result += user_database.remove_username(new_user)
            result += '\n'
        return result

    if RESPOND_STATE == "add_block":
        RESPOND_STATE = 'default'
        result = ''
        user_database = UserDataBase()
        for user in user_message:
            if not user.isnumeric():
                new_user = user_database.get_userid(username=user)
                new_user.block_mode = 1
                result += user_database.insert_data(new_user)
                result += " blocked successfully"
                result += '\n'
            else:
                new_user = user_database.get_username(user)
                new_user.block_mode = 1
                result += user_database.insert_data(new_user)
                result += " blocked successfully"
                result += '\n'
        return result

    if RESPOND_STATE == "remove_block":
        RESPOND_STATE = 'default'
        result = ''
        user_database = UserDataBase()
        for user in user_message:
            if not user.isnumeric():
                new_user = user_database.get_userid(username=user)
                user_database.remove_username(new_user)
                result += "username Unblocked successfully\n"
            else:
                new_user = user_database.get_username(user)
                user_database.remove_username(new_user)
                result += "userID removed from block list\n"
        return result
    return "Chat is deactivate pls use the button interface\n\nif u have problem press /help \n"


print("bot Started ...")
# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN = range(10)


def enter_alarm(update: Update, context: CallbackContext):
    current_user_id = update.message.chat_id
    current_user_first_name = update.message.chat.first_name
    current_user_last_name = update.message.chat.last_name
    now = datetime.now()
    data_time = now.strftime("%m/%d ,%H:%M:%S")
    for admin_chat_id in admin_list:
        context.bot.send_message(admin_chat_id,
                                 "user name: {first} {last}, user id: {id}  \nhas STARTED the bot at {time}"
                                 .format(first=current_user_first_name,
                                         last=current_user_last_name,
                                         id=current_user_id,
                                         time=str(data_time)))


def start_command(update: Update, context: CallbackContext):
    global RESPOND_STATE
    RESPOND_STATE = "add_block_user"  # put command handler in default state

    enter_alarm(update, context)  # let amin know some one is using a bot

    current_user_id = update.message.chat_id
    current_user_name = update.message.chat.first_name
    context.bot.sendChatAction(current_user_id, "TYPING")
    update.message.reply_text("HI {first}, i hope you enjoy and have good experience.".format(first=current_user_name))

    keyboard = [
        [
            InlineKeyboardButton("Admin Panel", callback_data='admin'),
            InlineKeyboardButton("User Panel", callback_data='user'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("in this bot you get a code and manage them \nPlease select your access panel",
                              reply_markup=reply_markup)
    return FIRST


def start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Admin Panel", callback_data='admin'),
            InlineKeyboardButton("User Panel", callback_data='user'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="welcome,Select your access panel", reply_markup=reply_markup)
    return FIRST


def admin_panel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard_1 = [
        [
            InlineKeyboardButton("User Management", callback_data='userManage'),
            InlineKeyboardButton("Code Management", callback_data='codeManage'),
        ],
        [InlineKeyboardButton("« Back to home", callback_data='back')],
    ]
    keyboard_2 = [[InlineKeyboardButton("« Back to home", callback_data='back')]]

    new_chat_id = str(update.callback_query.message.chat.id)
    if new_chat_id in admin_list:
        reply_markup = InlineKeyboardMarkup(keyboard_1)
        query.edit_message_text(
            text="Welcome Admin!!! ", reply_markup=reply_markup
        )
    else:
        reply_markup = InlineKeyboardMarkup(keyboard_2)
        query.edit_message_text(
            text="You are not registered as Admin!!?", reply_markup=reply_markup
        )
    return FIRST


def user_panel(update: Update, context: CallbackContext) -> int:
    new_userid = str(update.callback_query.message.chat.id)
    user_database = UserDataBase()
    new_user = user_database.get_username(userid=new_userid)

    query = update.callback_query
    query.answer()

    keyboard_1 = [
        [InlineKeyboardButton("$ Get Code", callback_data='getCode')],
        [InlineKeyboardButton("« Back to home", callback_data='back')],
    ]
    keyboard_2 = [
        [InlineKeyboardButton("« Back to home", callback_data='back')]
    ]

    if new_user.block_mode == 0:
        reply_markup = InlineKeyboardMarkup(keyboard_1)
        query.edit_message_text(
            text="Welcome to User panel {username}".format(username=new_user.username),
            reply_markup=reply_markup
        )
        return SECOND
    else:
        reply_markup = InlineKeyboardMarkup(keyboard_2)
        query.edit_message_text(
            text="""Access denied pls Register ur Username
                    \nlogin to your account like pattern:
                    \n/register <username> """,
            reply_markup=reply_markup
        )
        return FIRST


def user_manager(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Block list management", callback_data='block'),
            InlineKeyboardButton("UserName management", callback_data='password'),
        ],
        [InlineKeyboardButton("Daily Report", callback_data='report')],
        [InlineKeyboardButton("« Back to Admin panel", callback_data='admin')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="select your dashboard menu", reply_markup=reply_markup
    )
    return FIRST


def block_list_manager(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Add user", callback_data='addBlock'),
            InlineKeyboardButton("remove user", callback_data='removeBlock'),
        ],
        [InlineKeyboardButton("« Back to User manager", callback_data='userManage')],
    ]
    # user database
    user_database = UserDataBase()
    user_list = user_database.show_all_blocked()

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="this is your block list:\n\n{blocked}".format(blocked=tabulate.tabulate(
            user_list,
            tablefmt="orgtbl")),
        reply_markup=reply_markup
    )
    return FIRST


def add_block_user(update: Update, context: CallbackContext):
    global RESPOND_STATE
    RESPOND_STATE = "add_block"
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Enter userName or userID to block\nlike pattern:\nuser1 user2 userID3 ...")
    return ConversationHandler.END


def remove_block_user(update: Update, context: CallbackContext):
    global RESPOND_STATE
    RESPOND_STATE = "remove_block"
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Enter userName or userID to Unblock\nlike pattern:\nuser1 user2 userID3 ...")
    return ConversationHandler.END


def username_manager(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Add username", callback_data='addUsername'),
            InlineKeyboardButton("remove username", callback_data='removeUsername'),
        ],
        [InlineKeyboardButton("« Back to User manager", callback_data='userManage')],
    ]
    # user database
    user_database = UserDataBase()
    user_list = user_database.show_all_username()

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="this is your Username list:\n\n{users}".format(users=tabulate.tabulate(
            user_list,
            tablefmt="orgtbl")),
        reply_markup=reply_markup
    )
    return FIRST


def add_user(update: Update, context: CallbackContext):
    global RESPOND_STATE
    RESPOND_STATE = "add_user"
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Enter userName to add\nlike pattern:\nuser1 user2 ...")
    return ConversationHandler.END


def remove_user(update: Update, context: CallbackContext):
    global RESPOND_STATE
    RESPOND_STATE = "remove_user"
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Enter userName to remove\nlike pattern:\nuser1 user2 ...")
    return ConversationHandler.END


def report_manager(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("restart Records", callback_data='resReport')],
        [InlineKeyboardButton("« Back to User manager", callback_data='userManage')],
    ]
    # access to database
    code_database = CodeDataBase()
    code_list = code_database.show_daily_report()

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="this is your Daily Report :\n\n{code_table}".format(code_table=tabulate.tabulate(
            code_list,
            tablefmt="orgtbl",
            showindex=True)),
        reply_markup=reply_markup)
    return FIRST


def restart_daily_report(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("« Back to User manager", callback_data='userManage')]
    ]
    # access to database
    code_database = CodeDataBase()
    result = code_database.remove_expired_data()

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=result,
        reply_markup=reply_markup)
    return FIRST


def code_manager(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Add new code", callback_data='addCode')],
        [InlineKeyboardButton("« Back to Admin panel", callback_data='admin')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    code_database = CodeDataBase()
    code_list = code_database.show_all_data()

    query.edit_message_text(
        text="this is your code list:\n\n{code_table}".format(code_table=tabulate.tabulate(
            code_list,
            tablefmt="orgtbl",
            showindex=True)),
        reply_markup=reply_markup)
    return FIRST


def add_code(update: Update, context: CallbackContext):
    global RESPOND_STATE
    RESPOND_STATE = "add_code"
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Enter your codes\nlike pattern:\ncode1 code2 ...")
    return ConversationHandler.END


# GIVE NEW CODE TO USER
def end(update: Update, context: CallbackContext) -> int:
    new_userid = str(update.callback_query.message.chat.id)
    query = update.callback_query
    query.answer()

    # data base connections
    user_database = UserDataBase()
    new_user = user_database.get_username(userid=new_userid)
    code_database = CodeDataBase()
    new_code = code_database.pop_data(new_user)
    query.edit_message_text(text=new_code.data)

    code_number = len(code_database.show_all_data())
    if code_number < 10:
        for admin_chat_id in admin_list:
            context.bot.send_message(admin_chat_id,
                                     "CODE ALARM!!!\nIn term of codes, we have less than {number} code"
                                     .format(number=code_number))
    return ConversationHandler.END


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(""" pls Select /Start Commend from Menu
                                \nlogin to your account like pattern:
                                \n/register <username> 
                                \nOR contact with admin to report a Error""")


def check_user(user_info, userid: str):
    try:
        user_database = UserDataBase()
        user_name = user_info[1]
        bloc_list = user_database.show_all_blocked()
        for blocked in bloc_list:
            if userid == blocked[1] or user_name == blocked[0]:
                return "access denied"
        new_user = UserData(user_name, userid)
        return user_database.set_userid(new_user)
    except:
        return """ \nlogin to your account like pattern:
                    \n/register  <username> 
                    \nOR contact with admin to report a Error"""


def register_command(update: Update, context: CallbackContext):
    user_id = str(update.message.chat_id)
    user_name = str(update.message.text).split()
    check_user_result = check_user(user_name, user_id)
    update.message.reply_text(check_user_result)


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    response = responses(text)
    update.message.reply_text(response)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(seconder_token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            FIRST: [
                CallbackQueryHandler(admin_panel, pattern='^' + 'admin' + '$'),
                CallbackQueryHandler(user_panel, pattern='^' + 'user' + '$'),
                CallbackQueryHandler(start_over, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(block_list_manager, pattern='^' + 'block' + '$'),
                CallbackQueryHandler(username_manager, pattern='^' + 'password' + '$'),
                CallbackQueryHandler(report_manager, pattern='^' + 'report' + '$'),
                CallbackQueryHandler(user_manager, pattern='^' + 'userManage' + '$'),
                CallbackQueryHandler(code_manager, pattern='^' + 'codeManage' + '$'),
                CallbackQueryHandler(add_code, pattern='^' + 'addCode' + '$'),
                CallbackQueryHandler(add_block_user, pattern='^' + 'addBlock' + '$'),
                CallbackQueryHandler(remove_block_user, pattern='^' + 'removeBlock' + '$'),
                CallbackQueryHandler(add_user, pattern='^' + 'addUsername' + '$'),
                CallbackQueryHandler(remove_user, pattern='^' + 'removeUsername' + '$'),
                CallbackQueryHandler(restart_daily_report, pattern='^' + 'resReport' + '$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + 'back' + '$'),
                CallbackQueryHandler(end, pattern='^' + 'getCode' + '$'),
            ],
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("register", register_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()  # delay for respond time
    updater.idle()


if __name__ == '__main__':
    main()
