# Gmail-API-and-Sentiment-Analysis
Send a request to Gmail API and shows subject of first five messages which might be congratulating the receiver.

## Overview
This uses Gmail API call to return user's messages and then uses python NLTK library for text parsing and returns the subject of the first five mail which satisfy the condition.

## Requirements Requirements to run the program are:- 
**Python 3.x** </br>
**Pickle** This comes installed with python package. </br>
**Gmail API call modules** pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib </br>
**nltk**  1. pip install -U nltk </br>
          2. Open python interpreter </br>
          3. Type nltk.download() </br>
          4. From the dialog box, select choices and download </br></br>
          
**Gmail API** 1. Go to https://console.developers.google.com/ </br>
2. In the top left corner of the page, click on "Select a project".</br>
3. In the dialog box that opens up, click on "New project" in the top right corner.</br>
4. Type your project name, and click select.</br>
5. Click on "Enable API and service" on the page that opens up.</br>
6. Type in "Gmail API" in the search bar and click on the result.</br>
7. In the resulting page, click on Enable API. </br>
8. Click on "CREATE CREDENTIALS" on the next page.</br>
9. On the next page, choose "Gmail API", then select "Other UI(e.g. Windows, CLI tool) and then after selecting the button with the label "User data" click on "What credentials do I need" and grant permission.</br>
10. In the new tab that open up, type in application name and click save.</br>
11. Switch back to the main window and make click "Refresh".</br>
12. After that, click on "Create OAuth Client ID".</br>
13. Download the client ID that is generated.</br>
14. Rename the file to "credentials.json" and move it to the folder where the python script congratlations.py is located.</br>

## Further Developments 
Gmail API is very extensive but at the same time, very difficult to understand from the documentation.</br>
I'll try and make python scripts for the major API calls as tutorial. And maybe sprinkle a bit of text analysis and machine learning.

##### Feel free to improve the given code or the readme. Ideas are always welcome!

###### Thanks for reading!</br>TPT
