## Usage
This library is really easy to use:

```python
from supermail import EmailClient

# define email client
gmail = EmailClient("your_email@gmail.com", "your_password")

# get all messages
messages = gmail.read() # if you need only unread, set parameter filter=['UNSEEN']

# for each message
for msg in messages:
	# get message info
	print(msg.subject())
	print(msg.message())
	print(msg.sender())
	# get attachments
	attachments = msg.attachments('./temp') # returns a list of filenames saved in specified dir

# send a message with attachments
gmail.send('recipient@gmail.com', 'Nice subject', 'Nice message', \
	cc='xxx@domain.it',
	attachments=['/path/to/pdf.pdf', '/path/to/image.png'])
```

## Note
In order to use GMail, you need to log into [your security page](https://myaccount.google.com/security) and:
1. enable two-step verification
2. right below, it will appear an option called **App Password**. Create a new one that you will be able to use with supermail.


## Other email? No problem!
You can specify custom imap and smtp addresses and ports:

```python
email_address = "your_email@gmail.com"
email_pwd = "your_password"
imap_server = "imap.gmail.com"
imap_port   = 993
smtp_server='smtp.gmail.com'
smtp_port=587

# define email client
gmail = EmailClient(email_address, email_pwd, imap_server, imap_port, smtp_server, smtp_port)
```


## Install
You can install supermail from PyPI:
```bash
pip install supermail
```

or from the github page:

```bash
pip install git+https://github.com/dros1986/EmailClient.git
```
