from os import listdir
from simple_settings import settings

print (settings.LOG_FILE)
f=open(settings.LOG_FILE,'w')
f.write("Hello DOgs")
f.close()

os.listdir('/data/')
os.listdir('./')
