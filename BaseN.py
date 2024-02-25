#program converts base-10 to base-2-36

#global constants (main menu)
DEC_TO_BASE_N = "1"
BASE_N_TO_DEC = "2"
SIGN_BIN = "3"
HEX_TO_RGB = "4"


def main():
    print("1. Convert a decimal number to another base.")
    print("2. Covert a number from any base to a decimal number.")
    print("3. Sign a binary number using two's compliment.")
    print("4. Convert a color hexidecimal code to its RGB values.")

    choice = input("\nPlease enter an option (1-4): ")

    if choice == DEC_TO_BASE_N:
        baseTenToN()
        
    elif choice == BASE_N_TO_DEC:
        baseNToDec()

    elif choice == SIGN_BIN:
        signBinary()

    elif choice == HEX_TO_RGB:
        hexToRGB()

    return
        
#function converts a decimal number to another base
def baseTenToN():
    #initialize boolean variable for number error checking loop
    numValid = False

    #error checking loop
    while numValid != True:

        userNum = input("\nPlease enter a base-10 number using digits 0-9 (no decimals): ")

        #send to error checking function
        numValid = validNumDec(userNum)

    #convert userNum to integer after it has been checked to be valid
    userNum = int(userNum)

    #initialize boolean variable for base error checking loop
    baseValid = False

    #error checking loop
    while baseValid != True:
        
        base = input("Enter a base value from 2-36: ")

        #send to error checking function
        baseValid = validBase(base)

    #convert base to integer after it is checked for validity
    base = int(base)

    #get amount of digits in newNum by sending to digit function
    digits = digitCount(userNum, base)

    #initialize baseList by using digit value as the size determiner
    baseList = [""] * digits

    #fill baseList with the actual new digits in calcNum function
    baseList = calcBaseN(baseList, userNum, base)

    baseList = alphaNum(baseList)

    #convert baseList to a string
    newNum = stringConvert(baseList)

    #print output
    print(f"\n{userNum} in base {base} is equal to {newNum}")

    return 


#function converts a number of any base to a decimal number
def baseNToDec():
    #initialize boolean variables for number error checking loops
    baseValid = False
    numValid = False

    #base value error checking loop
    while baseValid != True:
        
        base = input("\nEnter a base value from 2-36: ")

        #send to error checking function
        baseValid = validBase(base)

    base = int(base)

    if base >= 16:
            print("\n*Use capital letters for alphabetical characters*")

    #obtain list from error checking and list building function
    numList = validNumN(base)

    #obtain calculated base-10 number
    newNum = calcBaseTen(numList, base)

    #print output
    print(f"\nThe value entered is equal to {newNum} in base-10.")


    return

def signBinary():
    print("work in progress")

    return


def hexToRGB():
    hexValid = False


    hexValue = input("Please enter a six-digit hex color value: #")

    hexList = validHex(hexValue)

    print(hexList)
        

    return


#determines amount of digits for final number
def digitCount(userNum, base):

    digits = 0
    
    #subtracts increasing powers of the base until number
    #is negative to determine digit count
    while userNum > 0:
        userNum -= base**digits

        if userNum > 0:
            digits += 1

    if base == 2:
        digits += 1

        
    #return digit count to main function
    return digits


#function calculates the value of each digit in the new number
def calcBaseN(baseList, userNum, base):
    #set count variable for later use as an exponent
    count = len(baseList) - 1

    for index in range(len(baseList)):

        #calculate the digit value by integer dividing by the largest divisible power of the base
        baseList[index] = userNum // (base ** count)

        #set userNum to the remainder of the previous division expression
        userNum = userNum % (base ** count)

        #advance count by one less for next loop iteration
        count -= 1

    #return the final number in list form to the main function
    return baseList


#function converts a base-n number to base-10
def calcBaseTen(numList, base):
    #initialize sum variables
    newNum = 0
    count = 0

    #initialize new list for list reversing loop
    revNumList = [""] * len(numList)

    #reverse the digits of the number
    for index in range(len(numList)):
        revNumList = numList[::-1]

    #calculate the value in base-10
    for index in range(len(revNumList)):
        #sum the digits by increasing powers
        newNum += int(revNumList[index]) * (base ** count)

        #increase the base place by 1
        count += 1
    
    #return the base-10 number to the function
    return newNum


#function converts baseList to a string for output printing
def stringConvert(baseList):
    #initialize string
    newNum = ""

    #use concatination for string conversions
    #(I'm opposed to the join method for some reason)
    for index in range(len(baseList)):
        newNum = newNum + str(baseList[index])

    #return the final string to the main function
    return newNum


#function converts characters past 9 to alphabetic characters
def alphaToNum(baseList):
    for index in range(len(baseList)):

        #checks if value is above 10, if so, use ascii chart to sequence through A-Z list
        if baseList[index] > 10:
            num = baseList[index] - 10
            baseList[index] = chr(num + 65)

    #return alphanumeric (if applicable) list to main function
    return baseList


def validNumDec(userNum):
    numValid = False

    #check if user input contains only numerical characters
    try:
        if "." in userNum:
            raise Exception

        userNum = int(userNum)

    #print error message if other characters are included
    except:
        print("\n***Error: Please use only digits 0-9***\n")

    if type(userNum) is int:
        numValid = True

    return numValid


def validBase(base):
    baseValid = False

    #check if user input contains only numerical characters and is above 2
    try:
        base = int(base)

        if base < 2 or base > 36:
            raise Exception

    #print error message if other characters are included or base is out of range
    except:
        print("\n***Error: Please use only base 2-36***\n")

    if (type(base) is int) and (base >= 2 and base <= 36):
        baseValid = True

    return baseValid

#function checks if a base-n number only uses characters in its character set
#and returns the list with only numeric values
def validNumN(base):
    numValid = False


    while numValid != True:

        userNum = input(f"Please enter a number in base-{base} form: ")

        #initialize list for string to be converted into a list
        numList = [""] * len(userNum)

        #assign or reassign error to 0 for each loop
        error = 0
        
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
                error += 1

            #check for any errors, if not, break loop condition
            if error == 0:
                numValid = True

            #if an error is found, print a message and restart the loop
            else:
                print(f"\n***Error: values outside of the character set of base-{base} were used***\n")

    return numList

def validHex(userNum):
    hexValid = False
    base = 16


    while hexValid != True:

        #initialize list for string to be converted into a list
        numList = [""] * len(userNum)
        
        #assign or reassign error to 0 for each loop
        error = 0

        if len(numList) == 6:
        
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
                    error += 1

        else:
            error = -1

        #check for any errors, if not, break loop condition
        if error == 0:
            hexValid = True

        #print length error message 
        elif error == -1:              
            print(f"\n***The value must contain six digits***\n")                
            hexValue = input(f"Please enter a six-digit hex color value: #")


        #if a character error is found, print a message and restart the loop
        else:
            print(f"\n***Error: values outside of the character set of base-16 were used***\n")
            hexValue = input(f"Please enter a six-digit hex color value: #")
            

    return numList

main()
