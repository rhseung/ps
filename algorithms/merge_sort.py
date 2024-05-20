def merge_sort(A, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(A, left, mid)
        merge_sort(A, mid + 1, right)
        merge(A, left, mid, right)

def _merge(A, left, mid, right):
    L = A[left:mid+1]
    R = A[mid+1:right+1]
    
    l, r = 0, 0
    i = left
    
    while l < len(L) and r < len(R):
        if L[l] <= R[r]:
            A[i] = L[l]
            l += 1
        else:
            A[i] = R[r]
            r += 1
        i += 1
    
    while l < len(L):
        A[i] = L[l]
        i += 1
        l += 1
    
    while r < len(R):
        A[i] = R[r]
        i += 1
        r += 1

def merge(A, left, mid, right):
    # i: L의 시작 idx, j: R의 시작 idx, k: 병합 배열의 시작 idx
    i, j, k = left, mid + 1, left
    sorted = [None] * len(A)
    
    while i <= mid and j <= right:
        if A[i] <= A[j]:
            sorted[k] = A[i]
            i += 1
        else:
            sorted[k] = A[j]
            j += 1
        k += 1
    
    if mid < i:
        sorted[k:k + right - j + 1] = A[j:right + 1]
    else:
        sorted[k:k + mid - i + 1] = A[i:mid + 1]
        
    A[left:right + 1] = sorted[left:right + 1]

if __name__ == "__main__":
    import random
    
    A = [random.randint(1, 100) for _ in range(500)]
    print(A)
    merge_sort(A, 0, len(A) - 1)
    print(A)
