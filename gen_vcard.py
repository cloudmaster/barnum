#!/usr/bin/env python

import sys, random
import gen_data

try:
	count = int(sys.argv[1])
except:
	count = 1

class Vcard:
	def __init__(self):
		self.name = None
		self.adr = None
		self.street = None
		self.company = None
		self.birthday = None
		self.email = None

	def printout(self):
		vcard = """BEGIN:VCARD
VERSION:3.0
FN:%s
N:%s;%s;;;
ORG:%s
BDAY:%s
EMAIL;TYPE=WORK:%s
X-JABBER;TYPE=HOME:%s
ADR;TYPE=HOME:;;%s;%s;%s;%s;USA
END:VCARD"""

		s = vcard % (' '.join(vc.name),
			vc.name[1], vc.name[0],
			vc.company, vc.birthday,
			vc.email, vc.email, vc.street,
			vc.adr[1], vc.adr[2], vc.adr[0])
		return s

for i in range(0, count):
	vc = Vcard()
	vc.name = gen_data.create_name()
	vc.adr = gen_data.create_city_state_zip()
	vc.company = gen_data.create_company_name()
	vc.birthday = gen_data.create_birthday()
	vc.email = gen_data.create_email(name=vc.name)
	vc.street = gen_data.create_street()
	print vc.printout()
