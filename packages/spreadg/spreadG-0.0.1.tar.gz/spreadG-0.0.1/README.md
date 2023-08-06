# SpreadG
 SpreadG is a small wrapper around the Google Sheets API (v4) and gspread 3.6.0 to provide more convenient access to Google Sheets from Python scripts and plot graphs with the help of Matplotlib.

<a href='https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the_api_name'>Turn on the API</a>, download an OAuth client ID as JSON file, and start working.

# Installation
```bash
pip install spreadg
```
This will also install google-api-python-client and its dependencies, notably httplib2 and oauth2client, as required dependencies.

# Quickstart
```python
from spreadg import *
data=dataloader('credentials.json', "Sheetname")
df=to_df(data)
fig = plotter(df, X, y)
fig.savefig("something.png")
```

author: Himanshu Pal<br>
mailto: palhimanshu997[at]gmail[.]com