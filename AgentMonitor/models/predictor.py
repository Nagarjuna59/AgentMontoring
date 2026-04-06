# AgentMonitor/models/predictor.py
"""
MAS Performance Predictor using XGBoost regression.
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import spearmanr
try:
    import xgboost as xgb
except Exception:
    xgb = None
    # xgboost is optional for training/prediction. If you need full predictor
    # capabilities, install xgboost: pip install xgboost


class MASPredictor:
    """
    Predict MAS performance using XGBoost regression on extracted features.
    """
    
    FEATURE_COLUMNS = [
        "avg_personal_score", "min_personal_score", "max_loops",
        "total_latency", "total_token_usage", "num_agents_triggered_enhancement",
        "num_nodes", "num_edges", "clustering_coefficient", "transitivity",
        "avg_degree_centrality", "avg_betweenness_centrality", "avg_closeness_centrality",
        "pagerank_entropy", "heterogeneity_score", "collective_score"
    ]
    
    TARGET_COLUMN = "label_mas_score"
    
    def __init__(self, model_path: Optional[Path] = None):
        """
        Args:
            model_path: Path to save/load model
        """
        self.model_path = model_path
        # If xgboost is unavailable, model will remain None and predict/train
        # operations will raise informative errors.
        self.model: Optional[Any] = None
        self.feature_importance_: Optional[pd.DataFrame] = None
        self.training_metrics_: Optional[Dict[str, float]] = None
        
    def train(
        self,
        data_path: Path,
        test_size: float = 0.2,
        cv_folds: int = 5,
        tune_hyperparams: bool = True,
        save_model: bool = True
    ) -> Dict[str, Any]:
        """
        Train XGBoost model on MAS benchmark data.
        
        Args:
            data_path: Path to mas_benchmark_results.csv
            test_size: Fraction for test set
            cv_folds: Number of cross-validation folds
            tune_hyperparams: Whether to run grid search
            save_model: Whether to save trained model
            
        Returns:
            Training metrics dict
        """
        print(f"\n{'='*60}")
        print("Training MAS Performance Predictor")
        print(f"{'='*60}\n")
        
        # Load data
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} samples from {data_path}")
        print(f"Columns: {list(df.columns)}\n")
        
        # Validate columns
        missing_features = set(self.FEATURE_COLUMNS) - set(df.columns)
        if missing_features:
            raise ValueError(f"Missing feature columns: {missing_features}")
        
        if self.TARGET_COLUMN not in df.columns:
            raise ValueError(f"Missing target column: {self.TARGET_COLUMN}")
        
        # Prepare features and target
        X = df[self.FEATURE_COLUMNS].values
        y = df[self.TARGET_COLUMN].values
        
        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")
        print(f"Target statistics: mean={y.mean():.4f}, std={y.std():.4f}, min={y.min():.4f}, max={y.max():.4f}\n")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        print(f"Train set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples\n")
        
        # Hyperparameter tuning
        if tune_hyperparams:
            print("Running hyperparameter tuning...")
            best_params = self._tune_hyperparameters(X_train, y_train, cv_folds)
            print(f"Best parameters: {best_params}\n")
        else:
            best_params = {
                'max_depth': 6,
                'learning_rate': 0.1,
                'n_estimators': 100,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'reg_alpha': 0.1,
                'reg_lambda': 1.0
            }
        
        # Train final model
        print("Training final model...")
        self.model = xgb.XGBRegressor(
            objective='reg:squarederror',
            random_state=42,
            **best_params
        )
        self.model.fit(X_train, y_train)
        print("Training complete.\n")
        
        # Evaluate
        print("Evaluating model...")
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        metrics = {
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test),
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'train_spearman': spearmanr(y_train, y_pred_train)[0],
            'test_spearman': spearmanr(y_test, y_pred_test)[0]
        }
        
        self.training_metrics_ = metrics
        
        print("Training Metrics:")
        print(f"  RMSE:      {metrics['train_rmse']:.4f}")
        print(f"  MAE:       {metrics['train_mae']:.4f}")
        print(f"  R²:        {metrics['train_r2']:.4f}")
        print(f"  Spearman:  {metrics['train_spearman']:.4f}\n")
        
        print("Test Metrics:")
        print(f"  RMSE:      {metrics['test_rmse']:.4f}")
        print(f"  MAE:       {metrics['test_mae']:.4f}")
        print(f"  R²:        {metrics['test_r2']:.4f}")
        print(f"  Spearman:  {metrics['test_spearman']:.4f}\n")
        
        # Feature importance
        self._compute_feature_importance()
        print("Top 10 Most Important Features:")
        print(self.feature_importance_.head(10).to_string(index=False))
        print()
        
        # Save model
        if save_model and self.model_path:
            self.save()
        
        print(f"{'='*60}\n")
        return metrics
    
    def _tune_hyperparameters(
        self,
        X: np.ndarray,
        y: np.ndarray,
        cv_folds: int = 5
    ) -> Dict[str, Any]:
        """Run grid search for hyperparameter tuning."""
        param_grid = {
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3],
            'n_estimators': [50, 100, 200],
            'subsample': [0.7, 0.8, 1.0],
            'colsample_bytree': [0.7, 0.8, 1.0],
        }
        
        xgb_model = xgb.XGBRegressor(
            objective='reg:squarederror',
            random_state=42
        )
        
        grid_search = GridSearchCV(
            xgb_model,
            param_grid,
            cv=cv_folds,
            scoring='neg_mean_squared_error',
            verbose=1,
            n_jobs=-1
        )
        
        grid_search.fit(X, y)
        return grid_search.best_params_
    
    def _compute_feature_importance(self) -> None:
        """Compute and store feature importance."""
        if self.model is None:
            return
        
        importance = self.model.feature_importances_
        self.feature_importance_ = pd.DataFrame({
            'feature': self.FEATURE_COLUMNS,
            'importance': importance
        }).sort_values('importance', ascending=False)
    
    def predict(self, features: Dict[str, float]) -> float:
        """
        Predict MAS performance from features.
        
        Args:
            features: Dict with 16 feature values
            
        Returns:
            Predicted label_mas_score
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first or load() a saved model.")
        
        # Extract features in correct order
        X = np.array([[features[col] for col in self.FEATURE_COLUMNS]])
        
        prediction = self.model.predict(X)[0]
        return float(prediction)
    
    def predict_batch(self, features_list: List[Dict[str, float]]) -> np.ndarray:
        """Predict for multiple MAS variants."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first or load() a saved model.")
        
        X = np.array([[f[col] for col in self.FEATURE_COLUMNS] for f in features_list])
        predictions = self.model.predict(X)
        return predictions
    
    def save(self, path: Optional[Path] = None, format: str = 'pkl') -> None:
        """
        Save model to disk in multiple formats.
        
        Args:
            path: Path to save model
            format: 'pkl' (pickle), 'json' (XGBoost JSON), or 'both'
        """
        if self.model is None:
            raise ValueError("No model to save.")
        
        save_path = path or self.model_path
        if save_path is None:
            raise ValueError("No save path specified.")
        
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save pickle (full state)
        if format in ['pkl', 'both']:
            pkl_path = save_path.with_suffix('.pkl')
            with open(pkl_path, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'feature_importance': self.feature_importance_,
                    'training_metrics': self.training_metrics_,
                    'feature_columns': self.FEATURE_COLUMNS,
                    'target_column': self.TARGET_COLUMN
                }, f)
            print(f"[SAVED] Model saved to {pkl_path}")
        
        # Save XGBoost native format
        if format in ['json', 'both']:
            json_path = save_path.with_suffix('.json')
            self.model.save_model(str(json_path))
            print(f"[SAVED] XGBoost model saved to {json_path}")
            
            # Save metadata separately
            meta_path = save_path.with_suffix('.meta.json')
            import json as json_lib
            with open(meta_path, 'w') as f:
                json_lib.dump({
                    'feature_columns': self.FEATURE_COLUMNS,
                    'target_column': self.TARGET_COLUMN,
                    'training_metrics': self.training_metrics_,
                    'feature_importance': self.feature_importance_.to_dict() if self.feature_importance_ is not None else None
                }, f, indent=2)
            print(f"[SAVED] Metadata saved to {meta_path}")
    
    def load(self, path: Optional[Path] = None) -> None:
        """Load model from disk."""
        load_path = path or self.model_path
        if load_path is None:
            raise ValueError("No load path specified.")
        
        load_path = Path(load_path)
        if not load_path.exists():
            raise FileNotFoundError(f"Model file not found: {load_path}")
        
        with open(load_path, 'rb') as f:
            data = pickle.load(f)
        
        self.model = data['model']
        self.feature_importance_ = data.get('feature_importance')
        self.training_metrics_ = data.get('training_metrics')
        
        print(f"[LOADED] Model loaded from {load_path}")
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance DataFrame."""
        if self.feature_importance_ is None:
            raise ValueError("Feature importance not available. Train model first.")
        return self.feature_importance_
    
    def get_training_metrics(self) -> Dict[str, float]:
        """Get training metrics."""
        if self.training_metrics_ is None:
            raise ValueError("Training metrics not available. Train model first.")
        return self.training_metrics_
