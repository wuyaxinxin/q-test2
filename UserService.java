// 自由万岁
// 始终生效

/**
 * 用户服务类
 * 提供用户管理的基本功能
 */
public class UserService {
    private String serviceName;
    private int maxUsers;
    
    /**
     * 构造函数
     * @param serviceName 服务名称
     * @param maxUsers 最大用户数
     */
    public UserService(String serviceName, int maxUsers) {
        this.serviceName = serviceName;
        this.maxUsers = maxUsers;
    }
    
    /**
     * 获取服务名称
     * @return 服务名称
     */
    public String getServiceName() {
        return serviceName;
    }
    
    /**
     * 设置服务名称
     * @param serviceName 服务名称
     */
    public void setServiceName(String serviceName) {
        this.serviceName = serviceName;
    }
    
    /**
     * 获取最大用户数
     * @return 最大用户数
     */
    public int getMaxUsers() {
        return maxUsers;
    }
    
    /**
     * 设置最大用户数
     * @param maxUsers 最大用户数
     */
    public void setMaxUsers(int maxUsers) {
        this.maxUsers = maxUsers;
    }
    
    /**
     * 添加用户
     * @param username 用户名
     * @return 是否添加成功
     */
    public boolean addUser(String username) {
        System.out.println("添加用户: " + username);
        return true;
    }
    
    /**
     * 删除用户
     * @param username 用户名
     * @return 是否删除成功
     */
    public boolean removeUser(String username) {
        System.out.println("删除用户: " + username);
        return true;
    }
    
    /**
     * 显示服务信息
     */
    public void displayInfo() {
        System.out.println("服务名称: " + serviceName);
        System.out.println("最大用户数: " + maxUsers);
    }
}
