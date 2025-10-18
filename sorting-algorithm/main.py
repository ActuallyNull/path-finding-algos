import random

def bubbleSort(arr):
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0,n-i-1):                        # Check if value at index j is bigger than index j+1
            if arr[j]>arr[j+1]:                         # if so, swap places, if not continue with the next index
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True

        if (swapped==False):
            break
    print("Bubble sorted array: "+str(arr))

def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j>=0 and key<arr[j]:                      # Check if the key is smaller than index j
            arr[j+1] = arr[j]                           # if so, insert at index j again and again until
            j-=1                                        # the conditions aren't valid anymore
        arr[j+1] = key                                  # and make index j+1 the new key and start again
    print("Insertion sorted array: "+str(arr))

def selectionSort(arr):
    n = len(arr)
    for i in range (n-1):                               # Go through the array and find the index of the array's
        min_idx = i                                     # smallest value and update min_idx. then switch it with
        for j in range (i+1, n):                        # the first unsorted index
            if arr[j]<arr[min_idx]:
                min_idx=j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    print("Selection sorted array: "+str(arr))

def partition(arr, low, high):
    
    # choose the pivot
    pivot = arr[high]
    
    # index of smaller element and indicates 
    # the right position of pivot found so far
    i = low - 1
    
    # traverse arr[low..high] and move all smaller
    # elements to the left side. Elements from low to 
    # i are smaller after every iteration
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            swap(arr, i, j)
    
    # move pivot after smaller elements and
    # return its position
    swap(arr, i + 1, high)
    return i + 1

# swap function
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

# the QuickSort function implementation
def quickSort(arr, low, high):
    if low < high:
        
        # pi is the partition return index of pivot
        pi = partition(arr, low, high)
        
        # recursion calls for smaller elements
        # and greater or equals elements
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)

def merge(arr, left, mid1, mid2, right):
    
    # Sizes of three subarrays
    size1 = mid1 - left + 1
    size2 = mid2 - mid1
    size3 = right - mid2
    
    # Temporary arrays for three parts
    left_arr = arr[left:left + size1]
    mid_arr = arr[mid1 + 1:mid1 + 1 + size2]
    right_arr = arr[mid2 + 1:mid2 + 1 + size3]
    
    # Merge three sorted subarrays
    i = j = k = 0
    index = left
    
    while i < size1 or j < size2 or k < size3:
        min_value = float('inf')
        min_idx = -1
        
        # Find the smallest among the three current elements
        if i < size1 and left_arr[i] < min_value:
            min_value = left_arr[i]
            min_idx = 0
        if j < size2 and mid_arr[j] < min_value:
            min_value = mid_arr[j]
            min_idx = 1
        if k < size3 and right_arr[k] < min_value:
            min_value = right_arr[k]
            min_idx = 2
        
        # Place the smallest element in the merged array
        if min_idx == 0:
            arr[index] = left_arr[i]
            i += 1
        elif min_idx == 1:
            arr[index] = mid_arr[j]
            j += 1
        else:
            arr[index] = right_arr[k]
            k += 1
        
        index += 1

def threeWayMergeSort(arr, left, right):
    
    # Base case: If single element, return
    if left >= right:
        return
    
    # Finding two midpoints for 3-way split
    mid1 = left + (right - left) // 3
    mid2 = left + 2 * (right - left) // 3
    
    # Recursively sort first third
    threeWayMergeSort(arr, left, mid1)
    
    # Recursively sort second third
    threeWayMergeSort(arr, mid1 + 1, mid2)
    
    # Recursively sort last third
    threeWayMergeSort(arr, mid2 + 1, right)
    
    # Merge the sorted parts
    merge(arr, left, mid1, mid2, right)

def bogoSort(arr):
    n = len(arr)
    while (is_sorted(arr) == False):
        shuffle(arr)
    print("Bogo sorted array: "+str(arr))

def is_sorted(arr):
    n = len(arr)
    for i in range (0, n-1):
        if (arr[i]>arr[i+1]):
            return False
    return True

def shuffle(arr):
    n = len(arr)
    for i in range(0,n):
        r = random.randint(0,n-1)
        arr[i],arr[r]=arr[r],arr[i]

arr = [4,7,1,5,8,3]
n = len(arr)
bubbleSort(arr)
insertionSort(arr)
selectionSort(arr)
quickSort(arr, 0, n-1)
print("Quick sorted array: "+str(arr))
threeWayMergeSort(arr, 0, n-1)
print("Merge sorted array: "+str(arr))
bogoSort()