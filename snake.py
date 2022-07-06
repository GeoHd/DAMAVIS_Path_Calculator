snake = [[2, 2], [3, 2], [3, 1], [3, 0], [2, 0], [1, 0], [0, 0]]
board = [4, 3]
depth = 3
from asyncio.windows_events import NULL
import os
from threading import Lock
from time import sleep
counter_lock = Lock()
path_counter = 0

def available(direction,snake,board):
    if (direction == "right"):
        return (not [snake[0][0]+1,snake[0][1]] in snake and snake[0][0]+1 < board[0])
    if (direction == "left"):
        return (not [snake[0][0]-1,snake[0][1]] in snake and snake[0][0]-1 > 0)
    if (direction == "up"):
        return (not [snake[0][0],snake[0][1]-1] in snake and snake[0][1]-1 > 0)
    if (direction == "down"):
        return (not [snake[0][0],snake[0][1]+1] in snake and snake[0][1]+1 < board[1])
    

def numberOfAvailableDifferentPaths(board, snake, depth):
    global path_counter
    snake_length = len(snake)
    if (board[0]*board[1]<snake_length):
        exit("Your snake is too big for the board")
    ppid = os.getpid()
    for i in range(depth):
        print(1) 
        if (available("right",snake,board)):
            if (i == depth -1):
                counter_lock.acquire()
                path_counter += 1
                counter_lock.release()
                exit(0)
            else:
                pid = os.fork()
                if (pid == 0):
                    snake.insert(0,[snake[0][0],snake[0][1]+1])
                    del snake[-1]
                    continue
                
        if (available("left",snake,board)):
            if (i == depth -1):
                counter_lock.acquire()
                path_counter += 1
                counter_lock.release()
                exit(0)
            else:
                pid = os.fork()
                if (pid == 0):
                    snake.insert(0,[snake[0][0],snake[0][1]-1])
                    del snake[-1]
                    continue
                            
        if (available("up",snake,board)):
            if (i == depth -1):
                counter_lock.acquire()
                path_counter += 1
                counter_lock.release()
                exit(0)
            else:                
                pid = os.fork()
                if (pid == 0):
                    snake.insert(0,[snake[0][0]-1,snake[0][1]])
                    del snake[-1]
                    continue
        
        if (available("down",snake, board)):
            if (i == depth -1):
                counter_lock.acquire()
                path_counter += 1
                counter_lock.release()
                exit(0)
            else:
                pid = os.fork()
                if (pid == 0):    
                    snake.insert(0,[snake[0][0],snake[0][1]-1])
                    del snake[-1]
                    continue

        if (os.getpid()!=ppid):
            exit(0)
        break
    counter_lock.acquire()
    sleep(5)
    return (path_counter)

print(available("right",snake,board))
print(available("left",snake,board))
print(available("up",snake,board))
print(available("down",snake,board))

print(numberOfAvailableDifferentPaths(board, snake, depth))

