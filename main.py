from environs import Env
from trello import TrelloClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Used to work with env parameters
env = Env()

# Loads parameters from .env file
# Note: you should not use a .env file in production
env.read_env()

# Defines the message format. Can be moved to a different file.
msg_format = "**Request submitted by:**\n" \
             "#{user}\n" \
             "**Details**\n" \
             "{message}"


def create_trello_task(client: TrelloClient, title: str, user: str, message: str,
                       trello_board_name=env("TRELLO_BOARD_NAME"), trello_list_name=env("TRELLO_LIST_NAME")):
    """
    This function is used to submit new messages via an existing client
    :param client: an instance of a configured TrelloClient
    :param title: the title of the new ticket
    :param user: the username of the submitter of the ticket
    :param message: the details of the message to be posted on trello
    :param trello_board_name: the name of the board to which the ticket will be posted
    :param trello_list_name: the name of the list (category) to which new messages will be added
    """

    # Try getting the board with the name <TRELLO_BOARD_NAME>. If the board is not found, raise an exception.
    trello_boards = client.list_boards(board_filter=trello_board_name)
    if len(trello_boards) == 0:
        raise LookupError(f'No board named "{trello_board_name}" was found. Please check the spelling of the name.')
    trello_board_name = client.get_board(board_id=trello_boards[0].id)

    # Try getting the list (category) with the name <TRELLO_LIST_NAME> from the selected board.
    # If the list is not found, raise an exception.
    trello_lists = trello_board_name.list_lists()
    # a hack because I didn't manage to make list_filter work
    trello_lists = [x for x in trello_lists if x.name == trello_list_name]
    if len(trello_lists) == 0:
        raise LookupError(f'No list named "{trello_list_name}" was found. Please check the spelling of the name.')
    trello_list_name = trello_lists[0]

    # Add the message to the category, formatted according to <msg_format>
    trello_list_name.add_card(name=title, desc=msg_format.format(user=user, message=message))


def get_google_form():
    # Auth with oauth2
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        env.json('CREDENTIALS'),
        env.json('SCOPES', default=["https://www.googleapis.com/auth/spreadsheets"])
    )

    # Authorize with Google API
    gc = gspread.authorize(credentials)

    # Load desired spreadsheet
    sheet = gc.open_by_key(env('SPREADSHEET_ID'))

    # Return the desired sheet under the spreadsheet
    return sheet.get_worksheet(env.int('SHEET_INDEX', default=0, ))


def main():
    # create a client for Trello API
    client = TrelloClient(
        api_key=env("TRELLO_API_KEY"),
        token=env("TRELLO_TOKEN")
    )

    # load the form (by default uses the first sheet)
    form = get_google_form()
    rows = form.get_all_values()

    for row_id, row in enumerate(rows):
        # skip header row
        if row_id == 0:
            continue

        # stop the iteration if we reach an empty row
        if len(row) == 0:
            break

        # skip ill-formatted rows
        if len(row) not in [4, 5] or (len(row) == 5 and row[-1] not in ['submitted', '']):
            continue

        # skip submitted rows
        elif len(row) == 5 and row[-1] == 'submitted':
            continue

        # assume that the order is: user, topic, message
        user, topic, message = row[1:4]

        # submit new ticket to trello
        try:
            # post the ticket
            create_trello_task(client, user=user, title=topic, message=message)

            # mark the ticket as submitted on the sheet
            form.update_acell(f'E{row_id+1}', 'submitted')
        except LookupError as err:
            print(err)


if __name__ == "__main__":
    main()

