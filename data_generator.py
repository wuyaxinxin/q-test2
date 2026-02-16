# 始终生效

import random
from datetime import datetime


def generate_trade_data():
    """
    生成全球贸易模拟数据
    
    返回包含2015-2024年5个主要国家的进出口数据
    """
    years = list(range(2015, 2025))
    
    countries_config = {
        '中国': {
            'base_import': 12000,
            'base_export': 15000,
            'growth_rate_import': 0.065,
            'growth_rate_export': 0.070,
        },
        '美国': {
            'base_import': 18000,
            'base_export': 13000,
            'growth_rate_import': 0.030,
            'growth_rate_export': 0.025,
        },
        '德国': {
            'base_import': 9000,
            'base_export': 11000,
            'growth_rate_import': 0.020,
            'growth_rate_export': 0.022,
        },
        '日本': {
            'base_import': 7000,
            'base_export': 8500,
            'growth_rate_import': 0.015,
            'growth_rate_export': 0.018,
        },
        '英国': {
            'base_import': 6000,
            'base_export': 5500,
            'growth_rate_import': 0.012,
            'growth_rate_export': 0.015,
        }
    }
    
    countries = {}
    
    for country_name, config in countries_config.items():
        import_data = []
        export_data = []
        
        for i, year in enumerate(years):
            import_value = config['base_import'] * ((1 + config['growth_rate_import']) ** i)
            export_value = config['base_export'] * ((1 + config['growth_rate_export']) ** i)
            
            import_value *= random.uniform(0.95, 1.05)
            export_value *= random.uniform(0.95, 1.05)
            
            import_data.append(round(import_value, 2))
            export_data.append(round(export_value, 2))
        
        countries[country_name] = {
            'import': import_data,
            'export': export_data
        }
    
    return {
        'status': 'success',
        'data': {
            'years': years,
            'countries': countries
        },
        'timestamp': datetime.now().isoformat()
    }


if __name__ == '__main__':
    data = generate_trade_data()
    print(data)
