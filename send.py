from argparse import ArgumentParser
from EmailMessage import EmailMessage

def main():
	parser = ArgumentParser(description='Mass Automailer. To actually send emails, pass \'-x\' flag. Otherwise, app runs in test mode.')
	
	parser.add_argument('-e', dest='email', default='', help='Email to send from.', required=True)
	parser.add_argument('-s', dest='password', default='', help='Password for email account.', required=True)
	parser.add_argument('-j', dest='subject', default='', help='Email subject.', required=True)
	parser.add_argument('-p', dest='plaintext_file', default='plaintext.txt', help='Text file with email plaintext content.')
	parser.add_argument('-r', dest='receivers_file', default='emails.csv', help='CSV file where the receivers are located with format: email,vars*. INCLUDE COLUMN HEADERS (these can\'t have spaces in them).')
	parser.add_argument('-t', dest='sleep_time', default=2, type=int, help='Sleep time between recipients, in seconds.')
	parser.add_argument('-l', dest='logging', action='store_true', help='Include this option to log the successful sends to a text file.')
	# parser.add_argument('-w', dest='html_file', default='index.html', help='File with HTML email content.')
	parser.add_argument('-x', dest='test', action='store_false', help='Disable test mode. See \'EmailMessage.py\' for details')

	args = parser.parse_args()

	config = {}
	config['sleep_time'] = args.sleep_time
	config['receivers_file'] = args.receivers_file
		# config['html_file'] = args.html_file
	config['text_file'] = args.plaintext_file
	config['subject'] = args.subject
	config['sender_email'] = args.email
	config['sender_password'] = args.password
	config['logging'] = args.logging
	# since test mode is such a crucial factor in the behavior of the script, I decided to keep it outside of the config dict
	sender = EmailMessage(config, test=args.test)
	sender.send_mail()


if __name__ == '__main__':
	main()
