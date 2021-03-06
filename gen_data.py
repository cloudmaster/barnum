#!/usr/bin/env python
"""
Barnum is a python-based test data generator.
Copyright (C) 2007 Chris Moffitt
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import cPickle as pickle
import random
import string
import gencc
import calendar
import datetime
import genpw
import os
import sys

# In Windows, sometimes __file__ is undefined
try:
    DIRNAME = os.path.dirname(__file__)
except NameError:
    DIRNAME = os.path.dirname(sys.argv[0])

gender_options=('Male', 'Female')
company_type = ('LawFirm', 'Generic', 'Short')
card_types = ('mastercard', 'visa', 'discover', 'amex')

try:
    source_file = open(os.path.join(DIRNAME, "source-data.pkl"),'rb')
except:
    print >>sys.stderr, "Error: Data archive source-data.pkl doesn't exist. Run convert_data.py first."
    sys.exit(1)
all_zips = pickle.load(source_file)
state_area_codes = pickle.load(source_file)
last_names = pickle.load(source_file)
male_first_names = pickle.load(source_file)
female_first_names = pickle.load(source_file)
street_names = pickle.load(source_file)
street_types = pickle.load(source_file)
latin_words = pickle.load(source_file)
email_domains = pickle.load(source_file)
job_titles = pickle.load(source_file)
company_names = pickle.load(source_file)
company_types = pickle.load(source_file)
noun_list = pickle.load(source_file)

source_file.close()

def create_name(full_name=True, gender=None):
    if not gender:
        gender = random.choice(gender_options)
    if gender == "Male":
        first_name = random.choice(male_first_names)
    else:
        first_name = random.choice(female_first_names)
    if full_name:
        return(first_name, random.choice(last_names))
    else:
        return(first_name)

def create_job_title():
    return random.choice(job_titles)

def create_phone(zip_code=None):
    if not zip_code:
        zip_code = random.choice(all_zips.keys())
    area_code = random.choice(state_area_codes[all_zips[zip_code][1]])
    output = "(%s)%s-%s" % (area_code, random.randint(111, 999), random.randint(1111, 9999))
    return(output)

def create_street():
    flavour = "german"
    number = random.randint(1, 9999)
    name = string.capwords(random.choice(street_names))
    if flavour == "german":
        street_type = random.choice(street_types)
        return("%s%s %s" % (name, street_type, number))
    else:
        street_type = string.capwords(random.choice(street_types))
        return("%s %s %s" % (number, name, street_type))

def create_city_state_zip(zip_code=None):
    if not zip_code:
        zip_code = random.choice(all_zips.keys())
    return(zip_code, all_zips[zip_code][0], all_zips[zip_code][1])

def create_sentence(min=4, max=15):
    sentence = []
    sentence.append(string.capitalize(random.choice(latin_words)))
    for word in range(1, random.randint(min, max - 1)):
        sentence.append(random.choice(latin_words))
    return " ".join(sentence) + "."

def create_paragraphs(num=1, min_sentences=4, max_sentences=7):
    paragraphs = []
    for para in range(0, num):
        for sentence in range(1, random.randint(min_sentences, max_sentences)):
            paragraphs.append(create_sentence()+" ")
        paragraphs.append("\n\n")
    return "".join(paragraphs)

def create_nouns(max=2):
    """
    Return a string of random nouns up to max number
    """
    nouns = []
    for noun in range(0, max):
        nouns.append(random.choice(noun_list))
    return " ".join(nouns)

def create_date(numeric=True, past=False, max_years_future=10, max_years_past=10):
    """
    Create a random valid date
    If past, then dates can be in the past
    If into the future, then no more than max_years into the future
    If it's not, then it can't be any older than max_years_past
    """
    if past:
        start = datetime.datetime.today() - datetime.timedelta(days=max_years_past * 365)
        #Anywhere between 1980 and today plus max_ears
        num_days = (max_years_future * 365) + start.day
    else:
        start = datetime.datetime.today()
        num_days = max_years_future * 365

    random_days = random.randint(1, num_days)
    random_date = start + datetime.timedelta(days=random_days)
    return(random_date)

def create_birthday(min_age=18, max_age=80):
    """
    Create a random birthday fomr someone between the ages of min_age and max_age
    """
    age = random.randint(min_age, max_age)
    start = datetime.date.today() - datetime.timedelta(days=random.randint(0, 365))
    return start - datetime.timedelta(days=age*365)

def create_email(tld=None, name=None):
    if not name:
        name = create_name()
    if not tld:
        tld = random.choice(email_domains)
    user_choices = ["%s.%s" % (name[0], name[1]), "%s" % name[0], "%s.%s" % (name[0][:1], name[1])]
    domain = random.choice(latin_words) + random.choice(latin_words)
    return ("%s@%s.%s" % (random.choice(user_choices), domain, tld))

def create_company_name(biz_type=None):
    name = []
    if not biz_type:
        biz_type = random.choice(company_type)
    if biz_type == "LawFirm":
        name.append(random.choice(last_names) + ", " + random.choice(last_names) + " & " +
                    random.choice(last_names))
        name.append('LLP')
    else:
        for i in range(1,random.randint(2, 4)):
            rand_name = random.choice(company_names)
            if rand_name not in name:
                name.append(rand_name)
        if biz_type == 'Generic':
            name.append(random.choice(company_types))
        elif len(name) < 3:
            name.append(random.choice(company_names))
    return " ".join(name)

def cc_number(card_type=None, length=None, num=1):
    if not card_type:
        card_type = random.choice(card_types)
    prefix_list = "gencc." + card_type + "PrefixList"
    length = 16
    return(card_type, gencc.credit_card_number(eval(prefix_list), length, num))

if __name__ == "__main__":
    first, last = create_name()
    add = create_street()
    zip, city, state = create_city_state_zip()
    phone = create_phone(zip)
    print first, last
    print add
    print "%s %s, %s" % (city, state, zip)
    print phone
    print create_sentence(), "\n"
    print create_paragraphs(num=3)
    cc = cc_number()
    print cc
    expiry = create_date(max_years_future=3)
    print expiry.strftime("%m/%y")
    print create_email(name=(first,last))
    print "Password: ", genpw.nicepass()
    print create_company_name()
    print create_job_title()
    print "Born on %s" % create_birthday().strftime("%m/%d/%Y")


