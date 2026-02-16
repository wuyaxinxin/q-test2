// 始终生效
// 模型决策

/**
 * Example类 - 一个简单的示例Java类
 * 提供基本的功能演示
 */
public class Example {
    private String name;
    private int value;

    /**
     * 默认构造函数
     */
    public Example() {
        this.name = "Default";
        this.value = 0;
    }

    /**
     * 带参数的构造函数
     * @param name 名称
     * @param value 数值
     */
    public Example(String name, int value) {
        this.name = name;
        this.value = value;
    }

    /**
     * 获取名称
     * @return 当前对象的名称
     */
    public String getName() {
        return name;
    }

    /**
     * 设置名称
     * @param name 要设置的名称
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取数值
     * @return 当前对象的数值
     */
    public int getValue() {
        return value;
    }

    /**
     * 设置数值
     * @param value 要设置的数值
     */
    public void setValue(int value) {
        this.value = value;
    }

    /**
     * 计算数值的平方
     * @return 数值的平方
     */
    public int square() {
        return value * value;
    }

    /**
     * 打印对象信息
     */
    public void printInfo() {
        System.out.println("Name: " + name + ", Value: " + value);
    }

    /**
     * 主方法 - 程序入口
     * @param args 命令行参数
     */
    public static void main(String[] args) {
        Example example = new Example("Test", 5);
        example.printInfo();
        System.out.println("Square of value: " + example.square());
    }
}
