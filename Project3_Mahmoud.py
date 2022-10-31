import sys

# Checks the type of MIPS code by checking the function
def checkType(line):
	splitLine = line.split(" ")
	if (splitLine[0] == "add" or splitLine[0] == "sub" or splitLine[0] == "sll" or splitLine[0] == "srl"):
		return "R type"
	elif (splitLine[0] == "addi" or splitLine[0] == "beq" or splitLine[0] == "bne" or splitLine[0] == "lw" or splitLine[0] == "sw"):
		return "I type"
	elif (splitLine[0] == "j"):
		return "J type"
	else:
		return "None"

# Gets the binary code for rType MIPS code
def rType(line,f):
    binary = "000000"
    x = line.split(",")
    y = x[0].split(" ")
    func = y[0]
    neg = False
	
    instruction1 = y[-1].replace("$","")
    instruction2 = x[1].replace("$","")
    instruction3 = x[2].replace("$","")
	
    instruction1, instruction2, instruction3 = changeToNum(instruction1, instruction2, instruction3)

    if int(instruction3) < 0:
        neg = True
    if int(instruction3) > 65535 or int(instruction3) < -32768:
        f.write("!!! Invalid Input !!!\n")
        quit()

    if func == "add":
        funcCode = "100000" 
    elif func == "sub":
        funcCode = "100010"
    elif func == "sll":
        funcCode = "000000"
    elif func == "srl":
        funcCode = "000010"
	
    bin1 = f'{int(instruction1):05b}'
    bin2 = f'{int(instruction2):05b}'
    bin3 = f'{int(instruction3):05b}'

    if neg == True:
        bin3 = bin(instruction3)
	
    if func == "add" or func == "sub":
        binary = binary + bin2 + bin3 + bin1 + "00000" + funcCode
    elif func == "sll" or func == "srl":
        binary = binary + "00000" + bin2 + bin1 + bin3 + funcCode
	
    f.write(binary + "\n")
	
# Gets the binary code for iType MIPS code
def iType(line,f):
    x = line.split(",")
    y = x[0].split(" ")
    func = y[0]
    print(x)
    neg = False
	
    instruction1 = y[-1].replace("$","")

    if func == 'sw' or func == 'lw':
        z = x[1]
        x = z.split("(")
        instruction2 = x[0]
        x[1] = x[1].replace("$","")
        instruction3 = x[1].replace(")","")
    else:
        instruction2 = x[1].replace("$","")
        instruction3 = x[2].replace("$","")
	
    instruction1, instruction2, instruction3 = changeToNum(instruction1,instruction2,instruction3)

    if int(instruction3) < 0:
        neg = True
    if int(instruction3) > 65535 or int(instruction3) < -32768:
        f.write("!!! Invalid Input !!!\n")
        quit()
	
    # Gets the opcode for each function
    if (func == "addi"):
        opcode = "001000"
    elif(func == "beq"):
        opcode = "000100"
        instruction3 = int(instruction3) // 4
    elif(func  == "bne"):
        opcode = "000101"
        instruction3 = int(instruction3) // 4
    elif(func == "lw"):
        opcode = "100011"
    elif(func == "sw"):
        opcode = "101011"

    bin1 = f'{int(instruction1):05b}'
    if func == "sw" or func == "lw":
        bin2 = f'{int(instruction2):016b}'
        if neg == True:
            bin3 = ("{0:0%db}" % 5).format(2**5 + int(instruction3))
        else:
             bin3 = f'{int(instruction3):05b}'
    else:
        bin2 = f'{int(instruction2):05b}'
        if neg == True:
            bin3 = ("{0:0%db}" % 16).format(2**16 + int(instruction3))
        else:
             bin3 = f'{int(instruction3):016b}'

        
	
    binary = opcode
		
    if func == "addi":
        binary = binary + bin2 + bin1 + bin3
    elif func == "beq" or func == "bne":
        binary = binary + bin1 + bin2 + bin3
    elif func == "lw" or func == "sw":
        binary = binary + bin3 + bin1 + bin2
	
    f.write(binary + "\n")
	
# Gets the binary codr for jType MIPS code
def jType(line, f):
	x = line.split(" ")
	print(x)
	
	func = x[0]
	
	if func == "j":
		opcode = "000010"
	
	num = x[1].replace("$","")
	num = int(num) // 4
	
	bin1 = f'{num:026b}'
	
	binary = opcode + bin1
	
	f.write(binary + "\n")
	
# Converts each MIPS instruction to decimal equivalent
def changeToNum(instruction1, instruction2, instruction3):
    if instruction1 == "gp":
        instruction1 = 28
    elif instruction1 == "sp":
        instruction1 = 29
    elif instruction1 == "fp":
        instruction1 = 30
    elif instruction1 == "ra":
        instruction1 = 31
    elif instruction1[0] == "s":
        instruction1 = instruction1.replace("s","")
        instruction1 = 16 + int(instruction1)
    elif instruction1[0] == "v":
        instruction1 = instruction1.replace("v","")
        instruction1 = 2 + int(instruction1)
    elif instruction1[0] == "a":
        instruction1 = instruction1.replace("a","")
        instruction1 = 4 + int(instruction1)
    elif instruction1[0] == "t":
        instruction1 = instruction1.replace("t","")
        instruction1 = 8 + int(instruction1)

    if instruction2 == "gp":
        instruction2 = 28
    elif instruction2 == "sp":
        instruction2 = 29
    elif instruction2 == "fp":
        instruction2 = 30
    elif instruction2 == "ra":
        instruction2 = 31
    elif instruction2[0] == "s":
        instruction2 = instruction2.replace("s","")
        instruction2 = 16 + int(instruction2)
    elif instruction2[0] == "v":
        instruction2 = instruction2.replace("v","")
        instruction2 = 2 + int(instruction2)
    elif instruction2[0] == "a":
        instruction2 = instruction2.replace("a","")
        instruction2 = 4 + int(instruction2)
    elif instruction2[0] == "t":
        instruction2 = instruction2.replace("t","")
        instruction2 = 8 + int(instruction2)    
        if instruction2 == 16:
            instruction2 = 24
        elif instruction2 == 17:
            instruction2 = 25

    if instruction3 == "gp":
        instruction3 = 28
    elif instruction3 == "sp":
        instruction3 = 29
    elif instruction3 == "fp":
        instruction3 = 30
    elif instruction3 == "ra":
        instruction3 = 31
    elif instruction3[0] == "s":
        instruction3 = instruction3.replace("s","")
        instruction3 = 16 + int(instruction3)
    elif instruction3[0] == "v":
        instruction3 = instruction3.replace("v","")
        instruction3 = 2 + int(instruction3)
    elif instruction3[0] == "a":
        instruction3 = instruction3.replace("a","")
        instruction3 = 4 + int(instruction3)
    elif instruction3[0] == "t":
        instruction3 = instruction3.replace("t","")
        instruction3 = 8 + int(instruction3)

    return instruction1, instruction2, instruction3

# Opens read file and calls necessary function for each line of MIPS code
def main():
    f = open(sys.argv[1], 'r') 
    lines = f.readlines()
    f.close()
	
    f = open("out_code.txt", "w")
	
    for line in lines:
        type = checkType(line)
        if (type == "R type"):
            try:
                rType(line,f)
            except:
                f.write("!!! Invalid Input !!!")
                quit()
        elif (type == "I type"):
            try:
                iType(line,f)
            except:
                f.write("!!! Invalid Input !!!")
                quit()
        else:
            try:
                jType(line,f)
            except:
                f.write("!!! Invalid Input !!!")
                quit()

if __name__ == "__main__":
	main()