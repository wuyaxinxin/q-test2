/**
 * 规则验证器类
 * 负责验证棋子移动是否符合象棋规则
 * 
 * 验证流程:
 * 1. 检查起点和终点位置是否合法
 * 2. 检查起点是否有棋子且属于当前玩家
 * 3. 检查终点是否为己方棋子
 * 4. 根据棋子类型验证移动规则
 * 
 * @author Chess Game
 * @version 1.0
 */
public class RuleValidator {
    /** 棋盘引用 */
    private Board board;
    
    /**
     * 构造规则验证器
     * 
     * @param board 要验证的棋盘
     */
    public RuleValidator(Board board) {
        this.board = board;
    }
    
    /**
     * 验证移动是否合法
     * 
     * @param fromX 起点横坐标
     * @param fromY 起点纵坐标
     * @param toX 终点横坐标
     * @param toY 终点纵坐标
     * @param currentSide 当前玩家阵营
     * @return 如果移动合法返回null,否则返回错误信息
     */
    public String validateMove(int fromX, int fromY, int toX, int toY, Side currentSide) {
        // 检查位置是否在棋盘范围内
        if (!board.isValidPosition(fromX, fromY)) {
            return "起点位置超出边界";
        }
        if (!board.isValidPosition(toX, toY)) {
            return "终点位置超出边界";
        }
        
        // 检查起点是否有棋子
        Piece fromPiece = board.getPiece(fromX, fromY);
        if (fromPiece == null) {
            return "起点位置没有棋子";
        }
        
        // 检查是否是当前玩家的棋子
        if (fromPiece.getSide() != currentSide) {
            return "这不是你的棋子";
        }
        
        // 检查终点是否是己方棋子
        Piece toPiece = board.getPiece(toX, toY);
        if (toPiece != null && toPiece.getSide() == currentSide) {
            return "不能吃己方棋子";
        }
        
        // 根据棋子类型验证移动规则
        return validatePieceMove(fromPiece, fromX, fromY, toX, toY);
    }
    
    /**
     * 根据棋子类型验证移动规则
     * 
     * @param piece 要移动的棋子
     * @param fromX 起点横坐标
     * @param fromY 起点纵坐标
     * @param toX 终点横坐标
     * @param toY 终点纵坐标
     * @return 如果移动合法返回null,否则返回错误信息
     */
    private String validatePieceMove(Piece piece, int fromX, int fromY, int toX, int toY) {
        switch (piece.getType()) {
            case KING:
                return validateKingMove(piece, fromX, fromY, toX, toY);
            case GUARD:
                return validateGuardMove(piece, fromX, fromY, toX, toY);
            case ELEPHANT:
                return validateElephantMove(piece, fromX, fromY, toX, toY);
            case ROOK:
                return validateRookMove(fromX, fromY, toX, toY);
            case KNIGHT:
                return validateKnightMove(fromX, fromY, toX, toY);
            case CANNON:
                return validateCannonMove(fromX, fromY, toX, toY);
            case PAWN:
                return validatePawnMove(piece, fromX, fromY, toX, toY);
            default:
                return "未知棋子类型";
        }
    }
    
    /**
     * 验证将/帅的移动规则
     * 只能在九宫格内移动,每次一步,横竖方向
     */
    private String validateKingMove(Piece piece, int fromX, int fromY, int toX, int toY) {
        // 检查是否在九宫格内
        boolean inPalace = false;
        if (piece.getSide() == Side.RED) {
            // 红方九宫格: x[3-5], y[7-9]
            inPalace = toX >= 3 && toX <= 5 && toY >= 7 && toY <= 9;
        } else {
            // 黑方九宫格: x[3-5], y[0-2]
            inPalace = toX >= 3 && toX <= 5 && toY >= 0 && toY <= 2;
        }
        
        if (!inPalace) {
            return "将帅不能离开九宫格";
        }
        
        // 检查是否只移动一步且是横竖方向
        int dx = Math.abs(toX - fromX);
        int dy = Math.abs(toY - fromY);
        if ((dx == 1 && dy == 0) || (dx == 0 && dy == 1)) {
            return null; // 合法移动
        }
        
        return "将帅只能走一步,且只能横竖移动";
    }
    
    /**
     * 验证士的移动规则
     * 只能在九宫格内沿斜线移动,每次一步
     */
    private String validateGuardMove(Piece piece, int fromX, int fromY, int toX, int toY) {
        // 检查是否在九宫格内
        boolean inPalace = false;
        if (piece.getSide() == Side.RED) {
            inPalace = toX >= 3 && toX <= 5 && toY >= 7 && toY <= 9;
        } else {
            inPalace = toX >= 3 && toX <= 5 && toY >= 0 && toY <= 2;
        }
        
        if (!inPalace) {
            return "士不能离开九宫格";
        }
        
        // 检查是否沿斜线移动一步
        int dx = Math.abs(toX - fromX);
        int dy = Math.abs(toY - fromY);
        if (dx == 1 && dy == 1) {
            return null; // 合法移动
        }
        
        return "士只能沿斜线走一步";
    }
    
