#!/usr/bin/python
"""
gencc: A simple program to generate credit card numbers that pass the MOD 10 check
(Luhn formula).
Useful for testing e-commerce sites during development.

Copyright 2003 Graham King

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import random
import sys
import copy

visaPrefixList = [['4', '5', '3', '9'],
                  ['4', '5', '5', '6'],
                  ['4', '9', '1', '6'],
                  ['4', '5', '3', '2'],
                  ['4', '9', '2', '9'],
                  ['4', '0', '2', '4', '0', '0', '7', '1'],
                  ['4', '4', '8', '6'],
                  ['4', '7', '1', '6'],
                  ['4']]

mastercardPrefixList = [['5', '1'],
                        ['5', '2'],
                        ['5', '3'],
                        ['5', '4'],
                        ['5', '5']]

amexPrefixList = [['3', '4'],
                    ['3', '7']]

discoverPrefixList = [['6', '0', '1', '1']]

dinersPrefixList = [['3', '0', '0'],
                    ['3', '0', '1'],
                    ['3', '0', '2'],
                    ['3', '0', '3'],
                    ['3', '6'],
                    ['3', '8']]

enRoutePrefixList = [['2', '0', '1', '4'],
                     ['2', '1', '4', '9']]

jcbPrefixList16 = [['3', '0', '8', '8'],
                   ['3', '0', '9', '6'],
                   ['3', '1', '1', '2'],
                   ['3', '1', '5', '8'],
                   ['3', '3', '3', '7'],
                   ['3', '5', '2', '8']]

jcbPrefixList15 = [['2', '1', '0', '0'],
                   ['1', '8', '0', '0']]

voyagerPrefixList = [['8', '6', '9', '9']]

"""
'prefix' is the start of the CC number as a string, any number of digits.
'length' is the length of the CC number to generate. Typically 13 or 16
"""
def completed_number(prefix, length):
    ccnumber = prefix

    # generate digits
    while len(ccnumber) < (length - 1):
        digit = random.choice(['0',  '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ccnumber.append(digit)

    # Calculate sum
    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:
        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])
        pos += 2

    # Calculate check digit
    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append( str(checkdigit) )

    return ''.join(ccnumber)

def credit_card_number(prefixList, length, howMany):
    result = []

    for i in range(howMany):
        ccnumber = copy.copy(random.choice(prefixList))
        result.append(completed_number(ccnumber, length))

    return result

def output(title, numbers):

    result = []
    result.append(title)
    result.append('-' * len(title))
    result.append('\n'.join(numbers))
    result.append('')

    return '\n'.join(result)

#
# Main
#
if __name__ == "__main__":
    creditcards = {
        "Mastercard" : (mastercardPrefixList, 16),
        "VISA 16 digit" : (visaPrefixList, 16),
        "VISA 13 digit" : (visaPrefixList, 13),
        "American Express" : (amexPrefixList, 15),
        "Discover" : (discoverPrefixList, 16),
        "Diners Club / Carte Blanche" : (dinersPrefixList, 14),
        "enRoute" : (enRoutePrefixList, 15),
        "JCB 15 digit" : (jcbPrefixList15, 15),
        "JCB 16 digit" : (jcbPrefixList16, 16),
        "Voyager" : (voyagerPrefixList, 15)
    }

    if len(sys.argv) != 2:
        print >>sys.stderr, "Syntax: gencc list|all|random|<card>"
        sys.exit(1)

    card = sys.argv[1]
    if sys.argv[1] == "random":
        card = creditcards.keys()[random.randint(0, len(creditcards.keys()) - 1)]
    elif sys.argv[1] == "list":
        for card in creditcards.keys():
            print card
        sys.exit(0)
    elif sys.argv[1] == "all":
        for card in creditcards.keys():
            cardparams = creditcards[card]
            number = credit_card_number(cardparams[0], cardparams[1], random.randint(1, 3))
            print output(card, number)
        sys.exit(0)

    cardparams = creditcards[card]
    number = credit_card_number(cardparams[0], cardparams[1], 1)
    print number[0]
