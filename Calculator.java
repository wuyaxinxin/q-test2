/**
 * Calculator类 - 提供基本的数学运算功能
 * 
 * @author Auto Generated
 * @version 1.0
 */
public class Calculator {
    
    /**
     * 加法运算
     * 
     * @param a 第一个操作数
     * @param b 第二个操作数
     * @return 两数之和
     */
    public double add(double a, double b) {
        return a + b;
    }
    
    /**
     * 减法运算
     * 
     * @param a 被减数
     * @param b 减数
     * @return 两数之差
     */
    public double subtract(double a, double b) {
        return a - b;
    }
    
    /**
     * 乘法运算
     * 
     * @param a 第一个操作数
     * @param b 第二个操作数
     * @return 两数之积
     */
    public double multiply(double a, double b) {
        return a * b;
    }
    
    /**
     * 除法运算
     * 
     * @param a 被除数
     * @param b 除数
     * @return 两数之商
     * @throws ArithmeticException 当除数为0时抛出
     */
    public double divide(double a, double b) throws ArithmeticException {
        if (b == 0) {
            throw new ArithmeticException("除数不能为0");
        }
        return a / b;
    }
    
    /**
     * 求幂运算
     * 
     * @param base 底数
     * @param exponent 指数
     * @return base的exponent次幂
     */
    public double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }
    
    /**
     * 求平方根
     * 
     * @param number 要求平方根的数
     * @return 平方根结果
     * @throws IllegalArgumentException 当输入负数时抛出
     */
    public double sqrt(double number) throws IllegalArgumentException {
        if (number < 0) {
            throw new IllegalArgumentException("不能对负数求平方根");
        }
        return Math.sqrt(number);
    }
    
    /**
     * 求绝对值
     * 
     * @param number 输入数值
     * @return 绝对值
     */
    public double abs(double number) {
        return Math.abs(number);
    }
    
    /**
     * 求最大值
     * 
     * @param a 第一个数
     * @param b 第二个数
     * @return 两数中的最大值
     */
    public double max(double a, double b) {
        return Math.max(a, b);
    }
    
    /**
     * 求最小值
     * 
     * @param a 第一个数
     * @param b 第二个数
     * @return 两数中的最小值
     */
    public double min(double a, double b) {
        return Math.min(a, b);
    }
    
    /**
     * 主方法 - 演示计算器功能
     * 
     * @param args 命令行参数
     */
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        
        System.out.println("=== 计算器演示 ===");
        System.out.println("10 + 5 = " + calc.add(10, 5));
        System.out.println("10 - 5 = " + calc.subtract(10, 5));
        System.out.println("10 * 5 = " + calc.multiply(10, 5));
        System.out.println("10 / 5 = " + calc.divide(10, 5));
        System.out.println("2 ^ 3 = " + calc.power(2, 3));
        System.out.println("√16 = " + calc.sqrt(16));
        System.out.println("|−5| = " + calc.abs(-5));
        System.out.println("max(10, 5) = " + calc.max(10, 5));
        System.out.println("min(10, 5) = " + calc.min(10, 5));
        
        // 测试异常处理
        try {
            System.out.println("10 / 0 = " + calc.divide(10, 0));
        } catch (ArithmeticException e) {
            System.out.println("错误: " + e.getMessage());
        }
        
        try {
            System.out.println("√−1 = " + calc.sqrt(-1));
        } catch (IllegalArgumentException e) {
            System.out.println("错误: " + e.getMessage());
        }
    }
}
