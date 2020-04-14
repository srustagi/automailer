# Description
A simple Python script to send mass emails with variable fields to a set of recipients.

# Notes
This script only works for Gmail accounts. You also need to have support for [less secure apps](https://myaccount.google.com/lesssecureapps) enabled, or you'll keep getting login errors.

# Known Restrictions
- the CSV file for the receivers should always start with the column `email`, which is the email for that particular person. After this, you can include any number of variable columns as needed.
- the CSV file for the receivers SHOULD INCLUDE THE COLUMN NAMES. Don't omit them or **everything will break**.
- the column names can only have alphanumeric characters and underscores. **no spaces**
- the variable fields in the plaintext email file ***MUST*** match the CSV column names exactly

# Setup
Following all of those rules [above](#known-restrictions), make a a text file with your email message. For any place in the message where content will be dynamically replaced (on a per-receiver basis), replace that word[s] with the variable name in curly braces. For example, `{organization_name}`, `{var1}`, etc. Remember that these variables must match the CSV column headers in number and content.

Your CSV file should follow a format like this (***including column names***):
| email              	| var1                 	| var2                 	| var3                 	| ... 	|
|--------------------	|----------------------	|----------------------	|----------------------	|-----	|
| srustagi@180dc.org 	| var1_value_for_shiv  	| var2_value_for_shiv  	| var3_value_for_shiv  	| ... 	|
| kkapur@180dc.org   	| var1_value_for_kabir 	| var2_value_for_kabir 	| var3_value_for_kabir 	| ... 	|
| ...                	| ...                  	| ...                  	| ...                  	| ... 	|

If you run the comnmand in its barest form (assuming you use default filenames and sleep values), it looks like `python3 send.py -e EMAIL -s PASSWORD -j SUBJECT`. However, this command doesn't actually send the email (another safety feature). Instead, it prints out the given configuration. To actually send the emails, you need to disable this test mode by passing the `-x` flag.

# Usage
`python3 send.py [-h] -e EMAIL -s PASSWORD -j SUBJECT [-p PLAINTEXT_FILE] [-r RECEIVERS_FILE] [-t SLEEP_TIME] [-l] [-x]`

### Command Line Args

*Required arguments:*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-e EMAIL`           Email to send from.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-s PASSWORD`        Password for email account.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-j SUBJECT`         Email subject.

*Optional Arguments*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-p PLAINTEXT_FILE`  Text file with email plaintext content. Defaults to `plaintext.txt`.
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-r RECEIVERS_FILE`  CSV file where the receivers are located. Defaults to `emails.csv`.
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-t SLEEP_TIME`      Sleep time between recipients, in seconds. Defaults to 2 seconds.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-h`, `--help`       show this help message and exit.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-l`                 Include this option to log the successful sends to a text file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`-x`                 Disable test mode. See 'EmailMessage.py' for details.

# Dependencies
None...... for now.......
