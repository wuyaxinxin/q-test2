// 始终生效
// 自由万岁

import java.text.DecimalFormat;

public class EqualPrincipalCalculator {
    private double principal;
    private double annualRate;
    private int months;
    private DecimalFormat df;
    
    public EqualPrincipalCalculator(double principal, double annualRate, int months) {
        this.principal = principal;
        this.annualRate = annualRate;
        this.months = months;
        this.df = new DecimalFormat("#,##0.00");
    }
    
    public double calculateMonthlyPrincipal() {
        return principal / months;
    }
    
    public double calculateMonthlyInterest(int month) {
        if (month < 1 || month > months) {
            throw new IllegalArgumentException("月份必须在1到" + months + "之间");
        }
        double monthlyRate = annualRate / 12;
        double remainingPrincipal = principal - (month - 1) * calculateMonthlyPrincipal();
        return remainingPrincipal * monthlyRate;
    }
    
    public double calculateMonthlyPayment(int month) {
        return calculateMonthlyPrincipal() + calculateMonthlyInterest(month);
    }
    
    public double calculateTotalInterest() {
        double totalInterest = 0;
        for (int i = 1; i <= months; i++) {
            totalInterest += calculateMonthlyInterest(i);
        }
        return totalInterest;
    }
    
    public String[][] generateRepaymentSchedule() {
        String[][] schedule = new String[months + 1][5];
        
        schedule[0][0] = "期数";
        schedule[0][1] = "每月应还本金";
        schedule[0][2] = "每月应还利息";
        schedule[0][3] = "每月还款总额";
        schedule[0][4] = "剩余本金";
        
        double monthlyPrincipal = calculateMonthlyPrincipal();
        double remainingPrincipal = principal;
        
        for (int i = 1; i <= months; i++) {
            double monthlyInterest = calculateMonthlyInterest(i);
            double monthlyPayment = monthlyPrincipal + monthlyInterest;
            remainingPrincipal -= monthlyPrincipal;
            
            schedule[i][0] = String.valueOf(i);
            schedule[i][1] = df.format(monthlyPrincipal);
            schedule[i][2] = df.format(monthlyInterest);
            schedule[i][3] = df.format(monthlyPayment);
            schedule[i][4] = df.format(Math.max(0, remainingPrincipal));
        }
        
        return schedule;
    }
    
    public void printRepaymentSchedule() {
        String[][] schedule = generateRepaymentSchedule();
        
        System.out.println("\n========== 等额本金还款计划表 ==========");
        System.out.println(String.format("%-8s %-15s %-15s %-15s %-15s", 
            schedule[0][0], schedule[0][1], schedule[0][2], schedule[0][3], schedule[0][4]));
        System.out.println("=".repeat(75));
        
        for (int i = 1; i <= Math.min(3, months); i++) {
            System.out.println(String.format("%-8s %-15s %-15s %-15s %-15s", 
                schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], schedule[i][4]));
        }
        
        if (months > 6) {
            System.out.println("...");
        }
        
        for (int i = Math.max(4, months - 2); i <= months; i++) {
            System.out.println(String.format("%-8s %-15s %-15s %-15s %-15s", 
                schedule[i][0], schedule[i][1], schedule[i][2], schedule[i][3], schedule[i][4]));
        }
        
        System.out.println("=".repeat(75));
        System.out.println("总利息: " + df.format(calculateTotalInterest()) + " 元");
        System.out.println("还款总额: " + df.format(principal + calculateTotalInterest()) + " 元");
    }
    
    public static void main(String[] args) {
        System.out.println("========== 等额本金计算器示例 ==========\n");
        
        double loanAmount = 1000000;
        double yearRate = 0.049;
        int loanMonths = 360;
        
        System.out.println("贷款信息:");
        System.out.println("  贷款本金: " + loanAmount + " 元");
        System.out.println("  年利率: " + (yearRate * 100) + "%");
        System.out.println("  还款期限: " + loanMonths + " 个月 (" + (loanMonths / 12) + " 年)");
        
        EqualPrincipalCalculator calculator = new EqualPrincipalCalculator(loanAmount, yearRate, loanMonths);
        
        DecimalFormat df = new DecimalFormat("#,##0.00");
        System.out.println("\n关键数据:");
        System.out.println("  每月固定还本金: " + df.format(calculator.calculateMonthlyPrincipal()) + " 元");
        System.out.println("  首月还款总额: " + df.format(calculator.calculateMonthlyPayment(1)) + " 元");
        System.out.println("  末月还款总额: " + df.format(calculator.calculateMonthlyPayment(loanMonths)) + " 元");
        System.out.println("  总利息: " + df.format(calculator.calculateTotalInterest()) + " 元");
        System.out.println("  还款总额: " + df.format(loanAmount + calculator.calculateTotalInterest()) + " 元");
        
        calculator.printRepaymentSchedule();
    }
}
