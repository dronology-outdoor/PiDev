from os import listdir
from simple_settings import settings

print (settings.LOG_FILE)
print (settings.DIR)
f=open(settings.LOG_FILE,'w')
f.write("Hello DOgs")
f.close()

a=listdir(settings.DIR)
print("HERE")
b=listdir('./')
print(a,b)
