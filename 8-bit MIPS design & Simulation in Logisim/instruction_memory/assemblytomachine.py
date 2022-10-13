import re

def getRegisterNumber(registerName):
    if registerName == "$zero":
        return "0"
    elif registerName == "$t0":
        return "1"
    elif registerName == "$t1":
        return "2"
    elif registerName == "$t2":
        return "3"
    elif registerName == "$t3":
        return "4"
    elif registerName == "$t4":
        return "5"
    
    return ""
  
def convertToHex(number):
    if(int(number) < 0):
        num = int(number)
        num = 255 + num + 1
        num = num | (1<<7)
        return hex(num).split("x")[-1]
    if(int(number) < 16):
        return "0" + hex(int(number)).split("x")[-1]
    else:
        return hex(int(number)).split("x")[-1]

def getLabelAddress(label, lines):
    count = 0
    label = label + ":"
    for line in lines:
        line = line.strip().split(" ")
        if line[0] == label:
            return count
        if len(line) > 1:
            count = count + 1
    
    return -1

def isNaN(number):
    try:
        float(number)
        return True
    except:
        return False

input = open("input.txt", "r")
output = open("machinecode.txt", "w")
lines = input.readlines()
output.write("v2.0 raw\n")
instruction = ""
count = 0
# print(lines)
for line in lines:
    line = re.split("\s|[,]", line)
    line = [i for i in line if i != '']
    # print(str(count) + " : " + str(line))
    if line[0] == "add":
        instruction = "f" + getRegisterNumber(line[2]) + getRegisterNumber(line[3]) + getRegisterNumber(line[1]) + "0" + "\n"
        count = count + 1
    elif line[0] == "addi":
        instruction = "b" + getRegisterNumber(line[2]) + getRegisterNumber(line[1]) + convertToHex(line[3]) + "\n"
        count = count + 1
    elif line[0] == "sub":
        instruction = "d" + getRegisterNumber(line[2]) + getRegisterNumber(line[3]) + getRegisterNumber(line[1]) + "0" + "\n"
        count = count + 1
    elif line[0] == "subi":
        instruction = "1" + getRegisterNumber(line[2]) + getRegisterNumber(line[1]) + convertToHex(line[3]) + "\n"
        count = count + 1
    elif line[0] == "and":
        instruction = "8" + getRegisterNumber(line[2]) + getRegisterNumber(line[3]) + getRegisterNumber(line[1]) + "0" + "\n"
        count = count + 1
    elif line[0] == "andi":
        instruction = "0" + getRegisterNumber(line[2]) + getRegisterNumber(line[1]) + convertToHex(line[3]) + "\n"
        count = count + 1
    elif line[0] == "or":
        instruction = "c" + getRegisterNumber(line[2]) + getRegisterNumber(line[3]) + getRegisterNumber(line[1]) + "0" + "\n"
        count = count + 1
    elif line[0] == "ori":
        instruction = "e" + getRegisterNumber(line[2]) + getRegisterNumber(line[1]) + convertToHex(line[3]) + "\n"
        count = count + 1
    elif line[0] == "sll":
        instruction = "5" + hex(int(line[3])).split("x")[-1] + getRegisterNumber(line[2]) + getRegisterNumber(line[1]) + "0" + "\n"
        count = count + 1
    elif line[0] == "srl":
        instruction = "7" + hex(int(line[3])).split("x")[-1] + getRegisterNumber(line[2]) + getRegisterNumber(line[1]) + "0" + "\n"
        count = count + 1
    elif line[0] == "nor":
        instruction = "3" + getRegisterNumber(line[2]) + getRegisterNumber(line[3]) + getRegisterNumber(line[1]) + "0" + "\n"
        count = count + 1
    elif line[0] == "sw":
        src = line[2].split("(")
        address = int(src[0]) * 8
        instruction = "4" + getRegisterNumber(src[1][0:3]) + getRegisterNumber(line[1][0:3]) + convertToHex(address) + "\n"
        count = count + 1
    elif line[0] == "lw":
        src = line[2].split("(")
        address = int(src[0]) * 8
        instruction = "6" + getRegisterNumber(src[1][0:3]) + getRegisterNumber(line[1][0:3]) + convertToHex(address) + "\n"
        count = count + 1
    
    elif line[0] == "beq":
        if isNaN(line[3]):
            offsetAddress = int(line[3]) - (count + 1)
            instruction = "2" + getRegisterNumber(line[1]) + getRegisterNumber(line[2]) + convertToHex(str(offsetAddress)) + "\n"
        else:
            labelAddress = getLabelAddress(line[3], lines)
            if labelAddress != -1:
                offsetAddress = labelAddress - (count + 1)
            else: 
                print("error: invalid label at line " + str(count))
            instruction = "2" + getRegisterNumber(line[1]) + getRegisterNumber(line[2]) + convertToHex(str(offsetAddress)) + "\n"
        count = count + 1

    elif line[0] == "bneq":
        if isNaN(line[3]):
            offsetAddress = int(line[3]) - (count + 1)
            instruction = "9" + getRegisterNumber(line[1]) + getRegisterNumber(line[2]) + convertToHex(str(offsetAddress)) + "\n"
        else:
            labelAddress = getLabelAddress(line[3], lines)
            if labelAddress != -1:
                offsetAddress = labelAddress - (count + 1)
            else: 
                print("error: invalid label at line " + str(count))
            instruction = "9" + getRegisterNumber(line[1]) + getRegisterNumber(line[2]) + convertToHex(str(offsetAddress)) + "\n"
        count = count + 1

    elif line[0] == "j":
        if isNaN(line[1]):
            instruction = "a" + convertToHex(line[1]) + "0" + "0" + "\n"
        else:
            labelAddress = getLabelAddress(line[1], lines)
            if labelAddress == -1:
                print("error: invalid label at line " + str(count))
            instruction = "a" + convertToHex(str(labelAddress)) + "0" + "0" + "\n"
        count = count + 1
    # elif line[0] == "beq":
    #     labelAddress = getLabelAddress(line[3], lines)
    #     if labelAddress != -1:
    #         offsetAddress = labelAddress - (count + 20)
    #     else: 
    #         print("error: invalid label at line " + str(count))
    #     instruction = "2" + getRegisterNumber(line[1][0:3]) + getRegisterNumber(line[2][0:3]) + convertToHex(str(offsetAddress)) + "\n"
    #     count = count + 20
    # elif line[0] == "bneq":
    #     labelAddress = getLabelAddress(line[3], lines)
    #     if labelAddress != -1:
    #         offsetAddress = labelAddress - (count + 20)
    #     else: 
    #         print("error: invalid label at line " + str(count))
    #     instruction = "9" + getRegisterNumber(line[1][0:3]) + getRegisterNumber(line[2][0:3]) + convertToHex(str(offsetAddress)) + "\n"
    #     count = count + 20
    # elif line[0] == "j":
    #     labelAddress = getLabelAddress(line[1], lines)
    #     if labelAddress == -1:
    #         print("error: invalid label at line " + str(count))
    #     instruction = "a" + convertToHex(str(labelAddress)) + "0" + "0" + "\n"
    #     count = count + 20

    output.write(instruction) 
    instruction = ""
    
input.close()
output.close()