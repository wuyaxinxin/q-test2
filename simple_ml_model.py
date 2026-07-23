import random
import math
from typing import List, Tuple

class SimpleMLModel:
    """
    一个简单的机器学习模型示例，演示从数据预处理到模型训练的基本流程
    """
    
    def __init__(self):
        self.weights = []
        self.bias = 0
        self.feature_means = []
        self.feature_stds = []
        self.is_trained = False
    
    def generate_sample_data(self, n_samples=1000):
        """
        生成示例数据集
        """
        print("正在生成示例数据...")
        
        # 生成特征变量
        features = []
        for i in range(n_samples):
            row = [random.gauss(0, 1) for _ in range(3)]  # 3个特征
            features.append(row)
        
        # 创建目标变量，基于特征的线性组合加上一些噪声
        targets = []
        for i in range(n_samples):
            target = 3 * features[i][0] + 2 * features[i][1] - features[i][2] + 0.5 * random.gauss(0, 1)
            targets.append(target)
        
        print(f"数据集大小: 特征矩阵 {n_samples}x3, 目标向量 {n_samples}x1")
        print(f"特征数量: 3")
        print(f"样本数量: {n_samples}")
        
        return features, targets
    
    def standardize_features(self, features):
        """
        标准化特征数据 (Z-score normalization)
        """
        print("正在进行数据标准化...")
        
        # 计算每个特征的均值和标准差
        n_features = len(features[0])
        means = []
        stds = []
        
        for j in range(n_features):
            col_values = [features[i][j] for i in range(len(features))]
            mean_val = sum(col_values) / len(col_values)
            variance = sum((x - mean_val)**2 for x in col_values) / len(col_values)
            std_val = math.sqrt(variance) if variance > 0 else 1  # 避免除零
            
            means.append(mean_val)
            stds.append(std_val)
        
        # 保存用于后续预测
        self.feature_means = means
        self.feature_stds = stds
        
        # 标准化数据
        standardized_features = []
        for i in range(len(features)):
            row = [(features[i][j] - means[j]) / stds[j] for j in range(n_features)]
            standardized_features.append(row)
        
        print("数据标准化完成")
        return standardized_features
    
    def split_data(self, features: List[List[float]], targets: List[float], test_size=0.2) -> Tuple:
        """
        划分训练集和测试集
        """
        print(f"\n正在划分数据集 (测试集比例: {test_size})...")
        
        n_samples = len(features)
        n_test = int(n_samples * test_size)
        
        # 随机打乱索引
        indices = list(range(n_samples))
        random.shuffle(indices)
        
        test_indices = set(indices[:n_test])
        train_features, train_targets = [], []
        test_features, test_targets = [], []
        
        for i in range(n_samples):
            if i in test_indices:
                test_features.append(features[i])
                test_targets.append(targets[i])
            else:
                train_features.append(features[i])
                train_targets.append(targets[i])
        
        print(f"训练集大小: {len(train_features)} 样本")
        print(f"测试集大小: {len(test_features)} 样本")
        
        return train_features, test_features, train_targets, test_targets
    
    def train_model(self, X_train: List[List[float]], y_train: List[float]):
        """
        使用梯度下降法训练线性回归模型
        """
        print("\n正在训练模型 (使用梯度下降法)...")
        
        n_features = len(X_train[0])
        n_samples = len(X_train)
        
        # 初始化权重和偏置
        weights = [random.uniform(-0.01, 0.01) for _ in range(n_features)]
        bias = 0.0
        learning_rate = 0.01
        epochs = 1000
        
        # 梯度下降
        for epoch in range(epochs):
            total_error = 0
            
            # 计算预测值和误差
            predictions = []
            for i in range(n_samples):
                pred = sum(weights[j] * X_train[i][j] for j in range(n_features)) + bias
                predictions.append(pred)
            
            # 计算梯度
            weight_gradients = [0.0 for _ in range(n_features)]
            bias_gradient = 0.0
            
            for i in range(n_samples):
                error = predictions[i] - y_train[i]
                total_error += error ** 2
                
                for j in range(n_features):
                    weight_gradients[j] += error * X_train[i][j]
                bias_gradient += error
            
            # 更新权重和偏置
            for j in range(n_features):
                weights[j] -= learning_rate * (weight_gradients[j] / n_samples)
            bias -= learning_rate * (bias_gradient / n_samples)
        
        # 保存训练好的参数
        self.weights = weights
        self.bias = bias
        self.is_trained = True
        
        print(f"训练完成! 经过 {epochs} 轮迭代")
        print(f"学习率: {learning_rate}")
        print(f"最终权重: {[round(w, 4) for w in weights]}")
        print(f"最终偏置: {round(bias, 4)}")
        
        return self
    
    def evaluate_model(self, X_test: List[List[float]], y_test: List[float]):
        """
        评估模型性能
        """
        if not self.is_trained:
            raise ValueError("模型尚未训练，请先调用train_model方法")
        
        print("\n正在评估模型性能...")
        
        # 预测
        y_pred = self.predict(X_test)
        
        # 计算评估指标
        n = len(y_test)
        mse = sum((y_pred[i] - y_test[i])**2 for i in range(n)) / n
        rmse = math.sqrt(mse)
        
        # 计算R²
        mean_y = sum(y_test) / len(y_test)
        ss_tot = sum((y_test[i] - mean_y)**2 for i in range(n))
        ss_res = sum((y_test[i] - y_pred[i])**2 for i in range(n))
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        print(f"均方误差 (MSE): {mse:.4f}")
        print(f"均方根误差 (RMSE): {rmse:.4f}")
        print(f"决定系数 (R²): {r2:.4f}")
        
        return {
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'y_pred': y_pred,
            'y_test': y_test
        }
    
    def predict(self, features: List[List[float]]):
        """
        使用训练好的模型进行预测
        """
        if not self.is_trained:
            raise ValueError("模型尚未训练，请先调用train_model方法")
        
        predictions = []
        for row in features:
            pred = sum(self.weights[i] * row[i] for i in range(len(row))) + self.bias
            predictions.append(pred)
        
        return predictions

