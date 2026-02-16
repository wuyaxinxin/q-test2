/**
 * 阵营枚举类
 * 表示象棋中的红方和黑方
 * 
 * @author Chess Game
 * @version 1.0
 */
public enum Side {
    /** 红方 */
    RED,
    /** 黑方 */
    BLACK;
    
    /**
     * 获取对方阵营
     * 
     * @return 对方的阵营
     */
    public Side opposite() {
        return this == RED ? BLACK : RED;
    }
    
    /**
     * 获取阵营的显示名称
     * 
     * @return 阵营名称(红方/黑方)
     */
    public String getDisplayName() {
        return this == RED ? "红方" : "黑方";
    }
}
