'''
This program is a demonstration of some concepts from my discrete math class.
Not everything is necessarily the most efficient, in fact, I will often take a
longer route to show the by-hand method as a restriction for myself.
'''

#global constants (Main Menu)
DEC_TO_BASE_N = "1"
BASE_N_TO_DEC = "2"
SIGN_BIN = "3"
HEX_TO_RGB = "4"
REPRINT_MENU = "R"
EXIT_FUNCTION = "E"
OPTION_LIST = ["1","2","3","4","R","E"]
BINARY_BASE = 2
HEX_BASE = 16
BYTE_LENGTH = 8

import os


def main():
    #exit function loop control variable
    exitFunction = False
    menuCount = 0
    promptAgain = True

    
    #while loop checks for ending the function
    while (not exitFunction):
        userInput = ""
        validChoice = False

        #print the menu for the first loop iteration
        if menuCount == 0:
            printMenu()

        #check if user would like to continue after the first loop iteration
        else:

            #only ask to select another option if they don't reprint menu (formats better)
            if promptAgain:
                #validation loop for choosing to continue
                while (not validChoice):

                    print("\nWould you like to select another option?")
                    menuChoice = input("Enter 'yes' or 'no': ")

                    #reprint menu if user chooses 'yes'
                    if menuChoice.upper() == "YES":
                        validChoice = True

                        print()
                        printMenu()

                    #exit function if user chooses 'no'
                    elif menuChoice.upper() == "NO":
                        validChoice = True

                        userInput = EXIT_FUNCTION
                        exitFunction = True

                    else:
                        print("\n***Error: Please enter either 'yes' or 'no'***")
                        validChoice = False
            
        promptAgain = True
        menuCount += 1

        if userInput != EXIT_FUNCTION:

            #initiate variable for user choice validation
            validInput = False

            #validation loop for user choice
            while (not validInput):
                userInput = input("\nSelect an option ('1','2','R',etc.): ")
                validInput = validMenuChoice(userInput)

                if (not validInput):
                    print("\n***Error: Invalid menu choice***")

            #Compare with constants to select the correct menu option
            if userInput == DEC_TO_BASE_N:
                decToBaseN()
            
            elif userInput == BASE_N_TO_DEC:
                baseNToDec()
        
            elif userInput == SIGN_BIN:
                signBinary()

            elif userInput == HEX_TO_RGB:
                hexToRGB()

            elif userInput.upper() == REPRINT_MENU:
                os.system('cls')
                printMenu()
                #variable allows for yes or no prompt to not be printed
                promptAgain = False

            elif userInput.upper() == EXIT_FUNCTION:
                exitFunction = True

    return


def decToBaseN():
    #boolean variable for valid input loop
    validUserDec = False
    validUserBase = False

    #input validation loop checks if an integer is entered
    while (not validUserDec):

        userDec = input("\nPlease enter a decimal number using digits 0-9 (no decimals): ")

        validUserDec = validDecimalNum(userDec)

    #input validation loop checks if the base entered is valid
    while (not validUserBase):
        
        base = input("Enter a base value from 2-36: ")

        #send to error checking function
        validUserBase = validBase(base)

    #convert userNum to and base to integers after both are valid
    userDec = int(userDec)
    base = int(base)

    #calculate the number of digits in the final number
    digits = digitCount(userDec, base)

    #initialize blank list for calculation function
    userDecList = [""] * digits

    #fill list with calculated digits from user inputted number
    userDecList = calcBaseN(userDecList, userDec, base)

    #convert the list into a string
    newUserDec = listToString(userDecList)

    #print output
    print(f"\n{userDec} in base {base} is equal to {newUserDec}")
    
    return


