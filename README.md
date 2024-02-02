# Parallel-Merge-Sort-Using-MPI
Parallel merge-sort is a sorting algorithm that uses the divide-and-conquer 
strategy to sort a large array of elements in parallel. It divides the array into 
subarrays and distributes them among different processes using MPI (Message 
Passing Interface). Each process sorts its subarray using a sequential merge-sort 
algorithm and then sends it back to the parent process. The parent process merges 
the sorted subarrays using a merge function until the whole array is sorted.
Since our main aim is sort them, the thing is just single instruction on 
multiple data. So, it is a good idea to use single instruction multiple parallel 
implementation.
We also compare measured time of serial and parallel version of merge 
sort, parallel version has achieved best speedup. Parallel merge-sort can achieve 
a speedup over serial merge-sort by reducing the communication and 
computation costs
