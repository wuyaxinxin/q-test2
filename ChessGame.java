import java.util.Scanner;

/**
 * 象棋游戏控制器类
 * 控制游戏主流程,协调各组件工作
 * 
 * 主要功能:
 * 1. 初始化游戏
 * 2. 显示棋盘
 * 3. 接收玩家输入
 * 4. 验证移动规则
 * 5. 执行移动
 * 6. 判断胜负
 * 7. 切换玩家
 * 
 * 使用示例:
 * <pre>
 * ChessGame game = new ChessGame();
 * game.start();
 * </pre>
 * 
 * @author Chess Game
 * @version 1.0
 */
public class ChessGame {
    /** 棋盘管理器 */
    private Board board;
    /** 规则验证器 */
    private RuleValidator validator;
    /** 当前玩家 */
    private Side currentPlayer;
    /** 输入扫描器 */
    private Scanner scanner;
    
    /**
     * 构造游戏控制器
     * 初始化棋盘、验证器和当前玩家
     */
    public ChessGame() {
        board = new Board();
        validator = new RuleValidator(board);
        currentPlayer = Side.RED; // 红方先行
        scanner = new Scanner(System.in);
    }
    
    /**
     * 启动游戏
     * 游戏主循环,包含初始化、显示、输入、验证、移动、判断胜负等步骤
     */
    public void start() {
        // 初始化棋盘
        board.initialize();
        
        // 显示游戏开始信息
        System.out.println("============================================");
        System.out.println("        欢迎来到简单象棋游戏!");
        System.out.println("============================================");
        System.out.println("规则说明:");
        System.out.println("1. 输入格式: x1,y1 x2,y2");
        System.out.println("2. 例如: 4,9 4,8 表示将(4,9)位置的棋子移动到(4,8)");
        System.out.println("3. 吃掉对方将帅即获胜");
        System.out.println("============================================");
        System.out.println();
        
        // 游戏主循环
        while (true) {
            // 显示当前棋盘
            board.display();
            
            // 显示当前玩家
            System.out.println("当前玩家: " + currentPlayer.getDisplayName());
            System.out.print("请输入移动(格式: x1,y1 x2,y2): ");
            
            // 读取输入
            String input = scanner.nextLine().trim();
            
            // 解析输入
            int[] coords = parseInput(input);
            if (coords == null) {
                System.out.println("输入格式错误,请重新输入");
                System.out.println();
                continue;
            }
            
            int fromX = coords[0];
            int fromY = coords[1];
            int toX = coords[2];
            int toY = coords[3];
            
            // 验证移动
            String error = validator.validateMove(fromX, fromY, toX, toY, currentPlayer);
            if (error != null) {
                System.out.println("移动不合法: " + error);
                System.out.println();
                continue;
            }
            
            // 执行移动
            board.movePiece(fromX, fromY, toX, toY);
            System.out.println("移动成功!");
            System.out.println();
            
            // 检查游戏是否结束
            if (!board.hasKing(Side.RED)) {
                board.display();
                System.out.println("============================================");
                System.out.println("    游戏结束! 黑方获胜!");
                System.out.println("============================================");
                break;
            }
            if (!board.hasKing(Side.BLACK)) {
                board.display();
                System.out.println("============================================");
                System.out.println("    游戏结束! 红方获胜!");
                System.out.println("============================================");
                break;
            }
            
            // 切换玩家
            currentPlayer = currentPlayer.opposite();
        }
        
        // 关闭扫描器
        scanner.close();
    }
    
    /**
     * 解析玩家输入
     * 将字符串格式"x1,y1 x2,y2"解析为坐标数组
     * 
     * @param input 用户输入字符串
     * @return 包含4个坐标的数组[fromX, fromY, toX, toY],如果解析失败返回null
     */
    private int[] parseInput(String input) {
        try {
            // 按空格分割起点和终点
            String[] parts = input.split("\\s+");
            if (parts.length != 2) {
                return null;
            }
            
            // 解析起点坐标
            String[] from = parts[0].split(",");
            if (from.length != 2) {
                return null;
            }
            int fromX = Integer.parseInt(from[0]);
            int fromY = Integer.parseInt(from[1]);
            
            // 解析终点坐标
            String[] to = parts[1].split(",");
            if (to.length != 2) {
                return null;
            }
            int toX = Integer.parseInt(to[0]);
            int toY = Integer.parseInt(to[1]);
            
            return new int[]{fromX, fromY, toX, toY};
        } catch (Exception e) {
            // 解析失败
            return null;
        }
    }
    
    /**
     * 主方法
     * 程序入口,创建游戏实例并启动
     * 
     * @param args 命令行参数(未使用)
     */
    public static void main(String[] args) {
        ChessGame game = new ChessGame();
        game.start();
    }
}
