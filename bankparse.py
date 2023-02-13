from itertools import permutations
from datetime import datetime
import random
from random import randint
import csv
import os
import time
import sys

customers = []
transactions = []

firstnames = r"firstNames.txt"
lastnames = r"lastNames.txt"

currentType = ""

Digits = '0123456789'


def to_int(p):
    return int(''.join(p))


def contains_123(p):
    return set(p) > set('123')


T = [to_int(p) for p in permutations(Digits, 6)
     if p[0] != '0' and contains_123(p)]

fpath = os.getcwd()

class Customer:
    def __init__(self, fname, lname, accountType, accountNumber):
        self.firstName = fname
        self.lastName = lname
        self.accountType = accountType
        self.accountNumber = accountNumber
        self.flaggedTransactions = 0

    def get_firstName(self):
        return self.firstName

    def get_lastName(self):
        return self.lastName

    def get_fullName(self):
        fullname = "{} {}".format(self.firstName, self.lastName)
        # fStrFname = f"{self.firstName}, {self.lastName}"
        return fullname

    def get_accountType(self):
        return self.accountType

    def get_accountNumber(self):
        return self.accountNumber
    
    def get_flaggedTransactions(self):
        return self.flaggedTransactions


class Transaction:
    def __init__(self, senderFullName, senderAccountNumber, sentAmount, recFullName, recAccountNumber, flaggedTransaction, flaggedComment, timestamp):
        self.senderFullName = senderFullName
        self.senderAccountNumber = senderAccountNumber
        self.sentAmount = sentAmount
        self.recipientFullName = recFullName
        self.recipientAccountNumber = recAccountNumber
        self.timestamp = timestamp
        self.flagged = flaggedTransaction
        self.flaggedComment = flaggedComment

    def flaggedSnippet(self):
        if self.flagged == True:
            return "Passed parser tests"
        else:
            return "Didn't pass parser tests"

    def get_senderName(self):
        return self.senderFullName

    def get_senderAccount(self):
        return self.senderAccountNumber

    def get_sentAmount(self):
        return self.sentAmount

    def get_recipientName(self):
        return self.recipientFullName

    def get_recipientAccount(self):
        return self.recipientAccountNumber

    def get_flagged(self):
        return self.flagged

    def get_flaggedComment(self):
        return self.flaggedComment

    def get_timestamp(self):
        return self.timestamp

    def get_Transaction(self):
        return self.senderFullName.strip() + "with account number " + str(self.senderAccountNumber) + " sent NGN" + str(self.sentAmount) + " to " + self.recipientFullName.strip() + " with account number " + str(self.recipientAccountNumber) + " at " + self.timestamp.strip() + ". This transaction " + self.flaggedSnippet()


def customersGenerator():
    print("Randomly generating 50 new customers...")
    # Generates 50 random customers
    i = 0
    while i < 50:
        firstname = random.choice(open(firstnames).readlines())
        lastname = random.choice(open(lastnames).readlines())

        type = random.randrange(0, 2)
        if type == 1:
            currentType = "Savings"
            accountType = "Savings"
        else:
            currentType = "Current"
            accountType = "Current"

        beginningFigure = 0
        if currentType == "Savings":
            beginningFigure = 2333
        elif currentType == "Current":
            beginningFigure = 2444

        accountNumber = str(beginningFigure) + str(T[i])
        accountNumber = int(accountNumber)

        customer = Customer(firstname.strip(), lastname.strip(), accountType.strip(), accountNumber)
        customers.append(customer)
        print(firstname.strip(), lastname.strip(),  accountType.strip(),  str(accountNumber))
        time.sleep(0.5)

        i += 1
    print("\nCustomers generated successfully!\n")
    time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


