# 始终生效

def calculate_sum(numbers):
    """
    计算数字列表的总和
    """
    return sum(numbers)


def calculate_average(numbers):
    """
    计算数字列表的平均值
    """
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def main():
    numbers = [1, 2, 3, 4, 5]
    print(f"数字列表: {numbers}")
    print(f"总和: {calculate_sum(numbers)}")
    print(f"平均值: {calculate_average(numbers)}")


if __name__ == "__main__":
    main()
