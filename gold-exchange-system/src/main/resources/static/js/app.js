// 获取当前汇率并更新页面
function updateGoldRate() {
    fetch('/api/rate')
        .then(response => response.json())
        .then(data => {
            const rateElements = document.querySelectorAll('.gold-rate');
            rateElements.forEach(element => {
                element.textContent = '$' + data.toFixed(2);
            });
        })
        .catch(error => {
            console.error('Error fetching gold rate:', error);
        });
}

// 页面加载完成后更新汇率
document.addEventListener('DOMContentLoaded', function() {
    // 如果页面中有显示汇率的部分，可以自动更新
    updateGoldRate();
    
    // 每分钟自动更新一次汇率（模拟实时更新）
    setInterval(updateGoldRate, 60000);
});

// 表单验证
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const amountInput = document.getElementById('amount');
            const amount = parseFloat(amountInput.value);
            
            if (isNaN(amount) || amount <= 0) {
                e.preventDefault();
                alert('请输入有效的金额');
                return false;
            }
        });
    }
});