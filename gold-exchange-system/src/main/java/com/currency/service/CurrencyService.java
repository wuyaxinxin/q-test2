package com.currency.service;

import org.springframework.stereotype.Service;

@Service
public class CurrencyService {
    
    // Mock gold price per ounce in USD (would normally come from an API)
    private Double goldPricePerOunce = 1800.0;
    
    public Double convertUsdToGold(Double usdAmount) {
        if (usdAmount == null || usdAmount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        return usdAmount / goldPricePerOunce; // Convert USD to ounces of gold
    }
    
    public Double convertGoldToUsd(Double goldOunces) {
        if (goldOunces == null || goldOunces <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        return goldOunces * goldPricePerOunce; // Convert ounces of gold to USD
    }
    
    public Double getGoldPricePerOunce() {
        return goldPricePerOunce;
    }
    
    public void updateGoldPrice(Double newPrice) {
        if (newPrice > 0) {
            this.goldPricePerOunce = newPrice;
        }
    }
}