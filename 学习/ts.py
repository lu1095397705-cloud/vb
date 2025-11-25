import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import warnings
import requests
import os
import sys

warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    """加载数据函数"""
    try:
        # 尝试从Gitee加载数据
        train_url = "https://gitee.com/lu228826/box/raw/master/study/purchase_prediction_train_set.csv"
        test_url = "https://gitee.com/lu228826/box/raw/master/study/purchase_prediction_test_set.csv"

        train_data = pd.read_csv(train_url)
        test_data = pd.read_csv(test_url)

        print("✅ 数据加载成功")
        print(f"训练数据形状: {train_data.shape}")
        print(f"测试数据形状: {test_data.shape}")

        return train_data, test_data

    except Exception as e:
        print(f"数据加载失败: {e}")
        print("使用示例数据...")

        # 创建示例数据
        np.random.seed(42)
        n_train = 1000
        n_test = 200

        # 训练数据
        train_data = pd.DataFrame({
            'gender': np.random.choice(['Male', 'Female'], n_train),
            'age': np.random.randint(18, 65, n_train),
            'income': np.random.randint(3000, 20000, n_train),
            'is_purchase': np.random.randint(0, 2, n_train)
        })

        # 测试数据
        test_data = pd.DataFrame({
            'ID': range(1, n_test + 1),
            'gender': np.random.choice(['Male', 'Female'], n_test),
            'age': np.random.randint(18, 65, n_test),
            'income': np.random.randint(3000, 20000, n_test)
        })

        return train_data, test_data


def preprocess_data(train_data, test_data):
    """数据预处理函数"""
    print("\n=== 数据预处理 ===")

    # 复制数据避免修改原数据
    train_processed = train_data.copy()
    test_processed = test_data.copy()

    # 自动识别列名
    def identify_columns(df, is_train=True):
        column_mapping = {}
        actual_columns = df.columns.tolist()

        # 性别列识别
        gender_keywords = ['gender', '性别', 'sex']
        for col in actual_columns:
            if any(keyword in col.lower() for keyword in gender_keywords):
                column_mapping['gender'] = col
                break

        # 年龄列识别
        age_keywords = ['age', '年龄']
        for col in actual_columns:
            if any(keyword in col.lower() for keyword in age_keywords):
                column_mapping['age'] = col
                break

        # 收入列识别
        income_keywords = ['income', '收入', 'salary']
        for col in actual_columns:
            if any(keyword in col.lower() for keyword in income_keywords):
                column_mapping['income'] = col
                break

        # 标签列识别（仅训练数据）
        if is_train:
            purchase_keywords = ['purchase', 'is_purchase', 'label', 'target']
            for col in actual_columns:
                if any(keyword in col.lower() for keyword in purchase_keywords):
                    column_mapping['is_purchase'] = col
                    break

        return column_mapping

    # 识别列名
    train_mapping = identify_columns(train_processed, is_train=True)
    test_mapping = identify_columns(test_processed, is_train=False)

    print(f"训练数据列映射: {train_mapping}")
    print(f"测试数据列映射: {test_mapping}")

    # 重命名列为标准名称
    train_processed = train_processed.rename(columns={v: k for k, v in train_mapping.items()})
    test_processed = test_processed.rename(columns={v: k for k, v in test_mapping.items()})

    # 确保必要的列存在
    required_train_cols = ['gender', 'age', 'income', 'is_purchase']
    required_test_cols = ['gender', 'age', 'income']

    for col in required_train_cols:
        if col not in train_processed.columns:
            if col == 'gender':
                train_processed[col] = np.random.choice(['Male', 'Female'], len(train_processed))
            elif col == 'age':
                train_processed[col] = np.random.randint(18, 65, len(train_processed))
            elif col == 'income':
                train_processed[col] = np.random.randint(3000, 20000, len(train_processed))
            elif col == 'is_purchase':
                train_processed[col] = np.random.randint(0, 2, len(train_processed))

    for col in required_test_cols:
        if col not in test_processed.columns:
            if col == 'gender':
                test_processed[col] = np.random.choice(['Male', 'Female'], len(test_processed))
            elif col == 'age':
                test_processed[col] = np.random.randint(18, 65, len(test_processed))
            elif col == 'income':
                test_processed[col] = np.random.randint(3000, 20000, len(test_processed))

    # 确保测试数据有ID列
    if 'ID' not in test_processed.columns:
        test_processed['ID'] = range(1, len(test_processed) + 1)

    # 数据清洗
    def clean_dataset(df):
        df_clean = df.copy()

        # 处理性别列
        if 'gender' in df_clean.columns:
            df_clean['gender'] = df_clean['gender'].astype(str)
            # 统一性别格式
            gender_map = {
                '男': 'Male', '男性': 'Male', '男人': 'Male', '男士': 'Male',
                '女': 'Female', '女性': 'Female', '女人': 'Female', '女士': 'Female',
                'M': 'Male', 'F': 'Female', 'm': 'Male', 'f': 'Female'
            }
            df_clean['gender'] = df_clean['gender'].map(
                lambda x: gender_map.get(x, 'Male' if x in ['Male', 'M', '男', '男性'] else
                ('Female' if x in ['Female', 'F', '女', '女性'] else 'Male'))
            )

        # 处理缺失值
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                if df_clean[col].dtype == 'object':
                    df_clean[col].fillna(df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else 'Unknown',
                                         inplace=True)
                else:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)

        # 处理异常值
        if 'age' in df_clean.columns:
            df_clean['age'] = df_clean['age'].clip(18, 65)
        if 'income' in df_clean.columns:
            df_clean['income'] = df_clean['income'].clip(1000, 50000)

        return df_clean

    train_processed = clean_dataset(train_processed)
    test_processed = clean_dataset(test_processed)

    print("✅ 数据预处理完成")
    print(f"训练数据形状: {train_processed.shape}")
    print(f"测试数据形状: {test_processed.shape}")

    return train_processed, test_processed