def baseNToDec():
    #initialize boolean variables for error checking loops
    validUserBase = False
    validUserNum = False

    #input validation loop checks if the base entered is valid
    while (not validUserBase):
        base = input("\nEnter a base value from 2-36: ")
        
        #send to error checking function
        validUserBase = validBase(base)

    #convert base value to int for calculations
    base = int(base)

    if base >= 16:
            print("\n*Use capital letters for alphabetical characters*")

    while (not validUserNum):
        userNum = input(f"Please enter a number in base-{base} form: ")
        validUserNum = validBaseNum(userNum, base)

    userNumList = [""] * (len(userNum))

    #convert user string to a list
    userNumList = stringToList(userNum)

    #convert the list into a final string in decimal form
    finalNum = calcBaseTen(userNumList, base)

    #print output
    print(f"\n{userNum} in base-{base} is equal to {finalNum} in decimal.")
    
    return


def signBinary():
    #intiate boolean for validation loop
    validUserDec = False
    negative = False
    base = BINARY_BASE
    
    #input validation loop checks if an integer is entered
    while (not validUserDec):

        userDec = input("\nPlease enter a decimal number using digits 0-9 (no decimals) from -128 to 127: ")
        originalDec = userDec

        #remove negative and store if it existed
        if userDec[0] == "-":
            userDec = userDec[1:]
            negative = True

        validUserDec = validDecimalNum(userDec)

        if validUserDec:

            #check if user input is in the range of a signed bit
            if not((int(userDec) >= -128) and (int(userDec) <= 127)):
                validUserDec = False
                print("\n***Error: Value must be between -128 and 127***")

    #convert to integer for calculations
    userDec = int(userDec)

    #calculate the number of digits in the final number
    digits = digitCount(userDec, base)

    #initialize blank list for calculation function
    userDecList = [""] * digits

    #fill list with calculated digits from user inputted number
    userBinList = calcBaseN(userDecList, userDec, base)

    #add any necessary zeros to fill a byte
    if len(userBinList) < BYTE_LENGTH:
        listLength = BYTE_LENGTH - len(userBinList)
        concatList = [0] * listLength
        userBinList = concatList + userBinList

    #take steps for signing if the number is negative    
    if negative:
        
        #invert the values of the binary number
        userBinList = invertValues(userBinList)

        #convert to decimal to add 1 if negative
        invDecNum = calcBaseTen(userBinList, base)
        
        invDecNum += 1
        

        #convert back to binary
        invDecList = [""] * BYTE_LENGTH
        invBinList = calcBaseN(invDecList, invDecNum, base)
        signedBinNum = listToString(invBinList)

    #if not negative, print as is
    else:
        signedBinNum = listToString(userBinList)

    #print output
    print(f"\n{originalDec} as a signed byte is equal to {signedBinNum}")

    return


#function converts a color hex code into its associated RGB values
def hexToRGB():
    validUserHex = False
    base = HEX_BASE

    #validation loop for length and characters used
    while (not validUserHex):
        print("\n*Use capital letters for non-numeric digits*")
        hexValue = input("Please enter a six-digit hex color value: #")
        validUserHex = validBaseNum(hexValue, base)

        if len(hexValue) != 6:
            print(f"\n***Error: value must contain six digits***\n")
            validUserHex = False

    #convert to a list for function loops
    hexValueList = stringToList(hexValue)

    #use list splicing to return each color value
    redValue = calcBaseTen(hexValueList[:2], base)
    greenValue = calcBaseTen(hexValueList[2:4], base)
    blueValue = calcBaseTen(hexValueList[4:], base)

    #print output
    print(f"\nRed: {redValue}\nGreen: {greenValue}\nBlue: {blueValue}")

    return


#function calculates the digits needed in a baseN number given the decimal number
def digitCount(userDec, base):
    digits = 0
    
    #subtracts increasing powers of the base until number
    #is negative to determine digit count
    while userDec > 0:
        userDec -= base**digits

        if userDec > 0:
            digits += 1

    #account for binary undercalculation
    if base == 2:
        digits += 1

    return digits


