#coding: utf-8
import  ldap

ldappath = "ldap://172.16.6.107"
baseDN = "dc=test,dc=com"
ldapuser = "cn=admin,dc=test,dc=com"
ldappass = "123456"
user = "zhouyanjiang"

l = ldap.initialize(ldappath)
print l.simple_bind_s(ldapuser,ldappass)
