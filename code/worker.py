worker :


import rpyc
import random
import sys,time
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

def main():
    # Connect to the server
    connections = []
    ip_addresses = ["10.113.6.125","10.113.6.227","10.113.7.32"]
    for ip in ip_addresses:
        print("Connecting to ", ip)
        connections.append(rpyc.connect(ip, 18812))
        print("Connected to ", ip)
    
    res = []
    start_time = time.time()
    print("Sending array to server instance 1")
    arr = list(map(int, input("Enter the array: ").split()))
    sorted_arr = connections[0].root.mergesort_mpi(arr)
    for i in sorted_arr:
        res.append(i)
    print(res)
    print("Sending array to server instance 2")
    arr = list(map(int, input("Enter the array: ").split()))
    sorted_arr = connections[1].root.mergesort_mpi(arr)
    for i in sorted_arr:
        res.append(i)
    print(res)
    print("Sending array to server instance 3")
    arr = list(map(int, input("Enter the array: ").split()))
    sorted_arr = connections[2].root.mergesort_mpi(arr)
    for i in sorted_arr:
        res.append(i)
    print(res)

    res = str(connections[0].root.mergesort_mpi(res))

    print("Gathering results from servers")
    # Generate random array
    # Call the remote method on the server
    end_time = time.time()
    print("Time taken: ", end_time - start_time)
    file = open("output.txt", "w")
    file.write((res))
    file.close()
    # print("Result: ", res)
    # Close the connection
    print("Closing connections")
    for conn in connections:
        conn.close()
    print("Connections closed")
if _name_ == '_main_':
    main()