def transactionGenerator():
    # Generates 20 dummy transactions
    print("Generating 20 dummy transactions...")
    time.sleep(1)
    flaggedParametersMSG = ["Non-correlation between transaction amount and customer. ", "Suspected evasion of mandatory tracking procedures. ", "Suspicious settling of royalty fees to client account in foreing currency. ", "Many transactions originating from similar IP addresses. ", "Suspicious loan repayment for purported purchase of elite real estate. "]

    cleanParameterMSG = "This transaction passed all tests."


    # flaggedAccounts = [2, 3, 8, 18, 20, 33, 41, 48]
    flaggedAmounts = [999999, 9999999]
    limitSavings = 5000000
    limitCurrent = 8500000
    count = 0
    if len(customers) > 1:
        while count < 20:
            timestamp = datetime.now()

            customerindex = random.randrange(1, len(customers))
            lastindex = len(customers) - 1
            fromCustomer = customers[customerindex]
            nextindex = 0
            if customerindex == lastindex:
                nextindex = 0
            else:
                nextindex = customerindex + 1
            
            toCustomer = customers[nextindex]

            flagIndex = random.randrange(1, len(flaggedParametersMSG))
            flagIndex = flagIndex - 1

            transactionAmount = randint(3000, 9999999)

            flaggedTransaction = random.choice([True, False])
            if flaggedTransaction == True:
                # Entire commented area unnecessary...just added it.
                # if flagIndex == 0:
                #     #Define parameter 1 scenario (more than lowest transaction amount):
                #     pass
                # elif flagIndex == 1:
                #     #Define parameter 2 scenario (flagged amounts):
                #     pass
                # elif flagIndex == 2:
                #     #Define parameter 3 scenario (no idea what this refers to...just flag with comment):
                #     pass
                # elif flagIndex == 3:
                #     #Define parameter 4 scenario (can't do this since app doesn't take in IPs...flag with comment):
                #     pass
                # elif flagIndex == 4:
                #     #Define parameter 5 scenario (no idea what this is...just flag with comment):
                #     pass
                #Would include a flagging for accounts that have flagged trasactions but nah...new parameters doesn't make provision.
                transaction = Transaction(fromCustomer.get_fullName().strip(), fromCustomer.get_accountNumber(), transactionAmount, toCustomer.get_fullName().strip(), toCustomer.get_accountNumber(), flaggedTransaction, flaggedParametersMSG[flagIndex].strip(), str(timestamp).strip())
                transactions.append(transaction)
            else:
                transaction = Transaction(fromCustomer.get_fullName().strip(), fromCustomer.get_accountNumber(), transactionAmount, toCustomer.get_fullName().strip(), toCustomer.get_accountNumber(), flaggedTransaction, cleanParameterMSG.strip(), str(timestamp).strip())
                transactions.append(transaction)
            # transaction.flaggedTransactions = flaggedCount
            print(transaction.get_Transaction())

            # I can extend this so once an account commits an infraction, they get added to the database of flagged accounts for review.

            count = count + 1
            time.sleep(0.5)
        print("Dummy transactions generated successfully!\n")
        time.sleep(1)
    else:
        time.sleep(3)
        print("Please generate some customers before transactions. There are currently no customers in database.")
        time.sleep(2)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()

customersFile = fpath + "\customers.csv"
transactionsFile = fpath + "\\transactions.csv"

