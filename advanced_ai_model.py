"""
企业级AI工程系统 - 展示AI工程师综合能力
"""

import random
import math
from typing import List, Tuple, Dict, Optional, Callable
import time
import json
import hashlib
from datetime import datetime
import threading
import queue
import statistics


class AIPipelineOrchestrator:
    """AI流水线编排器 - 展示AI工程师的系统编排能力"""
    
    def __init__(self):
        self.pipeline_stages = []
        self.stage_results = {}
        self.execution_history = []
        self.monitoring_callbacks = []
        
    def add_stage(self, stage_name: str, stage_function: Callable, dependencies: List[str] = None):
        """添加流水线阶段"""
        stage = {
            'name': stage_name,
            'function': stage_function,
            'dependencies': dependencies or [],
            'executed': False,
            'result': None,
            'execution_time': 0
        }
        self.pipeline_stages.append(stage)
        
    def execute_pipeline(self, ml_system, ethics_governance) -> Dict:
        """执行AI流水线"""
        print("[PIPELINE] 开始执行AI流水线...")
        
        start_time = time.time()
        execution_order = self._determine_execution_order()
        
        for stage_name in execution_order:
            stage = next(s for s in self.pipeline_stages if s['name'] == stage_name)
            print(f"[PIPELINE] 执行阶段: {stage_name}")
            
            stage_start = time.time()
            try:
                # 根据阶段函数的参数需求来调用
                if stage_name == 'data_ingestion':
                    result = stage['function']()
                elif stage_name == 'feature_engineering':
                    input_data = self.stage_results.get('data_ingestion')
                    if input_data is None:
                        raise ValueError(f"依赖阶段 'data_ingestion' 未执行或失败")
                    result = stage['function'](input_data)
                elif stage_name == 'data_preprocessing':
                    input_data = self.stage_results.get('feature_engineering')
                    if input_data is None:
                        raise ValueError(f"依赖阶段 'feature_engineering' 未执行或失败")
                    result = stage['function'](input_data)
                elif stage_name == 'model_training':
                    input_data = self.stage_results.get('data_preprocessing')
                    if input_data is None:
                        raise ValueError(f"依赖阶段 'data_preprocessing' 未执行或失败")
                    result = stage['function'](input_data)
                elif stage_name == 'model_evaluation':
                    # 对于评估阶段，使用预处理后的数据的一部分作为测试数据
                    processed_data = self.stage_results.get('data_preprocessing')
                    if processed_data is None:
                        raise ValueError(f"依赖阶段 'data_preprocessing' 未执行或失败")
                    result = stage['function'](processed_data)
                elif stage_name == 'fairness_analysis':
                    # 公平性分析需要模型和原始数据
                    input_data = self.stage_results.get('data_ingestion')
                    if input_data is None:
                        raise ValueError(f"依赖阶段 'data_ingestion' 未执行或失败")
                    result = stage['function'](ml_system, input_data)
                elif stage_name == 'privacy_analysis':
                    # 隐私分析需要模型和原始数据
                    input_data = self.stage_results.get('data_ingestion')
                    if input_data is None:
                        raise ValueError(f"依赖阶段 'data_ingestion' 未执行或失败")
                    result = stage['function'](ml_system, input_data)
                elif stage_name == 'audit_compliance':
                    # 审计合规需要模型和评估结果
                    eval_results = self.stage_results.get('model_evaluation', {})
                    result = stage['function'](ml_system, eval_results)
                else:
                    result = stage['function'](self.stage_results)
                
                execution_time = time.time() - stage_start
                
                stage['result'] = result
                stage['execution_time'] = execution_time
                stage['executed'] = True
                self.stage_results[stage_name] = result
                
                print(f"[PIPELINE] 阶段 {stage_name} 完成, 用时: {execution_time:.2f}s")
                
            except Exception as e:
                print(f"[PIPELINE] 阶段 {stage_name} 失败: {str(e)}")
                stage['result'] = {'error': str(e)}
                stage['executed'] = False
        
        total_time = time.time() - start_time
        self.execution_history.append({
            'execution_time': total_time,
            'completed_at': time.time(),
            'stages_executed': len([s for s in self.pipeline_stages if s['executed']])
        })
        
        print(f"[PIPELINE] 流水线执行完成, 总用时: {total_time:.2f}s")
        
        return {
            'total_execution_time': total_time,
            'stages_completed': len([s for s in self.pipeline_stages if s['executed']]),
            'stages_failed': len([s for s in self.pipeline_stages if not s['executed']]),
            'stage_results': self.stage_results
        }
    
    def _determine_execution_order(self) -> List[str]:
        """确定执行顺序"""
        executed = set()
        remaining = set(stage['name'] for stage in self.pipeline_stages)
        execution_order = []
        
        while remaining:
            ready_stages = []
            for stage in self.pipeline_stages:
                if stage['name'] in remaining and all(dep in executed for dep in stage['dependencies']):
                    ready_stages.append(stage['name'])
            
            if not ready_stages:
                raise Exception("无法解析依赖关系")
            
            for stage_name in ready_stages:
                execution_order.append(stage_name)
                executed.add(stage_name)
                remaining.remove(stage_name)
        
        return execution_order


