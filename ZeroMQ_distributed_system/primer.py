"""

"""

# Importing dependences
import sys
import zmq


# Initailising ports
ports = sys.argv

# zmq initialization for inputs and outputs
context = zmq.Context()

# Requesting socket (input)
sock_pub = context.socket(zmq.PUB)

# Subscribing socket (output)
sock_sub = context.socket(zmq.SUB)

# Lets connect the socket now
sock_sub.connect(f"tcp://127.0.0.1:{ports[1]}")
sock_pub.connect(f"tcp://127.0.0.1:{ports[2]}")
sock_sub.setsockopt_string(zmq.SUBSCRIBE, '')

# set a timeout for receive, make it non-blocking
sock_sub.RCVTIMEO = 1000

# Check for the prime number
def is_prime(n):
 n = int(n)
 if n in (2, 3):
    return "Prime"
 if n % 2 == 0:
    return "Not prime"
 for divisor in range(3, n, 2):
   if n % divisor == 0:
    return "not prime"
 return "prime"

try:
    while True:
           
            try:
                while True:
                   command = sock_sub.recv_string()
                   print(command)
                   split_command = command.split()
                   print(len(split_command))
                   # print(isinstance(int(number), int))
                   if (split_command[0] == "isprime" and len(split_command) < 3):
                    if(split_command[1].isdecimal()):
                      result = "The number " + split_command[1] + " is " + is_prime(split_command[1])
                      sock_pub.send_string(command + "\n" + result)
                      print(result)
                    else:
                      sock_pub.send_string("The correct format is 'isprime N' where 'N' is a number ")

                   elif(split_command[0] == "gcd"):
                      pass
                    
                   elif(len(split_command) > 2):
                      sock_pub.send_string(command)

                   

            except zmq.Again:
                pass 
            
                         
# 5. would be covered
except KeyboardInterrupt:
    print("Terminating client")
    sys.exit(0)