def saveCustomers():
    header = ['First Name', 'Last Name', 'Account Number', 'Account Type']

    with open(customersFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        if len(customers) > 0:
            for customer in customers:
                data = [customer.get_firstName(), customer.get_lastName(), customer.get_accountNumber(), customer.get_accountType()]
                writer.writerow(data)
                time.sleep(0.3)
        else:
            print("There are 0 customers available to store.")


def saveTransactions():
    header = ['Sender Full Name', 'Sender Account Number', 'Amount', 'Recipient Full Name', 'Recipient Account Number', 'Flagged?', 'Flagged Comments', 'Timestamp']
    
    with open(transactionsFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        if len(transactions) > 0:
            for transaction in transactions:
                # print(transaction.get_senderName(), transaction.get_senderAccount(), transaction.get_sentAmount(), transaction.get_recipientName(), transaction.get_recipientAccount(), str(transaction.get_flagged()), transaction.get_flaggedComment(), str(transaction.get_timestamp()))
                data = [transaction.get_senderName(), transaction.get_senderAccount(), transaction.get_sentAmount(), transaction.get_recipientName(), transaction.get_recipientAccount(), str(transaction.get_flagged()), transaction.get_flaggedComment(), str(transaction.get_timestamp())]
                writer.writerow(data)
                time.sleep(0.3)
        else:
            print("There are 0 transactions currently available to store.")


def numberofCustomers():
    return len(customers)


def nosTransactions():
    return len(transactions)


def nosCleanTransactions():
    cleantransactions = 0
    for transaction in transactions:
        if transaction.get_flagged() == False:
            cleantransactions = cleantransactions + 1
    return cleantransactions


def nosFlaggedTransactions():
    flaggedtransactions = 0
    for transaction in transactions:
        if transaction.get_flagged() == True:
            flaggedtransactions = flaggedtransactions + 1
    return flaggedtransactions


def menuControls(menu):
    if menu == 1:
        customersGenerator()
    elif menu == 2:
        transactionGenerator()
    elif menu == 3:
        print("Saving customers...")
        saveCustomers()
        print("Customers saved successfully!\n")
        time.sleep(1)
        input("Press ENTER to return to main menu")
        time.sleep(1)
        mainMenu()
    elif menu == 4:
        print("Saving transactions...")
        saveTransactions()
        print("Transactions saved successfully!\n")
        time.sleep(1)
        input("Press ENTER to return to main menu")
        time.sleep(1)
        mainMenu()
    elif menu == 5:
        print("Calculating...")
        time.sleep(2)
        print("Calculation complete.")
        time.sleep(0.5)
        print("\nThere are " + str(numberofCustomers()) + " customers in the database!\n")
        time.sleep(2)
    elif menu == 6:
        print("Calculating...")
        time.sleep(2)
        print("Calculation complete.")
        time.sleep(0.5)
        print("\nThere are " + str(nosTransactions()) + " transactions in the database!\n")
        time.sleep(2)
    elif menu == 7:
        print("Calculating...")
        time.sleep(2)
        print("Calculation complete.")
        time.sleep(0.5)
        print("\nThere are " + str(nosCleanTransactions()) + " clean transactions in the database!\n")
        time.sleep(2)
    elif menu == 8:
        print("Calculating...")
        time.sleep(2)
        print("Calculation complete.")
        time.sleep(0.5)
        print("\nThere are " + str(nosFlaggedTransactions()) + " flagged transactions in the database!\n")
        time.sleep(2)
    elif menu == 9:
        count = len(transactions)
        print(str(count) + " transactions to be deleted")
        time.sleep(0.3)
        print("Deleting...")
        while count > 0:
            del transactions[0]
            count  = count - 1
        print("Transactions deleted.")
        saveTransactions()
    elif menu == 10:
        count = len(customers)
        print(str(count) + " customers to be deleted.")
        time.sleep(0.3)
        print("Deleting...")
        while count > 0:
            del customers[0]
            count  = count - 1
            time.sleep(0.3)
        print("Customers deleted.")
        saveCustomers()
    elif menu == 00:
        exitApp()
    else:
        print("Invalid entry. Please enter a number within the range of available menu items.")
        print("Remember to make sure you enter a number and nothing else.")
        time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


def clearScreen():
    os.system('cls')


def exitApp():
    sys.exit()

def loadDataOnStart():
    print("Loading customers...")
    with open(customersFile, 'r', encoding='UTF8', newline='') as customrs:
        customrsData = csv.reader(customrs, delimiter=',')
        line_c = 0
        for row in customrsData:
            # print("loading customer " + str(line_c + 1))
            # print(row)
            customer = Customer(row[0].strip(), row[1].strip(), row[2], row[3].strip())
            print(row[0].strip(), row[1].strip(), str(row[2]), row[3].strip())
            customers.append(customer)
            line_c = line_c + 1
            # time.sleep(0.3)
        # print(customrsData)
        del customers[0]
        # print(customers[0].get_fullName())
        time.sleep(2)
        if line_c > 1:
            print("Loaded " + str(len(customers)) + " customers successfully!\n")
        else:
            print("Customers file is empty.")
        time.sleep(3)
    
    print("Loading transactions...")
    with open(transactionsFile, 'r', encoding='UTF8', newline='') as transctns:
        transctnsData = csv.reader(transctns, delimiter=',')
        linec = 0
        flaggedData = False
        for row in transctnsData:
            if row[5] == "True":
                # print("Testing flag")
                flaggedData = True
            transactn = Transaction(row[0].strip(), row[1], row[2], row[3].strip(), row[4], flaggedData, row[6].strip(), row[7].strip())
            # print(transactn)
            print(row[0].strip(), row[1], row[2], row[3].strip(), row[4], flaggedData, row[6].strip(), row[7].strip())
            transactions.append(transactn)
            linec = linec + 1
        del transactions[0]
        time.sleep(2)
        if linec > 1:
            print("Loaded " + str(len(transactions)) + " transactions successfully!\n")
        else:
            print("Transactions file is empty.")
        time.sleep(3)

def mainMenu():
    clearScreen()
    welcomeMsg = """

Welcome to the Bank Transactions Parser!
Simply enter the number of the Menu you would like to access to proceed.

------ RUN PROGRAM ------

1: Generate New customers
2: Generate transactions
3: Save Customer data
4: Save transactions data

---- GENERATE REPORTS ----

5: Number of customers in database
6: Number of transactions in database
7: Number of clean transactions
8: Number of flagged transactions

------ EXIT PROGRAM ------

9: Delete transactions data
10: Delete customers' data
00: EXIT

"""
    print(welcomeMsg)
    menu = int(input("Enter menu item # to proceed: "))
    menuControls(menu)


print("\nInitializing application...")
time.sleep(3)
loadDataOnStart()

mainMenu()