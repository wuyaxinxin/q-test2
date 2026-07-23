package com.currency.controller;

import com.currency.model.CurrencyConversion;
import com.currency.service.CurrencyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class CurrencyController {
    
    @Autowired
    private CurrencyService currencyService;
    
    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("conversion", new CurrencyConversion());
        model.addAttribute("goldPrice", currencyService.getGoldPricePerOunce());
        return "index";
    }
    
    @PostMapping("/convert")
    public String convertCurrency(@ModelAttribute CurrencyConversion conversion, Model model) {
        Double result = 0.0;
        
        if ("USD".equals(conversion.getFromCurrency()) && "GOLD".equals(conversion.getToCurrency())) {
            result = currencyService.convertUsdToGold(conversion.getAmount());
            conversion.setToCurrency("Gold Ounces");
        } else if ("GOLD".equals(conversion.getFromCurrency()) && "USD".equals(conversion.getToCurrency())) {
            result = currencyService.convertGoldToUsd(conversion.getAmount());
            conversion.setToCurrency("USD");
        }
        
        conversion.setResult(result);
        
        model.addAttribute("conversion", conversion);
        model.addAttribute("goldPrice", currencyService.getGoldPricePerOunce());
        
        return "result";
    }
    
    @ResponseBody
    @GetMapping("/api/rate")
    public Double getGoldRate() {
        return currencyService.getGoldPricePerOunce();
    }
}