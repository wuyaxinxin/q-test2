/**
 * 棋子类
 * 表示棋盘上的一个棋子,包含类型、阵营和显示符号
 * 
 * 使用示例:
 * <pre>
 * Piece redKing = new Piece(PieceType.KING, Side.RED);
 * System.out.println(redKing.getSymbol()); // 输出: 帅
 * </pre>
 * 
 * @author Chess Game
 * @version 1.0
 */
public class Piece {
    /** 棋子类型 */
    private final PieceType type;
    /** 棋子所属阵营 */
    private final Side side;
    
    /**
     * 构造一个棋子
     * 
     * @param type 棋子类型,不能为null
     * @param side 棋子阵营,不能为null
     */
    public Piece(PieceType type, Side side) {
        this.type = type;
        this.side = side;
    }
    
    /**
     * 获取棋子类型
     * 
     * @return 棋子类型
     */
    public PieceType getType() {
        return type;
    }
    
    /**
     * 获取棋子阵营
     * 
     * @return 棋子阵营(RED或BLACK)
     */
    public Side getSide() {
        return side;
    }
    
    /**
     * 获取棋子的显示符号
     * 根据棋子类型和阵营返回对应的汉字符号
     * 
     * @return 用于控制台显示的汉字符号
     */
    public String getSymbol() {
        // 根据阵营和类型返回对应的汉字
        if (side == Side.RED) {
            // 红方棋子
            switch (type) {
                case KING: return "帅";
                case GUARD: return "仕";
                case ELEPHANT: return "相";
                case ROOK: return "車";
                case KNIGHT: return "馬";
                case CANNON: return "炮";
                case PAWN: return "兵";
                default: return "?";
            }
        } else {
            // 黑方棋子
            switch (type) {
                case KING: return "将";
                case GUARD: return "士";
                case ELEPHANT: return "象";
                case ROOK: return "车";
                case KNIGHT: return "马";
                case CANNON: return "砲";
                case PAWN: return "卒";
                default: return "?";
            }
        }
    }
}