#function calculates the digits 
def calcBaseN(userDecList, userDec, base):
    #set count variable for later use as an exponent
    count = len(userDecList) - 1

    for index in range(len(userDecList)):

        #calculate the digit value by integer dividing by the largest divisible power of the base
        if (userDec // (base ** count)) < 10:
            userDecList[index] = userDec // (base ** count)

        #convert to character digits if applicable
        else:
            userDecList[index] = chr(userDec // (base ** count)+55)

        #set userNum to the remainder of the previous division expression
        userDec = userDec % (base ** count)

        #advance count by one less for next loop iteration
        count -= 1

    #return the final number in list form
    return userDecList


#function converts any base number to decimal
def calcBaseTen(numList, base):
    #initialize sum variables
    newNum = 0
    count = 0

    #initialize new list for list reversing loop
    revNumList = [""] * len(numList)

    #reverse the digits of the number
    for index in range(len(numList)):
        revNumList = numList[::-1]

    #convert any character digits to numeric digits
    for index in range(len(revNumList)):
        if str(revNumList[index]).isalpha():
            revNumList[index] = ord(revNumList[index]) - 55

    #calculate the value in base-10
    for index in range(len(revNumList)):
        #sum the digits by increasing powers
        newNum += int(revNumList[index]) * (base ** count)

        #increase the base place by 1
        count += 1
    
    #return the base-10 number to the function
    return newNum


#function converts zeros to ones and vice versa in a list
def invertValues(inputList):

    #loop iterates over list and inverts values
    for i in range(len(inputList)):
        if inputList[i] == 0:
            inputList[i] = 1

        elif inputList[i] == 1:
            inputList[i] = 0

    #return new list
    return inputList


#function converts a string to a list
def stringToList(string):
    #initiate blank list for the length of the string
    newList = [""] * (len(string))

    #iterate over the string and set each index equal to an index of the list
    for i in range(len(string)):
        newList[i] = string[i]

    #return the final list
    return newList

#function converts a list into a string using concatenation
def listToString(inputList):
    #initialize string
    string = ""

    #use concatination for string conversions
    #(I'm opposed to the join method for some reason)
    for i in range(len(inputList)):
        string = string + str(inputList[i])

    #return the final string    
    return string


#function prints out the main menu
def printMenu():
    
    print("1. Convert a decimal number to another base.")
    print("2. Covert a number from any base to a decimal number.")
    print("3. Sign a binary number using two's compliment.")
    print("4. Convert a color hexidecimal code to its RGB values.")

    print("\nEnter 'R' to clear the screen and reprint the menu")
    print("Enter 'E' to exit the program.")

    return


#checks if the user's menu choice is valid
def validMenuChoice(userInput):
    validInput = False
    
    for i in range(len(OPTION_LIST)):
        if OPTION_LIST[i] == userInput:
            validInput = True
    
    return validInput

#checks for a valid *general* decimal number
def validDecimalNum(userDec):
    decValid = False

    #check if user input contains only numerical characters
    decValid = userDec.isdigit()

    #print error message if other characters are included
    if (not decValid):
        print("\n***Error: Please use only digits 0-9***")

    else:
        decValid = True

    return decValid

#checks if the entered base is within a valid range
def validBase(base):
    validUserBase = False

    #check if user input contains only numerical characters and is above 2
    validUserBase = base.isdigit()

    if validUserBase:
        base = int(base)

    #check if the base is in the proper range
    if (validUserBase == True) and (base >= 2 and base <= 36):
        validUserBase = True

    #print error message if other characters are included or base is out of range
    else:
        print("\n***Error: Please use only base 2-36***\n")
        validUserBase = False      

    return validUserBase

#checks if an entered number is within the character set of its base
def validBaseNum(userNum, base):
    validUserNum = False
    error = False

    #check for any symbols not in any character set
    if userNum.isalnum():
        #initialize list for string to be converted into a list
        numList = [""] * len(userNum)
        
        for index in range(len(userNum)):

            #checks if character is alphabetical
            if userNum[index].isalpha():

                #convert alphabetical characters to numbers using ascii conversion
                numList[index] = ord(userNum[index]) - 55

            else:
                numList[index] = userNum[index]

            #check if the character is outside of the base's character set
            if int(numList[index]) > (base - 1):
                #accumulate error counter
                error = True

    else:
        error = True

    #send back valid boolean if no errors are found
    if (not error):
        validUserNum = True

    #print error message if any are found
    else:
        validUserNum = False
        print("\n***Error: Characters outside of the base character set were used***\n")

    return validUserNum


    
main()
