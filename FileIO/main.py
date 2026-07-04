# ===== OPEN THE STREAM =====
# myFile = open("aish.txt",'r')

# content = myFile.read()
# print(content)
# ===== CLOSE THE STREAM =====

# myFile.close()

#file = open ("aish.txt",'r')

#line = file.readline()

#for i in range(0, 15):
 #   print(line, end='')
  #  line = file.readline()
    
# file.close()

#import datetime
#import time



#log_date = str(datetime.datetime.now())
#log_date = log_date.replace(":", "-")
#print(log_date)
#frequency = 1 # 5 seconds
#file =open(f"{log_date}.txt", "w")

#for i in range (0, 20):
    #time.sleep(frequency)
    #print("Waking up")
    #file.write("Starting all engines")
    #log_date = str(datetime.datetime.now())
    #log_date = log_date.replace(":", "-")
    #print(f"New date is{log_date}")
    #file = open(f"{log_date}.txt", 'w')

    
#file.close()

#linesTowrite = ["Qaanitat", "\nis a mischievous girl","\nShe reads alot", "\nwatches films alot" ]
#with open("aish.txt", "a") as myFile:
    #myFile.writelines(linesTowrite)

from todo import startup

FILE_NAME = "todo.txt"


def main():
    startup(FILE_NAME)


main()