package com.currency.service;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class CurrencyServiceTest {

    @Test
    void testConvertUsdToGold() {
        CurrencyService service = new CurrencyService();
        
        // 测试正常的美元转黄金
        Double result = service.convertUsdToGold(1800.0);
        assertEquals(1.0, result, 0.001); // 1800美元应等于1盎司黄金(按$1800/盎司的价格)
        
        // 测试不同金额
        result = service.convertUsdToGold(900.0);
        assertEquals(0.5, result, 0.001); // 900美元应等于0.5盎司黄金
    }

    @Test
    void testConvertGoldToUsd() {
        CurrencyService service = new CurrencyService();
        
        // 测试正常的黄金转美元
        Double result = service.convertGoldToUsd(1.0);
        assertEquals(1800.0, result, 0.001); // 1盎司黄金应等于1800美元
        
        // 测试不同数量
        result = service.convertGoldToUsd(2.0);
        assertEquals(3600.0, result, 0.001); // 2盎司黄金应等于3600美元
    }

    @Test
    void testInvalidInputs() {
        CurrencyService service = new CurrencyService();
        
        // 测试负数输入
        assertThrows(IllegalArgumentException.class, () -> {
            service.convertUsdToGold(-100.0);
        });
        
        assertThrows(IllegalArgumentException.class, () -> {
            service.convertGoldToUsd(-1.0);
        });
        
        // 测试零值输入
        assertThrows(IllegalArgumentException.class, () -> {
            service.convertUsdToGold(0.0);
        });
    }
    
    @Test
    void testGetAndUpdateGoldPrice() {
        CurrencyService service = new CurrencyService();
        
        // 测试获取默认金价
        Double defaultPrice = service.getGoldPricePerOunce();
        assertEquals(1800.0, defaultPrice, 0.001);
        
        // 测试更新金价
        service.updateGoldPrice(2000.0);
        Double newPrice = service.getGoldPricePerOunce();
        assertEquals(2000.0, newPrice, 0.001);
        
        // 测试无效价格不会更新
        service.updateGoldPrice(-100.0);
        assertEquals(2000.0, service.getGoldPricePerOunce(), 0.001); // 应保持不变
    }
}