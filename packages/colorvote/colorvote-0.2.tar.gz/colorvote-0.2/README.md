# Colorvote

Colorvote is a colored coins protocol for voting on the Bitcoin (and compatible
altcoin) blockchain. It is a modified version of the EPOBC colored coin protocol
and uses the nSequence field to mark transactions. The protocol requires no
changes to the blockchain (i.e. soft forks) and has minimal overhead as votes
are transferred with normal P2PKH transactions. 

This repository contains a detailed protocol specification, a command line
utility, and a web server.

## Command Line