def main():
    """
    主函数：演示完整的机器学习流程
    """
    print("="*60)
    print("简单机器学习模型示例 - 完整流程演示")
    print("="*60)
    
    # 创建模型实例
    ml_model = SimpleMLModel()
    
    # 1. 生成示例数据
    features, targets = ml_model.generate_sample_data(n_samples=1000)
    
    # 2. 数据标准化
    standardized_features = ml_model.standardize_features(features)
    
    # 3. 划分数据集
    X_train, X_test, y_train, y_test = ml_model.split_data(standardized_features, targets)
    
    # 4. 训练模型
    model = ml_model.train_model(X_train, y_train)
    
    # 5. 评估模型
    metrics = ml_model.evaluate_model(X_test, y_test)
    
    # 6. 对新数据进行预测示例
    print("\n对新数据进行预测示例:")
    new_data_unscaled = [[1.0, 0.5, -0.2], [2.0, -1.0, 0.8]]
    
    # 需要使用与训练数据相同的标准化参数
    new_data = []
    for row in new_data_unscaled:
        standardized_row = [(row[j] - ml_model.feature_means[j]) / ml_model.feature_stds[j] for j in range(len(row))]
        new_data.append(standardized_row)
    
    new_predictions = ml_model.predict(new_data)
    print(f"新数据 (原始): {new_data_unscaled}")
    print(f"新数据 (标准化后): {[ [round(val, 4) for val in row] for row in new_data ]}")
    print(f"预测结果: {[round(pred, 4) for pred in new_predictions]}")
    
    print("\n" + "="*60)
    print("机器学习流程演示完成!")
    print("="*60)

if __name__ == "__main__":
    main()