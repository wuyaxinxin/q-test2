# 始终生效

def bubble_sort(arr):
    """
    冒泡排序算法实现
    
    参数:
        arr: 待排序的列表
    
    返回:
        排序后的列表
    """
    n = len(arr)
    # 复制数组，避免修改原数组
    arr_copy = arr.copy()
    
    # 外层循环控制排序轮数
    for i in range(n):
        # 设置交换标志，用于优化
        swapped = False
        
        # 内层循环进行相邻元素比较和交换
        for j in range(0, n - i - 1):
            # 如果前一个元素大于后一个元素，则交换
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
        
        # 如果本轮没有发生交换，说明已经有序，提前结束
        if not swapped:
            break
    
    return arr_copy


if __name__ == "__main__":
    # 测试冒泡排序
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("原始数组:", test_array)
    
    sorted_array = bubble_sort(test_array)
    print("冒泡排序后:", sorted_array)
    
    # 测试其他情况
    print("\n测试空数组:", bubble_sort([]))
    print("测试单元素数组:", bubble_sort([1]))
    print("测试已排序数组:", bubble_sort([1, 2, 3, 4, 5]))
    print("测试逆序数组:", bubble_sort([5, 4, 3, 2, 1]))
