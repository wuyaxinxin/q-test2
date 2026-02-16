/**
 * 棋盘管理器类
 * 负责维护棋盘状态,初始化棋盘,执行棋子移动
 * 
 * 棋盘坐标系:
 * - 横坐标x: 0-8 (从左到右)
 * - 纵坐标y: 0-9 (从上到下,黑方在上,红方在下)
 * 
 * 使用示例:
 * <pre>
 * Board board = new Board();
 * board.initialize();
 * board.display();
 * </pre>
 * 
 * @author Chess Game
 * @version 1.0
 */
public class Board {
    /** 棋盘宽度(横向) */
    private static final int WIDTH = 9;
    /** 棋盘高度(纵向) */
    private static final int HEIGHT = 10;
    
    /** 棋盘二维数组,存储每个位置的棋子 */
    private Piece[][] grid;
    
    /**
     * 构造棋盘
     * 创建空棋盘,需要调用initialize()方法初始化棋子
     */
    public Board() {
        grid = new Piece[WIDTH][HEIGHT];
    }
    
    /**
     * 初始化棋盘
     * 按照标准象棋规则摆放初始棋子位置
     * 黑方在上(y=0),红方在下(y=9)
     */
    public void initialize() {
        // 清空棋盘
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                grid[x][y] = null;
            }
        }
        
        // 黑方棋子 (y=0-3)
        grid[0][0] = new Piece(PieceType.ROOK, Side.BLACK);
        grid[1][0] = new Piece(PieceType.KNIGHT, Side.BLACK);
        grid[2][0] = new Piece(PieceType.ELEPHANT, Side.BLACK);
        grid[3][0] = new Piece(PieceType.GUARD, Side.BLACK);
        grid[4][0] = new Piece(PieceType.KING, Side.BLACK);
        grid[5][0] = new Piece(PieceType.GUARD, Side.BLACK);
        grid[6][0] = new Piece(PieceType.ELEPHANT, Side.BLACK);
        grid[7][0] = new Piece(PieceType.KNIGHT, Side.BLACK);
        grid[8][0] = new Piece(PieceType.ROOK, Side.BLACK);
        
        grid[1][2] = new Piece(PieceType.CANNON, Side.BLACK);
        grid[7][2] = new Piece(PieceType.CANNON, Side.BLACK);
        
        grid[0][3] = new Piece(PieceType.PAWN, Side.BLACK);
        grid[2][3] = new Piece(PieceType.PAWN, Side.BLACK);
        grid[4][3] = new Piece(PieceType.PAWN, Side.BLACK);
        grid[6][3] = new Piece(PieceType.PAWN, Side.BLACK);
        grid[8][3] = new Piece(PieceType.PAWN, Side.BLACK);
        
        // 红方棋子 (y=6-9)
        grid[0][6] = new Piece(PieceType.PAWN, Side.RED);
        grid[2][6] = new Piece(PieceType.PAWN, Side.RED);
        grid[4][6] = new Piece(PieceType.PAWN, Side.RED);
        grid[6][6] = new Piece(PieceType.PAWN, Side.RED);
        grid[8][6] = new Piece(PieceType.PAWN, Side.RED);
        
        grid[1][7] = new Piece(PieceType.CANNON, Side.RED);
        grid[7][7] = new Piece(PieceType.CANNON, Side.RED);
        
        grid[0][9] = new Piece(PieceType.ROOK, Side.RED);
        grid[1][9] = new Piece(PieceType.KNIGHT, Side.RED);
        grid[2][9] = new Piece(PieceType.ELEPHANT, Side.RED);
        grid[3][9] = new Piece(PieceType.GUARD, Side.RED);
        grid[4][9] = new Piece(PieceType.KING, Side.RED);
        grid[5][9] = new Piece(PieceType.GUARD, Side.RED);
        grid[6][9] = new Piece(PieceType.ELEPHANT, Side.RED);
        grid[7][9] = new Piece(PieceType.KNIGHT, Side.RED);
        grid[8][9] = new Piece(PieceType.ROOK, Side.RED);
    }
    
    /**
     * 获取指定位置的棋子
     * 
     * @param x 横坐标(0-8)
     * @param y 纵坐标(0-9)
     * @return 该位置的棋子,如果位置为空则返回null
     */
    public Piece getPiece(int x, int y) {
        if (!isValidPosition(x, y)) {
            return null;
        }
        return grid[x][y];
    }
    
    /**
     * 移动棋子
     * 将起点位置的棋子移动到终点位置,不进行规则验证
     * 
     * @param fromX 起点横坐标
     * @param fromY 起点纵坐标
     * @param toX 终点横坐标
     * @param toY 终点纵坐标
     */
    public void movePiece(int fromX, int fromY, int toX, int toY) {
        Piece piece = grid[fromX][fromY];
        grid[toX][toY] = piece;
        grid[fromX][fromY] = null;
    }
    
    /**
     * 检查位置是否在棋盘范围内
     * 
     * @param x 横坐标
     * @param y 纵坐标
     * @return 如果位置合法返回true,否则返回false
     */
    public boolean isValidPosition(int x, int y) {
        return x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT;
    }
    
    /**
     * 显示棋盘
     * 在控制台以文本形式显示当前棋盘状态
     */
    public void display() {
        // 打印列坐标
        System.out.print("  ");
        for (int x = 0; x < WIDTH; x++) {
            System.out.print(x + " ");
        }
        System.out.println();
        
        // 打印棋盘内容
        for (int y = 0; y < HEIGHT; y++) {
            // 打印行坐标
            System.out.print(y + " ");
            
            // 打印每个位置的棋子或空位
            for (int x = 0; x < WIDTH; x++) {
                Piece piece = grid[x][y];
                if (piece != null) {
                    System.out.print(piece.getSymbol() + " ");
                } else {
                    System.out.print("┼ ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }
    
    /**
     * 检查某方的将帅是否还在棋盘上
     * 用于判断游戏是否结束
     * 
     * @param side 要检查的阵营
     * @return 如果该方将帅存在返回true,否则返回false
     */
    public boolean hasKing(Side side) {
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                Piece piece = grid[x][y];
                if (piece != null && piece.getType() == PieceType.KING && piece.getSide() == side) {
                    return true;
                }
            }
        }
        return false;
    }
}
