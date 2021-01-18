import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from spotify_music_adder import add_saved_track_by_id, get_tracks_for_search_text

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# states for the conversation as ENUM
SEARCH, ADD_TRACK = range(2)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    user_id = update.message.from_user.id

    # trivial way to make sure only you can add new songs to your account
    if user_id != 1034723625:
        logger.warning(f"User {user_id} was trying to start a conversation.")
        update.message.reply_text("Only the owner of this bot is allowed to add new songs to their playlist.")

        return ConversationHandler.END

    logger.info(f"Conversation started with user {user_id}")
    update.message.reply_text(
        "Hi! I am the Spotify Track Adder Bot.\n\n"
        "Simply send me the name of the song you want to add. (e.g. Acivii SOS)\n"
        "I will then give you options and you can add it to your saved tracks.")

    return SEARCH


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def search_track(update, context):
    """Get the user song name from the user and start the track adding process
    Send a numbered list with the possibly meant songs.
    """
    user_id = update.message.from_user.id
    song_name = update.message.text
    logger.info(f"User {user_id} is trying to add {song_name}.")

    # search for the possible tracks
    found_tracks = get_tracks_for_search_text(song_name)
    found_tracks_dict = {}

    reply_keyboard = []
    curr_row = []

    for index, track in enumerate(found_tracks):
        track_name = f"{track[0]} - {track[1]}"
        curr_row.append(track_name)

        # assign the track name to referebce when a selection was made
        found_tracks_dict[track_name] = track

        # after every second element, create a new entry in the keyboard
        if index % 2 == 1:
            reply_keyboard.append(curr_row)
            curr_row = []

    # persist the dict in the context to be used in the next state
    context.user_data["found_tracks_dict"] = found_tracks_dict

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Please select the wanted song.", reply_markup=markup)

    return ADD_TRACK


def add_new_track(update, context):
    """Add the track that was selected by the user to the playlist"""

    # get the dict of tracks persisted in the previous search stage
    found_tracks_dict = context.user_data["found_tracks_dict"]

    selection = update.message.text
    user_id = update.message.from_user.id
    track = found_tracks_dict[selection]

    # create track name from artist and song
    track_name = f"{track[0]} - {track[1]}"

    # trigger the request to add it to the saved tracks list
    add_saved_track_by_id(track[2])

    logger.info(f"Added {track_name} to saved tracks for user {user_id}")
    update.message.reply_text(f"Added {track_name} to saved tracks.")

    return SEARCH


def cancel(update, context):
    """Inform the user that the conversation was canceled."""
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the converstation")
    update.message.reply_text("Bye! I hope we can talk again some day.")

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1154426738:AAGUe3G9KXjHSd7vDRGpjaAWkz0OL59Slhg", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SEARCH: [MessageHandler(Filters.text, search_track)],
            ADD_TRACK: [MessageHandler(Filters.text, add_new_track)]
        },

        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the polling process and run the bot until you press Ctrl-C
    # or the process receives a termination signal
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()