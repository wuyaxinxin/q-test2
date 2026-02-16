# 始终生效

from flask import Flask, render_template, jsonify
from data_generator import generate_trade_data

app = Flask(__name__)


@app.route('/')
def index():
    """
    主页路由
    
    渲染全球贸易走势展示页面
    """
    return render_template('index.html')


@app.route('/api/trade-data')
def get_trade_data():
    """
    API路由 - 获取贸易数据
    
    返回JSON格式的全球贸易进出口数据
    """
    data = generate_trade_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