    /**
     * 验证象/相的移动规则
     * 沿田字对角线移动,不能过河,移动路径中心不能有棋子
     */
    private String validateElephantMove(Piece piece, int fromX, int fromY, int toX, int toY) {
        // 检查是否过河
        if (piece.getSide() == Side.RED) {
            if (toY < 5) {
                return "相不能过河";
            }
        } else {
            if (toY > 4) {
                return "象不能过河";
            }
        }
        
        // 检查是否走田字
        int dx = toX - fromX;
        int dy = toY - fromY;
        if (Math.abs(dx) != 2 || Math.abs(dy) != 2) {
            return "象/相必须走田字";
        }
        
        // 检查田字中心是否有棋子(塞象眼)
        int centerX = fromX + dx / 2;
        int centerY = fromY + dy / 2;
        if (board.getPiece(centerX, centerY) != null) {
            return "象眼被塞,不能移动";
        }
        
        return null; // 合法移动
    }
    
    /**
     * 验证车的移动规则
     * 横竖直线移动,路径上不能有其他棋子
     */
    private String validateRookMove(int fromX, int fromY, int toX, int toY) {
        // 检查是否横竖移动
        if (fromX != toX && fromY != toY) {
            return "车只能横竖移动";
        }
        
        // 检查路径上是否有其他棋子
        if (fromX == toX) {
            // 纵向移动
            int minY = Math.min(fromY, toY);
            int maxY = Math.max(fromY, toY);
            for (int y = minY + 1; y < maxY; y++) {
                if (board.getPiece(fromX, y) != null) {
                    return "车的移动路径上有其他棋子";
                }
            }
        } else {
            // 横向移动
            int minX = Math.min(fromX, toX);
            int maxX = Math.max(fromX, toX);
            for (int x = minX + 1; x < maxX; x++) {
                if (board.getPiece(x, fromY) != null) {
                    return "车的移动路径上有其他棋子";
                }
            }
        }
        
        return null; // 合法移动
    }
    
    /**
     * 验证马的移动规则
     * 走日字,移动方向的直线上不能有棋子(蹩马腿)
     */
    private String validateKnightMove(int fromX, int fromY, int toX, int toY) {
        int dx = Math.abs(toX - fromX);
        int dy = Math.abs(toY - fromY);
        
        // 检查是否走日字
        if (!((dx == 2 && dy == 1) || (dx == 1 && dy == 2))) {
            return "马必须走日字";
        }
        
        // 检查是否蹩马腿
        int blockX, blockY;
        if (dx == 2) {
            // 横向走两步
            blockX = fromX + (toX - fromX) / 2;
            blockY = fromY;
        } else {
            // 纵向走两步
            blockX = fromX;
            blockY = fromY + (toY - fromY) / 2;
        }
        
        if (board.getPiece(blockX, blockY) != null) {
            return "马腿被蹩,不能移动";
        }
        
        return null; // 合法移动
    }
    
    /**
     * 验证炮的移动规则
     * 横竖直线移动,吃子时必须隔一个棋子
     */
    private String validateCannonMove(int fromX, int fromY, int toX, int toY) {
        // 检查是否横竖移动
        if (fromX != toX && fromY != toY) {
            return "炮只能横竖移动";
        }
        
        // 计算路径上的棋子数量
        int pieceCount = 0;
        if (fromX == toX) {
            // 纵向移动
            int minY = Math.min(fromY, toY);
            int maxY = Math.max(fromY, toY);
            for (int y = minY + 1; y < maxY; y++) {
                if (board.getPiece(fromX, y) != null) {
                    pieceCount++;
                }
            }
        } else {
            // 横向移动
            int minX = Math.min(fromX, toX);
            int maxX = Math.max(fromX, toX);
            for (int x = minX + 1; x < maxX; x++) {
                if (board.getPiece(x, fromY) != null) {
                    pieceCount++;
                }
            }
        }
        
        Piece toPiece = board.getPiece(toX, toY);
        if (toPiece == null) {
            // 移动时路径上不能有棋子
            if (pieceCount > 0) {
                return "炮移动时路径上不能有其他棋子";
            }
        } else {
            // 吃子时必须隔一个棋子
            if (pieceCount != 1) {
                return "炮吃子时必须隔一个棋子";
            }
        }
        
        return null; // 合法移动
    }
    
    /**
     * 验证兵/卒的移动规则
     * 未过河只能向前,过河后可左右前,每次只能走一步,不能后退
     */
    private String validatePawnMove(Piece piece, int fromX, int fromY, int toX, int toY) {
        int dx = Math.abs(toX - fromX);
        int dy = toY - fromY;
        
        // 检查是否只移动一步
        if ((dx == 0 && Math.abs(dy) == 1) || (dx == 1 && dy == 0)) {
            // 合法的一步移动
        } else {
            return "兵/卒只能走一步";
        }
        
        // 判断是否过河
        boolean crossed = false;
        if (piece.getSide() == Side.RED) {
            // 红方:过河是指到达y<5的区域
            crossed = fromY < 5;
            // 检查是否后退
            if (dy < 0) {
                return "兵不能后退";
            }
        } else {
            // 黑方:过河是指到达y>4的区域
            crossed = fromY > 4;
            // 检查是否后退
            if (dy > 0) {
                return "卒不能后退";
            }
        }
        
        // 未过河只能向前
        if (!crossed && dx != 0) {
            return "兵/卒未过河不能横向移动";
        }
        
        return null; // 合法移动
    }
}
