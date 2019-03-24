from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    print("With this program you'll be able to the first five messages where you were congratulated\n")
    print("Make sure you're connected to internet")
    print("You will be asked to grant permission to read your mail. If you did it once, there is no need to do it again")
    print("To grant permission, you will be redirected to your default browser. If you haven't logged in, you'll need to log in\n")
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API for user's profile details
    info = service.users().getProfile(userId='me').execute()
    # Here, we get the total number of messages use received
    number_of_messages = info['messagesTotal']

    # This API calls gives us the user's mail details
    results = service.users().messages().list(userId='me', maxResults=number_of_messages).execute()
    messages = results.get('messages', [])

    list_of_subjects = []
    print("Your results will be ready in a few minutes (Max. 5 minutes)\n")

    # We use this mail loop to get the mail of the user
    for message in messages:
        # This API call returns user's mails
        msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
        # This message decodes the raw message which was encoded in base64 encoding
        msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
        # Converts messages to string from bytes
        mime_msg = email.message_from_bytes(msg_str)
        # We get the main content from this call i.e the mail details
        msg_main = mime_msg.get_content_maintype()
        # Messages can be multipart or just text based. Here, in the if statement we separate those two.
        if msg_main == 'multipart':
            # Payload contains message's main part i.e the text part
            for part in mime_msg.get_payload():
                if part.get_content_maintype() == 'text':
                    filtered = text_filter(part.get_payload())
                    yes_or_no = congratulations(filtered)

                    if yes_or_no == 'yes':
                        # If the congratulations function finds that the message is in fact congratulating the receiver, we use this API call
                        # to find the subject of that mail
                        messageheader= service.users().messages().get(userId="me", id=message["id"], format="full", metadataHeaders=None).execute()
                        headers = messageheader["payload"]["headers"]
                        subject = [i['value'] for i in headers if i['name'] == "Subject"]
                        list_of_subjects.append(subject[0])

        # This code does the same job as the one from line 73-83
        elif msg_main == 'text':
            filtered = text_filter(mime_msg.get_payload())
            yes_or_no = congratulations(filtered)

            if yes_or_no == 'yes':
                messageheader= service.users().messages().get(userId="me", id=message["id"], format="full", metadataHeaders=None).execute()
                headers = messageheader["payload"]["headers"]
                subject = [i['value'] for i in headers if i['name'] == "Subject"]
                list_of_subjects.append(subject[0])

        if len(list_of_subjects)>=5:
            break
    '''
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['id'])
    '''
    print("Subject for messages of congratulations")
    x=1
    for title in list_of_subjects:
        if title == '':
            print('Subject %d: No Subject with this mail' %x)
        else:
            print("Subject %d: %s" %(x, title))
        x = x+1

def text_filter(text):
    # Removes HTML tags from the mail body
    clean = re.compile('<[^>]+>')
    body = re.sub(clean, '', text)
    # Cleans data for further evaluation.
    clean = re.compile('=\s\n')
    body = re.sub(clean, '', body)
    # Removes CSS tags
    clean = re.compile('{[^}]*}')
    body = re.sub(clean, '', body)

    return body

def congratulations(mail):
    # This function is used for sentiment annalysis, in this case, it finds out whether the message is congratulating hte person or not
    result = 'no'

    # Word tokenizer separates the word by space and arranges them in tokens
    tokenized = word_tokenize(mail)

    imp_words = []

    # Removes stopwords i.e the words that does not provide any value to the sentence such as 'a', 'you', 'me'
    stop_words = set(stopwords.words('english'))
    for w in tokenized:
        if w not in stop_words:
            imp_words.append(w)

    # Every word has some related words. In this case, 'congratulations', 'congratulating', 'congratulated' mean the same thing 
    stemmer = SnowballStemmer("english")
    main_word = stemmer.stem("congratulations")
    #imp_words.remove('.')

    # This loop checks if any of the word have the same meaning as congratulations
    for i in range(len(imp_words)):
        stemmed = stemmer.stem(imp_words[i])
        if stemmed == main_word:
            result = 'yes'
            return result
    return imp_words

if __name__ == '__main__':
    main()