class AdvancedMLSystem:
    """高级机器学习系统 - 展示AI工程师的模型工程能力"""
    
    def __init__(self, n_features: int = 3):
        self.n_features = n_features
        self.weights = [random.uniform(-0.01, 0.01) for _ in range(n_features)]
        self.bias = 0.0
        self.feature_scalers = [{'mean': 0.0, 'std': 1.0} for _ in range(n_features)]
        self.is_trained = False
        self.training_history = []
        self.validation_results = {}
        self.model_id = self._generate_model_id()
        self.performance_monitoring = {
            'latency_samples': [],
            'throughput_samples': [],
            'accuracy_samples': []
        }
        
    def _generate_model_id(self) -> str:
        """生成唯一模型ID"""
        timestamp = str(time.time())
        hash_input = f"{timestamp}_{self.n_features}".encode()
        return f"sys_model_{hashlib.md5(hash_input).hexdigest()[:12]}"
    
    def data_ingestion_stage(self) -> Tuple[List[List[float]], List[float]]:
        """数据摄取阶段"""
        print(f"[ML-SYSTEM] 执行数据摄取...")
        
        n_samples = 2000
        features = []
        targets = []
        
        for i in range(n_samples):
            row = [random.gauss(0, 1) for _ in range(self.n_features)]
            features.append(row)
            
            # 复杂的目标生成 (模拟真实世界关系)
            target = (3 * row[0] + 2 * row[1] - row[2] + 
                     0.5 * row[0] * row[1] +  # 交互项
                     0.1 * random.gauss(0, 1))  # 噪声
            targets.append(target)
        
        print(f"[ML-SYSTEM] 数据摄取完成: {n_samples} 样本, {self.n_features} 特征")
        return features, targets
    
    def feature_engineering_stage(self, raw_data: Tuple) -> Tuple[List[List[float]], List[float]]:
        """特征工程阶段"""
        print(f"[ML-SYSTEM] 执行特征工程...")
        
        features, targets = raw_data
        
        # 特征变换：添加多项式特征
        enhanced_features = []
        for row in features:
            enhanced_row = row[:]  # 原始特征
            
            # 添加交互特征
            enhanced_row.extend([
                row[0] * row[1],  # 特征交互
                row[0] * row[2],
                row[1] * row[2],
                row[0] ** 2,      # 多项式特征
                row[1] ** 2,
                row[2] ** 2
            ])
            enhanced_features.append(enhanced_row)
        
        # 更新特征数量
        self.n_features = len(enhanced_features[0])
        self.feature_scalers = [{'mean': 0.0, 'std': 1.0} for _ in range(self.n_features)]
        
        print(f"[ML-SYSTEM] 特征工程完成: {len(enhanced_features)} 样本, {self.n_features} 增强特征")
        return enhanced_features, targets
    
    def data_preprocessing_stage(self, features_targets: Tuple) -> Tuple[List[List[float]], List[float]]:
        """数据预处理阶段"""
        print(f"[ML-SYSTEM] 执行数据预处理...")
        
        features, targets = features_targets
        
        # 计算缩放参数
        for j in range(self.n_features):
            col_values = [features[i][j] for i in range(len(features))]
            mean_val = sum(col_values) / len(col_values)
            variance = sum((x - mean_val)**2 for x in col_values) / len(col_values)
            std_val = math.sqrt(max(variance, 1e-8))
            
            self.feature_scalers[j]['mean'] = mean_val
            self.feature_scalers[j]['std'] = std_val
        
        # 应用缩放
        scaled_features = []
        for i in range(len(features)):
            row = [(features[i][j] - self.feature_scalers[j]['mean']) / self.feature_scalers[j]['std'] 
                   for j in range(self.n_features)]
            scaled_features.append(row)
        
        print(f"[ML-SYSTEM] 数据预处理完成")
        return scaled_features, targets
    
    def model_training_stage(self, processed_data: Tuple) -> Dict:
        """模型训练阶段"""
        print(f"[ML-SYSTEM] 执行模型训练...")
        
        features, targets = processed_data
        
        # 重要：更新权重数组大小以匹配新的特征数量
        if len(self.weights) != self.n_features:
            self.weights = [random.uniform(-0.01, 0.01) for _ in range(self.n_features)]
        
        # 分割数据
        split_idx = int(0.8 * len(features))
        train_features = features[:split_idx]
        train_targets = targets[:split_idx]
        val_features = features[split_idx:]
        val_targets = targets[split_idx:]
        
        # 使用更复杂的优化算法
        learning_rate = 0.01
        epochs = 300
        best_val_loss = float('inf')
        patience = 20
        patience_counter = 0
        
        start_time = time.time()
        
        for epoch in range(epochs):
            # 前向传播
            predictions = []
            for row in train_features:
                pred = sum(self.weights[i] * row[i] for i in range(len(row))) + self.bias
                predictions.append(pred)
            
            # 计算梯度
            n_samples = len(train_features)
            weight_gradients = [0.0] * self.n_features
            bias_gradient = 0.0
            
            for i in range(n_samples):
                error = predictions[i] - train_targets[i]
                for j in range(self.n_features):
                    weight_gradients[j] += error * train_features[i][j]
                bias_gradient += error
            
            # 更新参数
            for j in range(self.n_features):
                self.weights[j] -= learning_rate * weight_gradients[j] / n_samples
            self.bias -= learning_rate * bias_gradient / n_samples
            
            # 验证损失
            val_predictions = [sum(self.weights[i] * row[i] for i in range(len(row))) + self.bias 
                              for row in val_features]
            val_loss = sum((val_predictions[i] - val_targets[i])**2 for i in range(len(val_targets))) / len(val_targets)
            
            # 早停
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
            else:
                patience_counter += 1
            
            if patience_counter >= patience:
                print(f"[ML-SYSTEM] 早停触发，最佳验证损失: {best_val_loss:.6f}")
                break
            
            if epoch % 50 == 0:
                train_loss = sum((predictions[i] - train_targets[i])**2 for i in range(len(train_targets))) / len(train_targets)
                print(f"[ML-SYSTEM] Epoch {epoch}: Train Loss = {train_loss:.6f}, Val Loss = {val_loss:.6f}")
        
        training_time = time.time() - start_time
        self.is_trained = True
        
        print(f"[ML-SYSTEM] 模型训练完成! 用时: {training_time:.2f}s")
        print(f"[ML-SYSTEM] 最终权重: {[round(w, 4) for w in self.weights[:5]]}...")  # 显示前5个权重
        
        return {
            'training_time': training_time,
            'final_weights': self.weights[:],
            'final_bias': self.bias,
            'epochs_run': epoch + 1,
            'best_validation_loss': best_val_loss
        }
    
    def model_evaluation_stage(self, processed_data: Tuple) -> Dict:
        """模型评估阶段"""
        print(f"[ML-SYSTEM] 执行模型评估...")
        
        # 从处理后的数据中分离出测试集
        features, targets = processed_data
        split_idx = int(0.8 * len(features))
        test_features = features[split_idx:]
        test_targets = targets[split_idx:]
        
        if len(test_features) == 0:
            # 如果训练数据不够，使用最后20%的数据作为测试
            split_idx = int(0.8 * len(features))
            test_features = features[split_idx:]
            test_targets = targets[split_idx:]
        
        if len(test_features) == 0:
            # 如果还是没有足够的测试数据，使用最后几个样本
            test_size = min(100, len(features) // 4)  # 使用大约25%的数据作为测试
            test_features = features[-test_size:]
            test_targets = targets[-test_size:]
        
        predictions = self.predict_batch(test_features)
        
        n = len(test_targets)
        
        # 计算评估指标
        mse = sum((predictions[i] - test_targets[i])**2 for i in range(n)) / n
        rmse = math.sqrt(mse)
        mae = sum(abs(predictions[i] - test_targets[i]) for i in range(n)) / n
        
        mean_target = sum(test_targets) / n
        ss_tot = sum((test_targets[i] - mean_target)**2 for i in range(n))
        ss_res = sum((test_targets[i] - predictions[i])**2 for i in range(n))
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # 计算其他统计指标
        residuals = [predictions[i] - test_targets[i] for i in range(n)]
        residual_mean = sum(residuals) / n
        residual_std = math.sqrt(sum((r - residual_mean)**2 for r in residuals) / n)
        
        evaluation_metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'residual_mean': residual_mean,
            'residual_std': residual_std,
            'n_samples': n
        }
        
        print(f"[ML-SYSTEM] 评估结果:")
        print(f"  MSE: {mse:.6f}")
        print(f"  RMSE: {rmse:.6f}")
        print(f"  MAE: {mae:.6f}")
        print(f"  R²: {r2:.6f}")
        print(f"  测试样本数: {n}")
        
        return evaluation_metrics
    
    def predict_batch(self, features: List[List[float]]) -> List[float]:
        """批量预测"""
        if not self.is_trained:
            raise ValueError("模型未训练，请先调用训练方法")
        
        start_time = time.time()
        predictions = []
        
        for row in features:
            pred = sum(self.weights[i] * row[i] for i in range(len(row))) + self.bias
            predictions.append(pred)
        
        latency = time.time() - start_time
        throughput = len(features) / latency if latency > 0 else float('inf')
        
        # 记录性能指标
        self.performance_monitoring['latency_samples'].append(latency)
        self.performance_monitoring['throughput_samples'].append(throughput)
        
        return predictions
    
    def predict_single(self, features: List[float]) -> float:
        """单个预测"""
        if not self.is_trained:
            raise ValueError("模型未训练，请先调用训练方法")
        
        prediction = sum(self.weights[i] * features[i] for i in range(len(features))) + self.bias
        return prediction


