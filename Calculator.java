/**
 * 计算器类，提供基本的数学运算功能
 * 包括加法、减法、乘法和除法运算
 */
public class Calculator {
    public static void main(String[] args) {
        // 示例计算操作
        int num1 = 10;
        int num2 = 5;
        
        System.out.println("数字1: " + num1);
        System.out.println("数字2: " + num2);
        
        System.out.println("加法结果: " + add(num1, num2));
        System.out.println("减法结果: " + subtract(num1, num2));
        System.out.println("乘法结果: " + multiply(num1, num2));
        System.out.println("除法结果: " + divide(num1, num2));
    }
    
    public static int add(int a, int b) {
        return a + b;
    }
    
    public static int subtract(int a, int b) {
        return a - b;
        // 可以添加更多逻辑，例如处理
    }
    
    public static int multiply(int a, int b) {
        return a * b;
    }
    
    public static double divide(int a, int b) {
        if(b == 0) {
            throw new IllegalArgumentException("除数不能为零");
        }
        return (double) a / b;
    }
}