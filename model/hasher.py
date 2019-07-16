#!/usr/bin/env python3

import bcrypt

def get_pw_hash(plain_text_pw):
    salt = bcrypt.gensalt()
    # salt resets every time function is run
    # printint the salt here just to demonstrate where it is in the returned hash
    print(f'salt: {salt}')
    print(bcrypt.hashpw(plain_text_pw, salt))
    # this can and should be written one line 
    # return bcrypt.hashpw(plain_text_pw, bcrypt.gensalt())

def check_pw(plain_text_pw, hashed_pw):
    # arguments need to be byte strings b'string'
    return bcrypt.checkpw(plain_text_pw, hashed_pw)


if __name__ == '__main__':
    # password and hash must be byte strings b'string' or encoded
    get_pw_hash(b'john')
    print(check_pw(b'john', b'$2b$12$rZLfd.czhy3iFjGSetXis.6elm3G71Pswr3xNjCPWzF3C/iUHojmm'))
    print(check_pw(b'greg', b'$2b$12$rZLfd.czhy3iFjGSetXis.6elm3G71Pswr3xNjCPWzF3C/iUHojmm'))
    #you don't need two separate columns for pw and salt in the db 
    #because first half of string is salt and second half is the pw
    #bcrypt returns True or False
