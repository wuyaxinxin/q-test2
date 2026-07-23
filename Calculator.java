/**
 * 计算器类，提供基本的数学运算功能
 * 包括加法、减法、乘法和除法运算
 */
public class Calculator {
    /**
     * 程序入口方法，演示计算器的基本运算功能
     * @param args 命令行参数（未使用）
     */
    public static void main(String[] args) {

        int num1 = 10;
        int num2 = 5;
        
        System.out.println("数字1: " + num1);
        System.out.println("数字2: " + num2);
        
        System.out.println("加法结果: " + add(num1, num2));
        System.out.println("减法结果: " + subtract(num1, num2));
        System.out.println("乘法结果: " + multiply(num1, num2));
        System.out.println("除法结果: " + divide(num1, num2));
    }
    
    /**
     * 加法运算
     * @param a 第一个操作数
     * @param b 第二个操作数
     * @return 两数之和
     */
    public static int add(int a, int b) {
        return a + b;
    }
    
    /**
     * 减法运算
     * @param a 被减数
     * @param b 减数
     * @return 两数之差
     */
    public static int subtract(int a, int b) {
        return a - b;
        // 可以添加更多逻辑，例如处理
    }
    
    /**
     * 乘法运算
     * @param a 第一个操作数
     * @param b 第二个操作数
     * @return 两数之积
     */
    public static int multiply(int a, int b) {
        return a * b;
    }
    
    /**
     * 除法运算
     * @param a 被除数
     * @param b 除数
     * @return 两数之商（浮点数结果）
     * @throws IllegalArgumentException 当除数为零时抛出
     */
    public static double divide(int a, int b) {
        if(b == 0) {
            throw new IllegalArgumentException("除数不能为零");
        }
        return (double) a / b;
    }
}