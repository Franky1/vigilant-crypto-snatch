#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2019 Martin Ueding <dev@martin-ueding.de>

import argparse

import bitstamp.client
import sqlalchemy


greeting = r"""
Welcome to

           $$\    $$\$$\         $$\$$\                   $$\     
           $$ |   $$ \__|        \__$$ |                  $$ |    
           $$ |   $$ $$\ $$$$$$\ $$\$$ |$$$$$$\ $$$$$$$\$$$$$$\   
           \$$\  $$  $$ $$  __$$\$$ $$ |\____$$\$$  __$$\_$$  _|  
            \$$\$$  /$$ $$ /  $$ $$ $$ |$$$$$$$ $$ |  $$ |$$ |    
             \$$$  / $$ $$ |  $$ $$ $$ $$  __$$ $$ |  $$ |$$ |$$\ 
              \$  /  $$ \$$$$$$$ $$ $$ \$$$$$$$ $$ |  $$ |\$$$$  |
               \_/   \__|\____$$ \__\__|\_______\__|  \__| \____/ 
                        $$\   $$ |                                
                        \$$$$$$  |                                
                         \______/                                 
           
           
            $$$$$$\                             $$\              
           $$  __$$\                            $$ |             
           $$ /  \__|$$$$$$\ $$\   $$\ $$$$$$\$$$$$$\   $$$$$$\  
           $$ |     $$  __$$\$$ |  $$ $$  __$$\_$$  _| $$  __$$\ 
           $$ |     $$ |  \__$$ |  $$ $$ /  $$ |$$ |   $$ /  $$ |
           $$ |  $$\$$ |     $$ |  $$ $$ |  $$ |$$ |$$\$$ |  $$ |
           \$$$$$$  $$ |     \$$$$$$$ $$$$$$$  |\$$$$  \$$$$$$  |
            \______/\__|      \____$$ $$  ____/  \____/ \______/ 
                             $$\   $$ $$ |                       
                             \$$$$$$  $$ |                       
                              \______/\__|                       
           
           
            $$$$$$\                    $$\             $$\       
           $$  __$$\                   $$ |            $$ |      
           $$ /  \__$$$$$$$\  $$$$$$\$$$$$$\   $$$$$$$\$$$$$$$\  
           \$$$$$$\ $$  __$$\ \____$$\_$$  _| $$  _____$$  __$$\ 
            \____$$\$$ |  $$ |$$$$$$$ |$$ |   $$ /     $$ |  $$ |
           $$\   $$ $$ |  $$ $$  __$$ |$$ |$$\$$ |     $$ |  $$ |
           \$$$$$$  $$ |  $$ \$$$$$$$ |\$$$$  \$$$$$$$\$$ |  $$ |
            \______/\__|  \__|\_______| \____/ \_______\__|  \__|
  

MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWNMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMWOO0MMMMMMMMMMMMM;  NMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMXOxkKMNKMMMMMMMMM:  NMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMWWMMWdx,MloMMMMMMMMMKl NMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMNc,dKK0ol,K:oKXMMWWMMMMMxWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMKkWMMMX0Wc,',''.;,;..;KN;NMMMWOOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMKNNKkkl' . .  kO;:cl:;dd;'',...'.'....0cKMMMMMNXOl:..::KMMMMMMMMMMMMMMMMMMMM
MM0dko:;dddollccccc::::;''''''........'',;;;;;;;;;;;;;;;;:cldk0XWo..,;dcckMMMX
MWKl;,,,.;,',;,',',,,',;,,,,','.....'',,,'''''''''''''''''''''.'',clcOO:;xKkON
MWNMMMMWWWWNNNX0'OXXXXNNNNNNXXKK000OOOOOOO0000KKKKXXXXXX0kKK0d;;dOxOKXXNWo;lMK
MMMMMMMMMMMMMMMWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMXXMMMMMMMMMWWWMM
""".strip()


def main():
    options = _parse_args()

    print(greeting)


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    options = parser.parse_args()

    return options


if __name__ == '__main__':
    main()
