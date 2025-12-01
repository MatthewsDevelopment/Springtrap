import os
from dotenv import load_dotenv
load_dotenv('.env')

launchmode = os.getenv("LAUNCHMODE")
if launchmode == "0":
    os.system('python ./main-discord.py & python ./main-stoat.py')
elif launchmode == "1":
    os.system('python ./main-discord.py')
elif launchmode == "2":
    os.system('python ./main-stoat.py')
elif launchmode == "3":
    os.system('python ./main-discord.py & python ./main-stoat.py & python ./main-guilded.py')
elif launchmode == "4":
    os.system('python ./main-guilded.py')
elif launchmode == "5":
    os.system('python ./main-discord.py & python ./main-guilded.py')
else:
    print("You did not provide a valid value for LAUNCHMODE inside of the .env file.")
    print("0 = Discord+Stoat bot")
    print("1 = Discord Bot Only")
    print("2 = Stoat Bot Only")
    print("3 = Discord+Stoat+Guilded Bot")
    print("4 = Guilded Bot Only")
    print("5 = Discord+Guilded Bot")
