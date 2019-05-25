# Google Forms to Trello converter
Tested under python 3.6

This app uses the following packages to read new replies and convert them to Trello tasks:
 - https://github.com/sarumont/py-trello
 - https://github.com/burnash/gspread
 
 ## Installation
 Clone to local folder
 Run `pip install -r requirements.txt`
 
 ## Usage
 Define the following environment parameters:
 
 **Trello**:
 1. TRELLO_API_KEY *(from: https://trello.com/app-key)*
 2. TRELLO_TOKEN *(from: https://trello.com/app-key)*
 3. TRELLO_BOARD_NAME (the name of the board you want to post the tickets at, case sensitive)
 3. TRELLO_LIST_NAME (the name of the category you want to post the ticket under, for example, "To Do")
 
 **Google**:
 *(from various places)*
 1. SCOPES:   
 defaults to ["https://www.googleapis.com/auth/spreadsheets"]
 2. SPREADSHEET_ID:  
  \<the id of the spreadsheet you want to read>
 3. SHEET_INDEX:  
  the id of the sheet in the spreadsheet (usually 0) 
 4. CREDENTIALS:  
   the json configuration of the Google API user **in one line** (an example for creating one can be seen here: https://github.com/juampynr/google-spreadsheet-reader)

 Run `python3 main.py`
 
 ##TODO
 - [ ] exception handling
 - [ ] logging
 - [ ] notifications
 - [ ] customization