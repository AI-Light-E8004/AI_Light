

while True: 

    user_input = input(" Please enter your lucky word or type 'END' to terminate loop: ")
     
    if user_input == "\n":
        print("You are really a geek")
        break
 
    elif user_input == "END":
        break
 
    else:
        print("Try Again")