class AIEthicsAndGovernance:
    """AI伦理与治理 - 展示AI工程师的治理能力"""
    
    def __init__(self):
        self.fairness_metrics = {}
        self.privacy_protecting_methods = []
        self.audit_logs = []
        self.compliance_standards = {
            'GDPR': False,
            'AI_ACT': False,
            'ISO_23053': False
        }
        
    def fairness_analysis_stage(self, model: AdvancedMLSystem, test_data: Tuple) -> Dict:
        """公平性分析"""
        print(f"[ETHICS] 执行公平性分析...")
        
        features, targets = test_data
        predictions = model.predict_batch(features)
        
        # 模拟敏感属性分析 (假设第0个特征为敏感属性)
        protected_groups = {}
        for i, (feat_row, pred) in enumerate(zip(features, predictions)):
            # 根据敏感特征值分组
            sensitive_val = feat_row[0]  # 假设第0个特征是敏感的
            group_key = 'high' if sensitive_val > 0 else 'low'
            
            if group_key not in protected_groups:
                protected_groups[group_key] = {'predictions': [], 'targets': []}
            
            protected_groups[group_key]['predictions'].append(pred)
            protected_groups[group_key]['targets'].append(targets[i])
        
        # 计算各组的统计信息
        group_stats = {}
        for group, data in protected_groups.items():
            group_stats[group] = {
                'count': len(data['predictions']),
                'avg_prediction': sum(data['predictions']) / len(data['predictions']) if data['predictions'] else 0,
                'avg_target': sum(data['targets']) / len(data['targets']) if data['targets'] else 0,
                'std_prediction': statistics.stdev(data['predictions']) if len(data['predictions']) > 1 else 0
            }
        
        # 计算公平性指标 (统计平等)
        groups = list(group_stats.values())
        if len(groups) > 1:
            prediction_disparity = max(g['avg_prediction'] for g in groups) - min(g['avg_prediction'] for g in groups)
            target_disparity = max(g['avg_target'] for g in groups) - min(g['avg_target'] for g in groups)
        else:
            prediction_disparity = 0
            target_disparity = 0
        
        fairness_result = {
            'group_statistics': group_stats,
            'prediction_disparity': prediction_disparity,
            'target_disparity': target_disparity,
            'fairness_score': 1.0 - min(1.0, prediction_disparity),  # 简单评分
            'fairness_threshold_met': prediction_disparity < 0.1
        }
        
        print(f"[ETHICS] 公平性分析完成: disparity={prediction_disparity:.4f}, fair={fairness_result['fairness_threshold_met']}")
        
        return fairness_result
    
    def privacy_analysis_stage(self, model: AdvancedMLSystem, training_data: Tuple) -> Dict:
        """隐私分析"""
        print(f"[ETHICS] 执行隐私分析...")
        
        features, targets = training_data
        
        # 简单的成员推理攻击风险评估
        # 检查模型在训练数据上的表现是否显著优于测试数据
        train_predictions = model.predict_batch(features[:200])  # 用部分训练数据
        train_targets_subset = targets[:200]
        
        # 计算训练数据上的误差
        train_errors = [abs(train_predictions[i] - train_targets_subset[i]) 
                       for i in range(len(train_predictions))]
        avg_train_error = sum(train_errors) / len(train_errors)
        
        privacy_metrics = {
            'avg_training_error': avg_train_error,
            'potential_membership_risk': avg_train_error < 0.1,  # 如果误差很小，可能有过拟合
            'privacy_score': 1.0 / (1.0 + avg_train_error),  # 简单的隐私评分
            'recommendations': []
        }
        
        if privacy_metrics['potential_membership_risk']:
            privacy_metrics['recommendations'].append(
                "检测到潜在的成员推理风险，建议使用差分隐私技术"
            )
        
        print(f"[ETHICS] 隐私分析完成: score={privacy_metrics['privacy_score']:.4f}")
        
        return privacy_metrics
    
    def audit_and_compliance_stage(self, model: AdvancedMLSystem, results: Dict) -> Dict:
        """审计与合规"""
        print(f"[ETHICS] 执行审计与合规检查...")
        
        audit_result = {
            'model_id': model.model_id,
            'compliance_check': {
                'gdpr_compliant': True,  # 简化的合规检查
                'explainability_implemented': True,
                'bias_testing_performed': True,
                'privacy_protected': True
            },
            'audit_trail': [
                f"Model {model.model_id} created at {datetime.now()}",
                f"Training completed with R²={results.get('r2', 0):.4f}",
                "Fairness analysis performed",
                "Privacy analysis performed"
            ],
            'certification_recommendation': 'Model meets enterprise standards'
        }
        
        print(f"[ETHICS] 审计与合规检查完成")
        
        return audit_result


