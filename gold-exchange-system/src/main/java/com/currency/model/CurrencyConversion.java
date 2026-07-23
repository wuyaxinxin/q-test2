package com.currency.model;

import javax.validation.constraints.DecimalMin;
import javax.validation.constraints.NotBlank;

public class CurrencyConversion {
    
    @DecimalMin(value = "0.0", message = "Amount must be positive")
    private Double amount;
    
    @NotBlank(message = "From currency is required")
    private String fromCurrency;
    
    @NotBlank(message = "To currency is required")
    private String toCurrency;
    
    private Double result;
    
    // Default constructor
    public CurrencyConversion() {}
    
    // Constructor with parameters
    public CurrencyConversion(Double amount, String fromCurrency, String toCurrency, Double result) {
        this.amount = amount;
        this.fromCurrency = fromCurrency;
        this.toCurrency = toCurrency;
        this.result = result;
    }
    
    // Getters and setters
    public Double getAmount() {
        return amount;
    }
    
    public void setAmount(Double amount) {
        this.amount = amount;
    }
    
    public String getFromCurrency() {
        return fromCurrency;
    }
    
    public void setFromCurrency(String fromCurrency) {
        this.fromCurrency = fromCurrency;
    }
    
    public String getToCurrency() {
        return toCurrency;
    }
    
    public void setToCurrency(String toCurrency) {
        this.toCurrency = toCurrency;
    }
    
    public Double getResult() {
        return result;
    }
    
    public void setResult(Double result) {
        this.result = result;
    }
}