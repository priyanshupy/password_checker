import requests
import sys
import hashlib
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code!=200:
        raise RuntimeError(f'Error fetching {res.status_code} check the api and try again')
    return res



def get_password_leaks(hashes,tail):
    hashes = (line.split(':') for line in hashes.text.splitlines())

    for h,count in hashes:
        if(h==tail):
            return count
    return 0

def password_converter(password):
    converted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char, tail = converted_pass[:5], converted_pass[5:]
    response = request_api_data(first5char)
    return get_password_leaks(response,tail)
  

def read_password():
  with open('password.txt',mode='r') as mypassword:
    password=mypassword.readlines()
    new=[n.rstrip('\n') for n in password]
    return new

def main(args): 
   for password in args:
       
       count = password_converter(password)
       if(count==0):
           print(f'your password {password} is safe')
       else:
           print(f'your password {password} was found {count} times it\'s probably better if you change it')
if __name__=='__main__':
    main(read_password())