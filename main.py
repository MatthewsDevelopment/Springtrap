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
    os.system('python ./main-fluxer.py')
elif launchmode == "4":
    os.system('python ./main-guilded.py')
elif launchmode == "5":
    os.system('python ./main-discord.py & python ./main-guilded.py')
elif launchmode == "6":
    os.system('python ./main-discord.py & python ./main-stoat.py & python ./main-fluxer.py')
elif launchmode == "7":
    os.system('python ./main-stoat.py & python ./main-fluxer.py')
else:
    print("You did not provide a valid value for LAUNCHMODE inside of the .env file.")
    print("0 = Discord+Stoat bot")
    print("1 = Discord Bot Only")
    print("2 = Stoat Bot Only")
    print("3 = Fluxer Bot Only")
    print("4 = Guilded Bot Only")
    print("5 = Discord+Guilded Bot")
    print("6 = Discord+Stoat+Fluxer Bot")
    print("7 = Stoat+Fluxer Bot")
