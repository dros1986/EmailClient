import os, email
from imapclient import IMAPClient
import smtplib
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
import mimetypes


class EmailMessage:

	DELETED = r'\Deleted'
	SEEN = r'\Seen'
	ANSWERED = r'\Answered'
	FLAGGED = r'\Flagged'
	DRAFT = r'\Draft'
	RECENT = r'\Recent' # This flag is read-only

	def __init__(self, server, msgid, data):
		self.server = server
		self.msgid = msgid
		self.data = data
		self.bytes = data[b'RFC822.SIZE']
		# self.flgs = data[b'FLAGS']


	def subject(self):
		envelope = self.data[b'ENVELOPE']
		return envelope.subject.decode()

	def sender(self):
		envelope = self.data[b'ENVELOPE']
		senders = envelope.from_
		res = []
		for sender in senders:
			res.append([sender.mailbox + sender.host, sender.name])
		return res

	def reply_to(self):
		envelope = self.data[b'ENVELOPE']
		replytos = reply_to.from_
		res = []
		for replyto in replytos:
			res.append([replyto.mailbox + replyto.host, replyto.name])
		return res

	def message(self):
		msg = email.message_from_bytes(self.data[b'RFC822'])
		txt = ''
		if msg.is_multipart():
			for part in msg.walk():
				type = part.get_content_type()
				disp = str(part.get('Content-Disposition'))
				# look for plain text parts, but skip attachments
				if type == 'text/plain' and 'attachment' not in disp:
					charset = part.get_content_charset()
					# decode the base64 unicode bytestring into plain text
					txt = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
					# if we've found the plain/text part, stop looping thru the parts
					break
		return txt

	def attachments(save_dir):
		# get raw content
		raw = email.message_from_bytes(self.data[b'RFC822'])
		# https://github.com/LukeARG/IMAPClient-and-Attachments/blob/master/IMAPCwAttchmnts.py
		# create output dir
		os.makedirs(save_dir, exist_ok=True)
		# Takes the raw data and breaks it into different 'parts' & python processes it 1 at a time [1]
		fns = []
		for part in msg.walk():
			 # if multipart, cannot have attachment
			if part.get_content_maintype() == 'multipart':
				continue
			# check 'Content-Disposition' field. If empty/None, no attach.
			if part.get('Content-Disposition') is None:
				continue
			# if the part isn't a 'multipart' type and has a 'Content-Disposition', get the filename
			file_name = part.get_filename()
			# retrieve file and append to fns
			if bool(file_name):
				fns.append(file_name)
				file_path = os.path.join(save_dir, file_name)
				with open(file_path, 'wb') as f:
					f.write(part.get_payload(decode=True))
		return fns

	def size(self):
		return self.data[b'RFC822.SIZE']

	def flags(self):
		return self.data[b'FLAGS']

	def date(self):
		envelope = self.data[b'ENVELOPE']
		return envelope.date

	def set_as_read(self):
		self.server.add_flags(self.msgid, [EmailMessage.SEEN])




class EmailClient:
	def __init__(self, email_address, email_pwd, imap_server='imap.gmail.com', imap_port=993,
												 smtp_server='smtp.gmail.com', smtp_port=587):
		# set attributes
		self.email_address = email_address
		self.email_pwd = email_pwd
		self.imap_server = imap_server
		self.imap_port = imap_port
		self.smtp_server = smtp_server
		self.smtp_port = smtp_port

	def read(self, filter=['ALL']):
		# connect server
		server = IMAPClient(self.imap_server, use_uid=True)
		server.login(self.email_address, self.email_pwd)
		select_info = server.select_folder('INBOX')
		# retrieve the messages and puts them in a collection [4][5]
		messages = server.search(filter)
		response = server.fetch(messages, ['FLAGS', 'BODY', 'RFC822.SIZE', 'ENVELOPE', 'RFC822'])
		# instantiate messages
		msgs = []
		for msgid, data in response.items():
			msgs.append(EmailMessage(server, msgid, data))
		# # close connection
		# server.logout()
		return msgs

	def file2part(self, file):
		# get type of file
		content_type, encoding = mimetypes.guess_type(file)
		if content_type is None or encoding is not None:
			content_type = 'application/octet-stream'
		# convert in proper mime
		main_type, sub_type = content_type.split('/', 1)
		if main_type == 'text':
			fp = open(file, 'rb')
			msg = MIMEText(fp.read(), _subtype=sub_type)
			fp.close()
		elif main_type == 'image':
			fp = open(file, 'rb')
			msg = MIMEImage(fp.read(), _subtype=sub_type)
			fp.close()
		elif main_type == 'audio':
			fp = open(file, 'rb')
			msg = MIMEAudio(fp.read(), _subtype=sub_type)
			fp.close()
		else:
			fp = open(file, 'rb')
			msg = MIMEBase(main_type, sub_type)
			msg.set_payload(fp.read())
			fp.close()
		# add file as header
		filename = os.path.basename(file)
		encoders.encode_base64(msg)
		msg.add_header('Content-Disposition', 'attachment', filename=filename)
		# return part
		return msg


	def send(self, to, subject, text, attachments=None):
		# log into SMTP server
		server = smtplib.SMTP(host=self.smtp_server, port=self.smtp_port)
		server.starttls()
		server.login(self.email_address, self.email_pwd)
		# create message
		message = MIMEMultipart()
		message['to'] = to
		message['from'] = self.email_address
		message['subject'] = subject
		message.attach(MIMEText(text))
		# add attachment
		if attachments is not None:
			if not isinstance(attachments, list):
				attachments =  [attachments]
			 # attach each file as part to the message
			for attachment in attachments:
				part = self.file2part(attachment)
				message.attach(part)
				# https://stackoverflow.com/questions/26582811/gmail-python-multiple-attachments
		# send email
		server.sendmail(self.email_address, to, message.as_string())
		server.close()
