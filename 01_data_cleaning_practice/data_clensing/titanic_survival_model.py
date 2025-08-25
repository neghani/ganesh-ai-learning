import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def load_and_explore_data(file_path):
    """Load the dataset and perform initial exploration"""
    print("Loading Titanic dataset...")
    df = pd.read_csv(file_path)
    
    print(f"Dataset shape: {df.shape}")
    print("\nColumn information:")
    print(df.info())
    
    print("\nFirst few rows:")
    print(df.head())
    
    print("\nSurvival rate:")
    print(df['Survived'].value_counts(normalize=True))
    
    print("\nMissing values:")
    print(df.isnull().sum())
    
    return df

def preprocess_data(df):
    """Clean and preprocess the data for modeling"""
    # Create a copy to avoid modifying original data
    data = df.copy()
    
    # Feature engineering
    # Extract title from name
    data['Title'] = data['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    data['Title'] = data['Title'].replace(['Lady', 'Countess','Capt', 'Col',
                                          'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    data['Title'] = data['Title'].replace('Mlle', 'Miss')
    data['Title'] = data['Title'].replace('Ms', 'Miss')
    data['Title'] = data['Title'].replace('Mme', 'Mrs')
    
    # Family size feature
    data['FamilySize'] = data['SibSp'] + data['Parch'] + 1
    data['IsAlone'] = (data['FamilySize'] == 1).astype(int)
    
    # Age groups
    data['Age'].fillna(data['Age'].median(), inplace=True)
    data['AgeGroup'] = pd.cut(data['Age'], bins=[0, 12, 18, 35, 60, 100], 
                             labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
    
    # Fare groups
    data['Fare'].fillna(data['Fare'].median(), inplace=True)
    data['FareGroup'] = pd.qcut(data['Fare'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])
    
    # Fill missing Embarked with most common value
    data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)
    
    # Handle Cabin - create a feature indicating if cabin is known
    data['HasCabin'] = (~data['Cabin'].isnull()).astype(int)
    
    # Select features for modeling
    features_to_use = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 
                       'Title', 'FamilySize', 'IsAlone', 'AgeGroup', 'FareGroup', 'HasCabin']
    
    # Create feature matrix
    X = data[features_to_use].copy()
    y = data['Survived']
    
    # Encode categorical variables
    categorical_features = ['Sex', 'Embarked', 'Title', 'AgeGroup', 'FareGroup']
    label_encoders = {}
    
    for feature in categorical_features:
        le = LabelEncoder()
        X[feature] = le.fit_transform(X[feature])
        label_encoders[feature] = le
    
    return X, y, label_encoders, data

def train_models(X, y):
    """Train multiple models and compare their performance"""
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features for logistic regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42)
    }
    
    # Train and evaluate models
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        if name == 'Logistic Regression':
            # Use scaled features for logistic regression
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        else:
            # Use original features for tree-based models
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_mean': cv_mean,
            'cv_std': cv_std,
            'predictions': y_pred
        }
        
        print(f"Test Accuracy: {accuracy:.4f}")
        print(f"Cross-validation: {cv_mean:.4f} (+/- {cv_std * 2:.4f})")
        print(f"Classification Report:")
        print(classification_report(y_test, y_pred))
    
    return results, X_test, y_test, scaler

def analyze_feature_importance(model, feature_names):
    """Analyze and plot feature importance for tree-based models"""
    if hasattr(model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(importance_df)
        
        # Plot feature importance
        plt.figure(figsize=(10, 6))
        sns.barplot(data=importance_df.head(10), x='importance', y='feature')
        plt.title('Top 10 Feature Importance')
        plt.xlabel('Importance')
        plt.tight_layout()
        plt.show()
        
        return importance_df
    else:
        print("Model doesn't have feature_importances_ attribute")
        return None

def predict_survival(model, scaler, label_encoders, passenger_data, model_name):
    """Make prediction for a new passenger"""
    # Create a dataframe with the passenger data
    passenger_df = pd.DataFrame([passenger_data])
    
    # Apply same preprocessing
    for feature, le in label_encoders.items():
        if feature in passenger_df.columns:
            # Handle unknown categories
            try:
                passenger_df[feature] = le.transform(passenger_df[feature])
            except ValueError:
                # If category not seen during training, use most frequent
                passenger_df[feature] = 0  # Default encoding
    
    # Scale if needed
    if model_name == 'Logistic Regression':
        passenger_features = scaler.transform(passenger_df)
    else:
        passenger_features = passenger_df.values
    
    # Make prediction
    prediction = model.predict(passenger_features)[0]
    probability = model.predict_proba(passenger_features)[0]
    
    return prediction, probability

def main():
    """Main function to run the complete analysis"""
    # Load and explore data
    df = load_and_explore_data('category_text.csv')
    
    # Preprocess data
    X, y, label_encoders, processed_data = preprocess_data(df)
    
    print(f"\nFeatures used for modeling: {list(X.columns)}")
    print(f"Feature matrix shape: {X.shape}")
    
    # Train models
    results, X_test, y_test, scaler = train_models(X, y)
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['cv_mean'])
    best_model = results[best_model_name]['model']
    
    print(f"\nBest model: {best_model_name}")
    print(f"Cross-validation score: {results[best_model_name]['cv_mean']:.4f}")
    
    # Analyze feature importance for the best model
    if best_model_name in ['Random Forest', 'Gradient Boosting']:
        importance_df = analyze_feature_importance(best_model, X.columns)
    
    # Example prediction
    print("\n" + "="*50)
    print("EXAMPLE PREDICTION")
    print("="*50)
    
    # Example passenger (similar to Jack from Titanic movie)
    example_passenger = {
        'Pclass': 3,
        'Sex': 'male',
        'Age': 20,
        'SibSp': 0,
        'Parch': 0,
        'Fare': 7.25,
        'Embarked': 'S',
        'Title': 'Mr',
        'FamilySize': 1,
        'IsAlone': 1,
        'AgeGroup': 'Adult',
        'FareGroup': 'Low',
        'HasCabin': 0
    }
    
    prediction, probability = predict_survival(best_model, scaler, label_encoders, 
                                             example_passenger, best_model_name)
    
    print(f"Example passenger: {example_passenger}")
    print(f"Predicted survival: {'Survived' if prediction == 1 else 'Did not survive'}")
    print(f"Survival probability: {probability[1]:.3f}")
    print(f"Death probability: {probability[0]:.3f}")
    
    return results, best_model, label_encoders, scaler

if __name__ == "__main__":
    results, best_model, label_encoders, scaler = main() 