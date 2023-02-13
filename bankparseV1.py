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


class Customer:
    def __init__(self, fname, lname, accountType, accountNumber):
        self.firstName = fname
        self.lastName = lname
        self.accountType = accountType
        self.accountNumber = accountNumber

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
        self.flaggedTransactions = 0

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

    def get_flaggedTransactions(self):
        return self.flaggedTransactions

    def get_Transaction(self):
        return self.senderFullName.strip() + "with account number " + str(self.senderAccountNumber) + " sent NGN" + str(self.sentAmount) + " to " + self.recipientFullName.strip() + " with account number " + str(self.recipientAccountNumber) + " at " + self.timestamp.strip() + ". This transaction " + self.flaggedSnippet()
        # + ". User has " + str(self.flaggedTransactions()) + " amount of flagged transactions."


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
        print(firstname.strip(), lastname.strip(),  accountType.strip(),  str(accountNumber),  "\n")
        time.sleep(0.5)

        i += 1
    print("Customers generated successfully!\n")
    time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


def transactionGenerator():
    print("Generating 20 dummy transactions...")
    time.sleep(1)
    parameters = ["Flagged Account", "Suspicious Amount", "Suspicious Activity", "Limit Exceedeo9d For Type"]
    # Generate 20 transactions
    # Sender Full Name', 'Sender Account Number', 'Amount', 'Recipient Full Name', 'Recipient Account Number', 'Flagged?', Timestamp

    # Flagged Account::: List of flagged accounts
    # Suspicious Amount::: Range of suspicious amounts
    # Suspicious Activity::: Sending at least 5 transactions at a go
    # Limit Exceeded for type::: Limits for saving or current accounts

    # IP addresses --- will require a very large amount of data which will take more time and use up more space. Don't know what the scenario for use is and if it's like a school project then there's usually a size limit for the program

    flaggedAccounts = [2, 3, 8, 18, 20, 33, 41, 48]
    flaggedAmounts = [999999, 9999999]
    limitSavings = 5000000
    limitCurrent = 8500000
    count = 0
    if len(customers) > 1:
        while count < 20:
            timestamp = datetime.now()

            flaggedSender = False
            flaggedRecipient = False
            susAmount = False
            susActivity = False
            limitExceeded = False

            flaggedTransaction = False
            flaggedComment = ""

            flaggedCount = 0

            limitExceededMSG = "Sending limit exceeded. "
            flaggedAmountsMSG = "Flagged amount. "
            flaggedAccountsMSG = "Flagged account. "

            customerindex = random.randrange(1, len(customers))
            lastindex = len(customers) - 1
            fromCustomer = customers[customerindex]
            
            nextindex = 0
            if customerindex == lastindex:
                nextindex = 0
            else:
                nextindex = customerindex + 1
            
            toCustomer = customers[nextindex]

            # Flagged accounts, sender or recipient
            for account in flaggedAccounts:
                if account == customerindex:
                    flaggedSender = True
                    flaggedTransaction = True
                    flaggedComment = flaggedComment + flaggedAccountsMSG
                if account == toCustomer:
                    flaggedRecipient = True
                    flaggedTransaction = True
                    flaggedComment = flaggedComment + flaggedAccountsMSG

            transactionAmount = randint(3000, 9999999)

            # Flagged amounts
            for amount in flaggedAmounts:
                if amount == transactionAmount:
                    susAmount = True
                    flaggedTransaction = True
                    flaggedComment = flaggedComment + flaggedAmountsMSG

            # Current/Savings limits
            if fromCustomer.get_accountType() == "Savings":
                if transactionAmount >= limitSavings:
                    limitExceeded = True
                    flaggedTransaction = True
                    flaggedComment = flaggedComment + limitExceededMSG
            if fromCustomer.get_accountType() == "Current":
                if transactionAmount >= limitCurrent:
                    limitExceeded = True
                    flaggedTransaction = True
                    flaggedComment = flaggedComment + limitExceededMSG
            if flaggedTransaction == True:
                flaggedCount = flaggedCount + 1

            print(fromCustomer.get_fullName().strip(), fromCustomer.get_accountNumber(), transactionAmount, toCustomer.get_fullName().strip(), toCustomer.get_accountNumber(), flaggedTransaction, flaggedComment.strip(), str(timestamp).strip())

            transaction = Transaction(fromCustomer.get_fullName().strip(), fromCustomer.get_accountNumber(), transactionAmount, toCustomer.get_fullName().strip(), toCustomer.get_accountNumber(), flaggedTransaction, flaggedComment.strip(), str(timestamp).strip())
            transactions.append(transaction)
            # transaction.flaggedTransactions = flaggedCount
            # print(transaction.get_Transaction())

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


