import smtplib, time, os, csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailMessage:
	"""
	Simple script to automatically mass mail a message to a set of recipients 
	"""
	def __init__(self, config, test=True):
		"""
		test = BOOLEAN -- are you in test mode? if so, this won't actually send the email, 
			   but print the config info instead to avoid accidental mishaps
		config = {
			'sleep_time': INT -- number of seconds to sleep in between each email send,
			'receivers_file': STRING -- filename of text file with receivers of the email: one per line,
			# 'html_file': STRING, optional -- filename of HTML email content,
			'text_file': STRING -- filename of plaintext content,
			'subject': STRING -- subject of email,
			'sender_email': STRING -- who this email is coming from,
			'sender_password': STRING -- password for the sender account
		}
		"""
		self.test = test
		self.logging = config['logging']
		if os.path.exists(config['receivers_file']):
			self.__receivers = {}
			with open(config['receivers_file'], 'r') as f:
				csv_reader = csv.reader(f, delimiter=',')
				self.__var_names = next(csv_reader)
				n = len(self.__var_names)
				for item in csv_reader:
					self.__receivers[item[0]] = {}
					self.__receivers[item[0]][self.__var_names[0]] = item[0]
					for i in range(1, n):
						self.__receivers[item[0]][self.__var_names[i]] = item[i]
		else:
			self.__receivers = None
		# if os.path.exists(config['html_file']):
		# 	with open(config['html_file'], 'r') as f:
		# 		self.__html_content = f.read()
		# else:
		# 	self.__html_content = False
		if os.path.exists(config['text_file']):
			with open(config['text_file'], 'r') as f:
				self.__text_content = str(f.read())
		self.__subject = config['subject']
		self.__sender_email = config['sender_email']
		self.__sender_password = config['sender_password']
		self.__sleep_time = config['sleep_time']
		self.__successful_sends = []

	def get_recievers(self):
		"""
		accessor for receivers
		"""
		return self.__receivers

	def get_sender_email(self):
		"""
		accessor for sender email
		"""
		return self.__sender_email

	def get_hashed_sender_password(self):
		"""
		accessor for password, safety is a priority to return a hash value.
		"""
		return hash(self.__sender_password)

	def get_text_content(self):
		"""
		accessor for text content
		"""
		return self.__text_content

	# def get_html_content(self):
		"""
		accessor for html content
		"""
		# return self.__html_content

	def get_subject(self):
		"""
		accessor for email subject
		"""
		return self.__subject

	def get_vars(self):
		"""
		accessor for var names
		"""
		return self.__var_names

	def get_successful_sends(self):
		"""
		accessor for successful sends just in case it fails and you want to know who the email went to
		"""
		return self.__successful_sends

	def add_successful_send(self, sender):
		"""
		mutator for successful send
		"""
		self.__successful_sends.append(sender)
		return

	def send_mail(self):
		"""
		actually send the email. this looks at all the inputs and makes sure everything is good, and if so,
		it asks user for confirmation. If the user confirms, it sends the email as specified
		"""
		if self.test:
			# if we're in testing mode, just print out the config info
			print('======================== CONFIG INFO ========================')
			print('Sender email: \n\t' + self.get_sender_email())
			print('\nEmail subject: \n\t' + self.get_subject())
			print('\nReceivers: \n\t' + ', '.join(self.get_recievers()))
			print('\nVariables per receiver: \n\t' + ', '.join(self.get_vars()))
			print('\nText content: \n\n' + self.get_text_content())
			# print('\nHTML content: \n' + self.get_html_content())
			print('====================== CONFIG INFO END ======================')
			print('In order to actually send the email, please pass the -x flag.')
		else:
			# check to see if anything important is missing
			if None in [self.__receivers, self.__text_content, self.__subject, self.__sender_email, self.__sender_password]:
				print('One of your inputs seems to be missing or of type None. Please try again')
				return -1

			# confirm that the user really wants to send this
			response = input('Are you sure you want to send this email? [Y]es to continue, [N]o to abort.\n')
			if response.lower() in ['y', 'yes']:				
				# create the email server
				print('Starting server -----')
				mail = smtplib.SMTP('smtp.gmail.com', 587)
				mail.ehlo()
				mail.starttls()
				print('SMTP Server STARTED -----')

				# try to login the user
				print('Logging in user -----')
				try:
					mail.login(self.get_sender_email(), self.__sender_password)
				except:
					print('LOGIN ERROR -- TRY AGAIN')
					return -1
				print('Login successful! -----')
				# the dynamic part. I know this isn't computationally super efficient (subject, sender, object init are repeated per sender)
				# however, due to some MIME intricacies that I don't even fully understand, if you want to vary the message per sender
				# which we are doing (the variables), you can't simply 'del' the field out, and reattaching causes issues
				# bottom line, those few lines only take a little bit of extra time per email to execute, and this script will never be run
				# for over like 500 people, so it doesn't matter
				for receiver in self.__receivers.keys():
					# create the message
					msg = MIMEMultipart('alternative')
					msg['Subject'] = self.get_subject()
					msg['From'] = self.get_sender_email()
						# print('Attaching plaintext email content for {} -----'.format(receiver))
					# this is the line of code that fills in the variables
					tmp = self.get_text_content().format(**self.__receivers[receiver])
					msg.attach(MIMEText(tmp, 'plain'))
						# print('Attaching plaintext email content DONE -----')
						# print('Attaching HTML email content -----')
						# if self.get_html_content():
						# 	msg.attach(MIMEText(self.get_html_content(), 'html'))
						# print('Attaching HTML email content DONE -----')
					
					msg['To'] = receiver
					try:
						mail.sendmail(self.get_sender_email(),
									  receiver, msg.as_string())
					except:
						# some contingencies if stuff breaks.
						print('An exception occurred. Please try again.')
						print('Here is a list of people the email was successfully sent to:\n\t')
						print(self.get_successful_sends())
						print('This has been written to disk for your convenience as \'successful_sends.txt\'')
						with open('successful_sends.txt', 'a+') as f:
							for i in self.get_successful_sends():
								f.write(i)
								f.write('\n')
						return -1
					print('Mail sent successfully to ' + receiver + '. Waiting ' +
						  str(self.__sleep_time) + ' seconds before next send.')
					self.add_successful_send(receiver)
					# MAKE SURE NO DOUBLE-SENDS HAPPEN
					del msg['To']
					del msg['From']
					del msg['Subject']
					# this is here so GMail isn't sussed out by send rate
					time.sleep(self.__sleep_time)

				mail.quit()
				print("All emails sent successfully!")
				# I realized this could be convenient outside of a disaster situation, so it's a command line arg now.
				if self.logging:
					with open('successful_sends.txt', 'a+') as f:
						f.write('For email with subject {}:\n'.format(self.get_subject))
						for i in self.get_successful_sends():
							f.write(i)
							f.write('\n')
						f.write('\n')
					print('Recipients are saved to the file \'successful_sends.txt\' for your convenience.')
				return 0
			else:
				print('Exiting Program')
				return -1
