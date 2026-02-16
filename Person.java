// 始终生效
// 自由万岁

/**
 * Person JavaBean类
 * 包含基本的用户信息属性
 */
public class Person {
    private String name;
    private int age;
    private String email;
    private String address;

    /**
     * 无参构造方法
     */
    public Person() {
    }

    /**
     * 全参构造方法
     */
    public Person(String name, int age, String email, String address) {
        this.name = name;
        this.age = age;
        this.email = email;
        this.address = address;
    }

    /**
     * 获取姓名
     */
    public String getName() {
        return name;
    }

    /**
     * 设置姓名
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取年龄
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置年龄
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取邮箱
     */
    public String getEmail() {
        return email;
    }

    /**
     * 设置邮箱
     */
    public void setEmail(String email) {
        this.email = email;
    }

    /**
     * 获取地址
     */
    public String getAddress() {
        return address;
    }

    /**
     * 设置地址
     */
    public void setAddress(String address) {
        this.address = address;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", email='" + email + '\'' +
                ", address='" + address + '\'' +
                '}';
    }
}