# def transactionParser():
#     pass


def loadCustomers():
    print("Loading customers...")
    with open('/Workspace/bankParse/customers.csv', 'r', encoding='UTF8', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        if sum(1 for row in reader) > 1:
            line_count = 0
            for row in reader:
                if line_count == 0:
                    continue
                else:
                    customer = Customer(row[0].strip(), row[1].strip(), row[2].strip(), row[3])
                    customers.append(customer)
                line_count += 1
                time.sleep(0.3)
        else:
            print("Customers file is empty.")
    print("Customers loaded successfully!\n")
    time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


def loadTransactions():
    print("Loading transactions...")
    with open('/Workspace/bankParse/transactions.csv', 'r', encoding='UTF8', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        if sum(1 for row in reader) > 1:
            line_count = 0
            flaggedData = False
            for row in reader:
                if line_count == 0:
                    continue
                else:
                    if row[5] == "True":
                        flaggedData = True

                    transaction = Transaction(row[0].strip(), row[1].strip(), row[2].strip(), row[3])
                    transactions.append(transaction)
                    data = [row[0].strip(), row[1], row[2], row[3].strip(), row[4], flaggedData, row[6].strip(), row[7].strip()]
                    transactions.append(transaction)
                line_count += 1
                time.sleep(0.3)
            else:
                print("Transactions file is empty.")
    print("Transactions loaded successfully!\n")
    time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


def saveCustomers():
    print("Saving customers...")
    header = ['First Name', 'Last Name', 'Account Number', 'Account Type']

    if len(customers) > 0:
        with open('/Workspace/bankParse/customers.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for customer in customers:
                data = [customer.get_firstName(), customer.get_lastName(), customer.get_accountNumber(), customer.get_accountType()]
                writer.writerow(data)
                time.sleep(0.3)
    else:
        print("There are 0 customers available to store.")
    print("Customers saved successfully!\n")
    time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


def saveTransactions():
    print("Saving transactions...")
    header = ['Sender Full Name', 'Sender Account Number', 'Amount', 'Recipient Full Name', 'Recipient Account Number', 'Flagged?', 'Flagged Comments', 'Flagged Transactions', 'Timestamp']

    if len(transactions) > 0:
        with open('/Workspace/bankParse/transactions.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for transaction in transactions:
                # print(transaction.get_senderName(), transaction.get_senderAccount(), transaction.get_sentAmount(), transaction.get_recipientName(), transaction.get_recipientAccount(), str(transaction.get_flagged()), transaction.get_flaggedComment(), str(transaction.get_timestamp()))
                data = [transaction.get_senderName(), transaction.get_senderAccount(), transaction.get_sentAmount(), transaction.get_recipientName(), transaction.get_recipientAccount(), str(transaction.get_flagged()), transaction.get_flaggedComment(), transaction.get_flaggedTransactions(), str(transaction.get_timestamp())]
                writer.writerow(data)
                time.sleep(0.3)
    else:
        print("There are 0 transactions currently available to store.")

    print("Transactions saved successfully!\n")
    time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


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
        saveCustomers()
    elif menu == 4:
        saveTransactions()
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
        while count > 0:
            del transactions[0]
        saveTransactions()
    elif menu == 10:
        count = len(customers)
        while count > 0:
            del customers[0]
        saveCustomers()
    elif menu == 00:
        exitApp()
    else:
        print("Invalid entry. Please enter a number within the range of available menu items.")
        print("Remember to make sure you enter a number and nothing else.")
        time.sleep(1)
    # try:
    #     match menu:
    #         case 1:
    #             customersGenerator()
    #         case 2:
    #             transactionGenerator()
    #         case 3:
    #             saveCustomers()
    #         case 4:
    #             saveTransactions()
    #         case 5:
                
    #         case 6:
                
    #         case 7:
    #             print("Calculating...")
    #             time.sleep(2)
    #             print("Calculation complete.")
    #             time.sleep(0.5)
    #             print("\nThere are " + str(nosCleanTransactions()) + " clean transactions in the database!\n")
    #             time.sleep(2)
    #         case 8:
    #             print("Calculating...")
    #             time.sleep(2)
    #             print("Calculation complete.")
    #             time.sleep(0.5)
    #             print("\nThere are " + str(nosFlaggedTransactions()) + " flagged transactions in the database!\n")
    #             time.sleep(2)
    #         case 9:
    #             print("Not yet active")
    #         case 10:
    #             print("Not yet active")
    #         case 00:
    #             exitApp()

    # except:
    #     print("Invalid entry. Please enter a number within the range of available menu items.")
    #     print("Remember to make sure you enter a number and nothing else.")
    #     time.sleep(1)
    input("Press ENTER to return to main menu")
    time.sleep(1)
    mainMenu()


def clearScreen():
    os.system('cls')


def exitApp():
    sys.exit()

def loadDataOnStart():
    print("Loading customers...")
    with open('customers.csv', 'r', encoding='UTF8', newline='') as customrs:
        customrsData = csv.reader(customrs, delimiter=',')
        line_c = 0
        for row in customrsData:
            # print("loading customer " + str(line_c + 1))
            # print(row)
            customer = Customer(row[0].strip(), row[1].strip(), row[2], row[3].strip())
            # print(row[0].strip(), row[1].strip(), str(row[2]), row[3].strip())
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
    with open('transactions.csv', 'r', encoding='UTF8', newline='') as transctns:
        transctnsData = csv.reader(transctns, delimiter=',')
        linec = 0
        flaggedData = False
        for row in transctnsData:
            if row[5] == "True":
                print("Testing flag")
                flaggedData = True
            transactn = Transaction(row[0].strip(), row[1], row[2], row[3].strip(), row[4], flaggedData, row[6].strip(), row[7].strip())
            print(transactn)
            transactions.append(transactn)
            linec = linec + 1
        del transactions[0]
        time.sleep(2)
        if linec > 1:
            print("Loaded " + str(len(transactions)) + " transactions successfully!\n")
        else:
            print("Customers file is empty.")
        time.sleep(3)


    # print("Loading transactions...")
    # with open('/Workspace/bankParse/transactions.csv', 'r', encoding='UTF8', newline='') as transactns:
    #     readfile = csv.reader(transactns, delimiter=',')
    #     if sum(1 for transactn in readfile) > 1:
    #         lineCount = 0
    #         flaggedData = False
    #         for row in readfile:
    #             if lineCount == 0:
    #                 continue
    #             else:
    #                 if row[5] == "True":
    #                     flaggedData = True
    #                 print("loading...")
    #                 transaction = Transaction(row[0].strip(), row[1].strip(), row[2].strip(), row[3])
    #                 transactions.append(transaction)
    #                 # data = [row[0].strip(), row[1], row[2], row[3].strip(), row[4], flaggedData, row[6].strip(), row[7].strip()]
    #                 # transactions.append(transaction)
    #             line_count += 1
    #             time.sleep(0.3)
    #             time.sleep(2)
    #             print("Transactions loaded successfully!\n")
    #     else:
    #         print("Transactions file is empty.")
    #         time.sleep(3)

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

# transactionGenerator()
mainMenu()