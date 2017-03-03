#!/usr/bin/python


'''
shamelessly borrowed from https://docs.python.org/2/library/email-examples.html
'''

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendNotice(main_list,history):
	# me == my email address
	# you == recipient's email address
	me = "jchytrowski@aurifero.us"
	you = "jchytrowski@gmail.com"

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Link"
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).

	newHTML="""\
        <html>
          <head></head>
          <body>"""
	

	for jobset in main_list:
                for listing in jobset:
                        title=jobset[listing][0]
                        url=jobset[listing][1]
                        location=jobset[listing][2]
                        snippet=jobset[listing][3]
                        company=jobset[listing][4]

                        if history.query_archive(url):
                                continue
                        else:
                                history.push_archive(url)
				
				entry='<p><a href="%s">%s</a><br> %s -- %s<br>%s</p>'					% (url, title, company, location, snippet)
				newHTML="".join([newHTML, entry])
	tail='</body></html>'
	newHTML="".join([newHTML, tail])


                        #print '%s \n%s  -- %s\n%s\n%s\n\n' % (title, company, location, snippet, url)


	text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>Hi!<br>
	       How are you?<br>
	       Here is the <a href="https://www.python.org">link</a> you wanted.
	    </p>
	  </body>
	</html>
	"""

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(newHTML, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('localhost')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(me, you, msg.as_string())
	s.quit()

