# 始终生效

def selection_sort(arr):
    """
    选择排序算法实现
    
    参数:
        arr: 待排序的列表
    
    返回:
        排序后的列表
    """
    n = len(arr)
    # 复制数组，避免修改原数组
    arr_copy = arr.copy()
    
    # 外层循环控制已排序区域的边界
    for i in range(n):
        # 假设当前位置为最小值的索引
        min_index = i
        
        # 在未排序区域中查找最小元素
        for j in range(i + 1, n):
            if arr_copy[j] < arr_copy[min_index]:
                min_index = j
        
        # 将找到的最小元素与当前位置元素交换
        arr_copy[i], arr_copy[min_index] = arr_copy[min_index], arr_copy[i]
    
    return arr_copy


if __name__ == "__main__":
    # 测试选择排序
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("原始数组:", test_array)
    
    sorted_array = selection_sort(test_array)
    print("选择排序后:", sorted_array)
    
    # 测试其他情况
    print("\n测试空数组:", selection_sort([]))
    print("测试单元素数组:", selection_sort([1]))
    print("测试已排序数组:", selection_sort([1, 2, 3, 4, 5]))
    print("测试逆序数组:", selection_sort([5, 4, 3, 2, 1]))
