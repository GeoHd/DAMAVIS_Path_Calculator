from threading import Lock, Thread
import copy, sys, ast


counter_lock = Lock()
path_counter = 0
original_board = []


# This method is used to investigate the possibilities of next moves.
# Entry parameters:
### snake: A list of lists of two integers. Represents the snake
### direction: A string that includes the direction of the next move. It can take four values: right, left, up and down
### original_board: A global variable that is used to make sure that the snake doesn't escape the board
# Result:
### The method returns a boolean value that indicates the possibility of the indicated move

def available(snake, direction):
    global original_board
    if (direction == "right"):
        return ((not [snake[0][0]+1,snake[0][1]] in snake[0:-1]) and snake[0][0]+1 < original_board[0])
    if (direction == "left"):
        return ((not [snake[0][0]-1,snake[0][1]] in snake[0:-1]) and snake[0][0]-1 >= 0)
    if (direction == "up"):
        return ((not [snake[0][0],snake[0][1]-1] in snake[0:-1]) and snake[0][1]-1 >= 0)
    if (direction == "down"):
        return ((not [snake[0][0],snake[0][1]+1] in snake[0:-1]) and snake[0][1]+1 < original_board[1])


# This method is used to update the snakes nodes after moving
# Entry parameters:
### snake: A list of lists of two integers. Represents the snake
### direction: A string that includes the direction of the next move. It can take four values: right, left, up and down
# Result:
### The method returns a new snake adding the new node to the biginning of the snake and erasing the last node
def move_snake (snake, direction):
    if (direction == "right"):
        new_snake = copy.copy(snake)
        new_snake.insert(0,[snake[0][0]+1,snake[0][1]])
        del new_snake[-1]

    elif (direction == "left"):
        new_snake = copy.copy(snake)
        new_snake.insert(0,[snake[0][0]-1,snake[0][1]])
        del new_snake[-1]
    
    elif (direction == "up"):
        new_snake = copy.copy(snake)
        new_snake.insert(0,[snake[0][0],snake[0][1]-1])
        del new_snake[-1]
    
    elif (direction == "down"):
        new_snake = copy.copy(snake)
        new_snake.insert(0,[snake[0][0],snake[0][1]+1])
        del new_snake[-1]
    
    return new_snake


# This method is the core of this program. It is called recursively and it basically checks if a movi is possible 
# within the depth margin. If positive, it launchs a new thread that calls the method again after moving the snake 
# and decrementing depth. Finally, when depth reaches 1, the global variable path_counter will be incremented with
# each possible move. This function only finishes after all the threads are closed.
# Entery parameters:
### snake: A list of lists of two integers. Represents the snake
### depth: A positive integer that refers to the depth left till we start calculating path possibilities
### path_counter: A global integer that accumulates the path posibilities
# This method doesn't return anything. It's labour is to update the global variable
def search_loop(snake, depth):
    global path_counter
    

    if (available(snake,"right")):
        if (depth == 1):
            counter_lock.acquire()
            path_counter += 1
            counter_lock.release()
        else:     
            new_snake = move_snake(snake, "right")
            new_depth = depth -1
            t1= Thread(target=search_loop,args=(new_snake,new_depth))
            t1.start()
            t1.join()
            
    if (available(snake,"left")):
        if (depth == 1):
            counter_lock.acquire()
            path_counter += 1
            counter_lock.release()
        else:
            new_snake = move_snake(snake, "left")
            new_depth = depth -1
            t1= Thread(target=search_loop,args=(new_snake,new_depth))
            t1.start()
            t1.join()

    if (available(snake,"up")):
        if (depth == 1):
            counter_lock.acquire()
            path_counter += 1
            counter_lock.release()

        else:                
            new_snake = move_snake(snake, "up")
            new_depth = depth -1
            t1= Thread(target=search_loop,args=(new_snake,new_depth))
            t1.start()
            t1.join()

    if (available(snake,"down")):
        if (depth == 1):
            counter_lock.acquire()
            path_counter += 1
            counter_lock.release()
            
        else:
            new_snake = move_snake(snake, "down")
            new_depth = depth -1
            t1= Thread(target=search_loop,args=(new_snake,new_depth))
            t1.start()
            t1.join()   
    
    return

# This method prepares the environment for the recursive call
# Entery parameters:
### snake: A list of lists of two positive integers. Given by the end user and represents the snake
### border: A list of two positive integers. Given by the end user and represents the border size
### depth: A positive integer that refers to the depth left till we start calculating path possibilities
# After calling the recursive method, this method returns the final result
def numberOfAvailableDifferentPaths(snake, board, depth):
    global path_counter
    global original_board
    original_board = board
    snake_length = len(snake)
    if (board[0]*board[1]<snake_length):
        exit("Your snake is too big for the board")
    
    if (board[0]*board[1]== snake_length):
        if(available(snake,"right") or available(snake,"left") or available(snake,"up") or available(snake,"down")):
            return 1
        else:
            return 0
    
    search_loop(snake,depth)
    
    return (path_counter)





if __name__ == "__main__":

    try:
        snake = ast.literal_eval(sys.argv[1])
        if (type(snake)!= list):
            exit(1)
    
    except:
        print("Type issue in the first argument. Please make sure to enter a valid snake format.")
        exit(1)
        

    try: 
        board = ast.literal_eval(sys.argv[2])
        if (type(board)!= list):
            exit(1)
    except:
        print("Type issue in the second argument. Please make sure to enter a valid board format (A list of two integers).")
        exit(1)
    


    try:
        for i in snake:
            if  (i[0]>=board[0] or i[0]<0 or i[1]>=board[1] or i[1]<0):
                exit(1)
    except:
        print("An issue occured while validating entries. Looks like either your snake and/or your border don't match the description or your snake has escaped the borders.")
        exit(1)


    try:
        depth = int(sys.argv[3])
        if (depth<=0):
            exit(1)
    except:
        print("Type issue in the third argument. Please make sure to enter a valid depth format (A possitive integer).")
        exit(1)
   
    
    print("Total number of possible paths is: "+str(numberOfAvailableDifferentPaths(snake, board, depth)))