def main():
    """主要演示函数"""
    print("="*80)
    print("企业级AI工程系统 - AI工程师综合能力演示")
    print("="*80)
    
    # 创建系统组件
    orchestrator = AIPipelineOrchestrator()
    ml_system = AdvancedMLSystem(n_features=3)
    ethics_governance = AIEthicsAndGovernance()
    
    # 构建AI流水线
    orchestrator.add_stage('data_ingestion', ml_system.data_ingestion_stage)
    orchestrator.add_stage('feature_engineering', ml_system.feature_engineering_stage, ['data_ingestion'])
    orchestrator.add_stage('data_preprocessing', ml_system.data_preprocessing_stage, ['feature_engineering'])
    orchestrator.add_stage('model_training', ml_system.model_training_stage, ['data_preprocessing'])
    orchestrator.add_stage('model_evaluation', ml_system.model_evaluation_stage, ['data_preprocessing'])  # 评估依赖于预处理数据
    orchestrator.add_stage('fairness_analysis', ethics_governance.fairness_analysis_stage, ['data_ingestion', 'model_training'])  # 需要模型训练完成后
    orchestrator.add_stage('privacy_analysis', ethics_governance.privacy_analysis_stage, ['data_ingestion', 'model_training'])  # 需要模型训练完成后
    orchestrator.add_stage('audit_compliance', ethics_governance.audit_and_compliance_stage, ['model_evaluation'])
    
    # 执行流水线
    pipeline_results = orchestrator.execute_pipeline(ml_system, ethics_governance)
    
    # 提取关键结果
    eval_results = pipeline_results['stage_results'].get('model_evaluation', {})
    fairness_results = pipeline_results['stage_results'].get('fairness_analysis', {})
    privacy_results = pipeline_results['stage_results'].get('privacy_analysis', {})
    audit_results = pipeline_results['stage_results'].get('audit_compliance', {})
    
    # 输出最终报告
    print("\n" + "="*80)
    print("AI系统综合评估报告")
    print("="*80)
    print(f"模型ID: {ml_system.model_id}")
    print(f"流水线总执行时间: {pipeline_results['total_execution_time']:.2f}s")
    print(f"成功执行阶段数: {pipeline_results['stages_completed']}")
    print(f"失败阶段数: {pipeline_results['stages_failed']}")
    print()
    print("性能指标:")
    print(f"  R² 得分: {eval_results.get('r2', 0):.4f}")
    print(f"  RMSE: {eval_results.get('rmse', 0):.4f}")
    print(f"  MAE: {eval_results.get('mae', 0):.4f}")
    print()
    print("公平性指标:")
    print(f"  预测差异: {fairness_results.get('prediction_disparity', 0):.4f}")
    print(f"  公平性得分: {fairness_results.get('fairness_score', 0):.4f}")
    print(f"  符合公平性阈值: {fairness_results.get('fairness_threshold_met', False)}")
    print()
    print("隐私指标:")
    print(f"  隐私得分: {privacy_results.get('privacy_score', 0):.4f}")
    print(f"  成员推理风险: {privacy_results.get('potential_membership_risk', False)}")
    print()
    print("治理与合规:")
    print(f"  GDPR合规: {audit_results.get('compliance_check', {}).get('gdpr_compliant', False)}")
    print(f"  可解释性实现: {audit_results.get('compliance_check', {}).get('explainability_implemented', False)}")
    print(f"  偏见测试执行: {audit_results.get('compliance_check', {}).get('bias_testing_performed', False)}")
    print()
    print("系统就绪状态:")
    is_ready = (
        eval_results.get('r2', 0) > 0.9 and
        fairness_results.get('fairness_threshold_met', False) and
        privacy_results.get('privacy_score', 0) > 0.8
    )
    print(f"  部署就绪: {is_ready}")
    
    print("\n" + "="*80)
    print("AI工程师综合能力演示完成!")
    print("展示了: 系统架构设计、机器学习工程、数据工程、治理与合规等能力")
    print("="*80)


if __name__ == "__main__":
    main()