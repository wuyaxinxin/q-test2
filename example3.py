# 始终生效

def fibonacci(n):
    """
    生成斐波那契数列
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def main():
    n = 10
    result = fibonacci(n)
    print(f"前{n}个斐波那契数: {result}")


if __name__ == "__main__":
    main()
