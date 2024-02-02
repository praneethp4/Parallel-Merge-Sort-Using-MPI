server : 


import rpyc
from mpi4py import MPI
import sys
import time


class MyService(rpyc.Service):

    def on_connect(self, conn):
        print("Connected to the client")

    def on_disconnect(self, conn):
        print("Disconnected from the client")

    def exposed_mergesort_mpi(self, arr):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        def mergesort(array,low,high):
            if low < high:
                if high - low < 100000:
                    array[low:high+1] = sorted(array[low:high+1])
                else:
                    mid = (low + high) // 2
                    mergesort(array, low, mid)
                    mergesort(array, mid + 1, high)
                    merge(array, low, mid, high)
        
        def merge(array,low,mid,high):
            left = array[low:mid+1]
            right = array[mid+1:high+1]
            k = low
            i = 0
            j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    array[k] = left[i]
                    i += 1
                else:
                    array[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                array[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                array[k] = right[j]
                j += 1
                k += 1

        if rank == 0:
            start_time = time.time()
            chunks = [arr[i::size] for i in range(size)]
        else:
            chunks = None

        chunk = comm.scatter(chunks, root=0)
        mergesort(chunk, 0, len(chunk) - 1)
        sorted_chunks = comm.gather(chunk, root=0)

        if rank == 0:
            sorted_arr = []
            for chunk in sorted_chunks:
                sorted_arr.extend(chunk)
            mergesort(sorted_arr, 0, len(sorted_arr) - 1)
            end_time = time.time()
            print("Time taken: ", end_time - start_time)
            print(sorted_arr)
            return sorted_arr


if _name_ == "_main_":
    from rpyc.utils.server import ThreadPoolServer

    # Start the RPyC server
    server = ThreadPoolServer(MyService, port=18812)
    server.start()