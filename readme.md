## Usage
This library is really easy to use:

```python
email_address = "your_email@gmail.com"
email_pwd = "your_password"
imap_server = "imap.gmail.com"
imap_port   = 993
smtp_server='smtp.gmail.com'
smtp_port=587

# define email client
gmail = EmailClient(email_address, email_pwd, imap_server, imap_port, smtp_server, smtp_port)

# get all messages
messages = gmail.read()

# for each message
for msg in messages:
	# get message info
	print(msg.subject())
	print(msg.message())
	print(msg.sender())
	# get attachments
	attachments = msg.attachments('./temp') # returns a list of filenames
	print('---')

# send a message with attachments
gmail.send('recipient@gmail.com', 'Nice subject', 'Nice message', \
	attachments=['/path/to/pdf.pdf', '/path/to/image.png'])
```

## Installation
```bash
pip install <git_repo>
```

## Include it in your git project as submodule
To include EmailClient in your project:
```bash
git submodule add <git_repo>
```
Remember when you clone your project in another place to clone with:
```bash
git clone -- <your_git_repo>
```