def exploratory_data_analysis(train_data):
    """探索性数据分析"""
    print("\n=== 探索性数据分析 ===")

    # 基本统计信息
    print("数据基本信息:")
    print(train_data.info())
    print("\n数值列统计描述:")
    print(train_data.describe())

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 性别分布
    gender_counts = train_data['gender'].value_counts()
    axes[0, 0].bar(gender_counts.index, gender_counts.values, color=['lightblue', 'lightpink'])
    axes[0, 0].set_title('Gender Distribution')
    axes[0, 0].set_ylabel('Count')

    # 购买分布
    purchase_counts = train_data['is_purchase'].value_counts()
    axes[0, 1].bar(purchase_counts.index, purchase_counts.values, color=['lightcoral', 'lightgreen'])
    axes[0, 1].set_title('Purchase Distribution')
    axes[0, 1].set_ylabel('Count')

    # 购买比例
    purchase_pct = train_data['is_purchase'].value_counts(normalize=True)
    axes[0, 2].pie(purchase_pct.values, labels=['No Purchase', 'Purchase'], autopct='%1.1f%%',
                   colors=['lightcoral', 'lightgreen'])
    axes[0, 2].set_title('Purchase Ratio')

    # 年龄分布
    axes[1, 0].hist(train_data['age'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[1, 0].set_title('Age Distribution')
    axes[1, 0].set_xlabel('Age')
    axes[1, 0].set_ylabel('Frequency')

    # 收入分布
    axes[1, 1].hist(train_data['income'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    axes[1, 1].set_title('Income Distribution')
    axes[1, 1].set_xlabel('Income')
    axes[1, 1].set_ylabel('Frequency')

    # 性别与购买关系
    purchase_by_gender = train_data.groupby('gender')['is_purchase'].mean()
    axes[1, 2].bar(purchase_by_gender.index, purchase_by_gender.values, color=['lightblue', 'lightpink'])
    axes[1, 2].set_title('Purchase Rate by Gender')
    axes[1, 2].set_ylabel('Purchase Rate')

    plt.tight_layout()
    plt.show()

    # 相关性分析
    numeric_data = train_data[['age', 'income', 'is_purchase']].corr()
    print("\n数值特征相关性矩阵:")
    print(numeric_data)

    return fig


def train_models(X_train, y_train, X_test, y_test):
    """训练多个模型并选择最佳模型"""
    print("\n=== 模型训练 ===")

    # 数据预处理管道
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['age', 'income']),
            ('cat', OneHotEncoder(drop='first'), ['gender'])
        ]
    )

    # 定义多个模型
    models = {
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
        'DecisionTree': DecisionTreeClassifier(random_state=42, max_depth=5),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=3)
    }

    results = {}

    for name, model in models.items():
        try:
            # 创建管道
            pipeline = Pipeline([
                ('preprocessor', preprocessor),
                ('model', model)
            ])

            # 训练模型
            pipeline.fit(X_train, y_train)

            # 预测
            y_pred = pipeline.predict(X_test)

            # 评估
            accuracy = accuracy_score(y_test, y_pred)

            results[name] = {
                'pipeline': pipeline,
                'accuracy': accuracy,
                'predictions': y_pred
            }

            print(f"{name}: 准确率 = {accuracy:.4f}")

        except Exception as e:
            print(f"{name} 训练失败: {e}")

    return results


def create_submission_file(model, test_data, filename='submission.csv'):
    """创建提交文件"""
    print("\n=== 生成提交文件 ===")

    # 准备测试数据特征
    feature_cols = ['gender', 'age', 'income']
    X_test = test_data[feature_cols]

    # 进行预测
    predictions = model.predict(X_test)

    # 创建提交DataFrame
    submission_df = pd.DataFrame({
        'ID': test_data['ID'],
        'Prediction': predictions
    })

    # 数据清洗：确保没有非法值
    submission_df = clean_submission_data(submission_df)

    # 保存文件
    submission_df.to_csv(filename, index=False)

    print(f"✅ 提交文件已生成: {filename}")
    print(f"文件形状: {submission_df.shape}")
    print("前5行预览:")
    print(submission_df.head())
    print(f"\n预测分布:\n{submission_df['Prediction'].value_counts()}")

    return submission_df


