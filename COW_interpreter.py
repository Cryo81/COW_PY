#python script to interpret COW language defined here :
#https://esolangs.org/wiki/COW
#Use input.cow as an input


import sys

#machine representation / initialization
register=None
pos_mem=0
mem_block=[0]

def interpret(_instr):
    global mem_block,pos_mem,register,code_size
    match _instr:
        case "moo":
            if f.tell()<8:
                return
            f.seek(-8,1)#skip previous instruction
            instr=f.read(3)
            f.seek(1,1)
            while instr.decode('ascii')!="MOO" and f.tell()>=4:
                f.seek(-4,1)
                instr=f.read(3)
                f.seek(-3,1)

        case "mOo":
            if pos_mem==0:
                mem_block=[0]+mem_block
            else:
                pos_mem -= 1

        case "moO":
            if pos_mem==len(mem_block)-1:
                mem_block=mem_block+[0]
            pos_mem+=1
        case "mOO":
            interpret(mem_block[pos_mem])
        case "Moo":
            if mem_block[pos_mem] == 0:
                try:
                    mem_block[pos_mem] = ord(sys.stdin.read(1))
                except:
                    print("Error reading input")
            else :
                sys.stdout.write(chr(mem_block[pos_mem]))
        case "MOo":
            mem_block[pos_mem] -= 1
        case "MoO":
            mem_block[pos_mem] += 1
        case "MOO":
            if mem_block[pos_mem] == 0:
                f.seek(4,1) #skip next instruction
                instr=f.read(3)
                f.seek(1,1)
                while instr.decode("ascii")!="moo": #look for moo
                    if f.tell()>=code_size:
                        return
                    instr=f.read(3)
                    f.seek(1,1)
                return
        case "OOO":
            mem_block[pos_mem] = 0
        case "MMM":
            if register == None:
                register = mem_block[pos_mem]
            else:
                mem_block[pos_mem]=register
                register=None
        case "OOM":
            sys.stdout.write(mem_block[pos_mem])
        case "oom":
            try:
                mem_block[pos_mem]=int(sys.stdin())
            except:
                print("input should be an integer")

    return

#Readfile and execute instruction one by one
f=open("input.cow","rb") #binary mode to enable whence
code_size=f.seek(0,2)
f.seek(0)
while True:
    instr=f.read(3)
    if instr.decode('ascii')=="": break
    f.seek(1,1) #skip whitespace character
    interpret(instr.decode('ascii'))

f.close()