def clean_submission_data(submission_df):
    """清洗提交数据，确保没有非法值"""
    df_clean = submission_df.copy()

    # 处理缺失值
    df_clean.fillna(0, inplace=True)

    # 处理无穷大值
    df_clean = df_clean.replace([np.inf, -np.inf], 0)

    # 确保预测值为0或1
    df_clean['Prediction'] = df_clean['Prediction'].apply(
        lambda x: 1 if x > 0.5 else 0
    ).astype(int)

    # 确保ID为整数
    df_clean['ID'] = df_clean['ID'].astype(int)

    return df_clean


def submit_to_heywhale(submission_file, token):
    """提交到和鲸平台"""
    print("\n=== 和鲸平台提交 ===")

    # 检查文件是否存在
    if not os.path.exists(submission_file):
        print(f"❌ 提交文件 {submission_file} 不存在")
        return False

    # 检查文件格式
    try:
        df_check = pd.read_csv(submission_file)
        if 'ID' not in df_check.columns or 'Prediction' not in df_check.columns:
            print("❌ 文件格式错误: 必须包含 'ID' 和 'Prediction' 列")
            return False

        # 检查预测值是否合法
        if not df_check['Prediction'].isin([0, 1]).all():
            print("❌ 预测值必须为0或1")
            return False

        print("✅ 文件格式检查通过")
    except Exception as e:
        print(f"❌ 文件读取失败: {e}")
        return False

    # 下载提交工具
    print("1. 下载提交工具...")
    try:
        # 使用requests下载提交工具
        submit_tool_url = "https://cdn.kesci.com/submit_tool/v4/heywhale_submit"
        response = requests.get(submit_tool_url)

        if response.status_code == 200:
            with open('heywhale_submit', 'wb') as f:
                f.write(response.content)

            # 设置执行权限
            os.chmod('heywhale_submit', 0o755)
            print("✅ 提交工具下载成功")
        else:
            print(f"❌ 下载失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 下载过程中出错: {e}")
        return False

    # 执行提交
    print("2. 执行提交...")
    try:
        # 使用subprocess执行提交命令
        cmd = f'./heywhale_submit -token {token} -file {submission_file}'
        result = os.system(cmd)

        if result == 0:
            print("✅ 提交成功!")
            return True
        else:
            print(f"❌ 提交失败，返回码: {result}")
            return False
    except Exception as e:
        print(f"❌ 提交过程中出错: {e}")
        return False


def main():
    """主函数"""
    print("开始客户购买预测分析...")
    print("=" * 50)

    # 1. 加载数据
    train_data, test_data = load_data()

    # 2. 数据预处理
    train_processed, test_processed = preprocess_data(train_data, test_data)

    # 3. 探索性数据分析
    exploratory_data_analysis(train_processed)

    # 4. 准备特征和标签
    X = train_processed[['gender', 'age', 'income']]
    y = train_processed['is_purchase']

    print(f"\n特征形状: {X.shape}")
    print(f"标签分布:\n{y.value_counts()}")

    # 5. 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"训练集大小: {X_train.shape}")
    print(f"测试集大小: {X_test.shape}")

    # 6. 训练模型
    results = train_models(X_train, y_train, X_test, y_test)

    if not results:
        print("❌ 所有模型训练都失败了")
        return

    # 7. 选择最佳模型
    best_model_name = max(results, key=lambda x: results[x]['accuracy'])
    best_model = results[best_model_name]['pipeline']
    best_accuracy = results[best_model_name]['accuracy']

    print(f"\n🎉 最佳模型: {best_model_name} (准确率: {best_accuracy:.4f})")

    # 8. 在完整训练集上重新训练最佳模型
    best_model.fit(X, y)
    print("✅ 已在完整数据集上重新训练最佳模型")

    # 9. 生成提交文件
    submission_file = 'submission.csv'
    submission_df = create_submission_file(best_model, test_processed, submission_file)

    # 10. 提交到和鲸平台
    token = "f6e4a67b7fc8e49c"  # 从图片中获取的token
    success = submit_to_heywhale(submission_file, token)

    if success:
        print("\n🎉 分析完成! 请在和鲸平台查看提交记录")
    else:
        print("\n⚠️  提交失败，但提交文件已生成")
        print("您可以手动执行以下命令进行提交:")
        print(f"!./heywhale_submit -token {token} -file {submission_file}")

    # 11. 保存模型
    model_filename = 'best_purchase_model.pkl'
    joblib.dump(best_model, model_filename)
    print(f"\n💾 最佳模型已保存为: {model_filename}")

    print("\n" + "=" * 50)
    print("分析流程完成")


if __name__ == "__main__":
    main()

