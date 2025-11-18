"""Train advanced ML models with sophisticated features."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

import numpy as np
from sklearn.model_selection import train_test_split
from models.database import Match
from database.connection import get_session, init_db
from services.advanced_features import AdvancedFeatureEngineer
from ml.advanced_models import AdvancedModelTrainer
from utils.logger import setup_logger

logger = setup_logger(__name__)


def prepare_advanced_training_data():
    """Prepare training data with advanced features."""
    logger.info("\n" + "="*70)
    logger.info("PREPARING ADVANCED TRAINING DATA")
    logger.info("="*70 + "\n")
    
    init_db()
    session = get_session()
    feature_engineer = AdvancedFeatureEngineer(session)
    
    # Get all finished matches
    matches = session.query(Match).filter(
        Match.status == 'finished',
        Match.home_goals.isnot(None),
        Match.away_goals.isnot(None)
    ).order_by(Match.date).all()
    
    logger.info(f"Found {len(matches)} finished matches")
    
    X = []
    y_1x2 = []
    y_btts = []
    y_ou25 = []
    
    skipped = 0
    
    for i, match in enumerate(matches):
        if (i + 1) % 100 == 0:
            logger.info(f"Processing match {i+1}/{len(matches)}")
        
        try:
            # Generate advanced features
            features = feature_engineer.engineer_advanced_features(match.id)
            
            # Determine outcomes
            if match.home_goals > match.away_goals:
                outcome_1x2 = 0  # Home win
            elif match.home_goals < match.away_goals:
                outcome_1x2 = 2  # Away win
            else:
                outcome_1x2 = 1  # Draw
            
            btts = 1 if (match.home_goals > 0 and match.away_goals > 0) else 0
            total_goals = match.home_goals + match.away_goals
            over_25 = 1 if total_goals > 2.5 else 0
            
            X.append(features)
            y_1x2.append(outcome_1x2)
            y_btts.append(btts)
            y_ou25.append(over_25)
            
        except Exception as e:
            skipped += 1
            if skipped % 50 == 0:
                logger.warning(f"Skipped {skipped} matches due to errors")
            continue
    
    logger.info(f"\n✓ Prepared {len(X)} training samples (skipped {skipped})")
    
    X = np.array(X)
    y_1x2 = np.array(y_1x2)
    y_btts = np.array(y_btts)
    y_ou25 = np.array(y_ou25)
    
    # Get feature names
    feature_names = feature_engineer.get_feature_names()
    logger.info(f"✓ Generated {len(feature_names)} advanced features")
    
    session.close()
    
    return X, y_1x2, y_btts, y_ou25, feature_names


def train_advanced_models():
    """Train all advanced models."""
    logger.info("\n" + "="*70)
    logger.info("ADVANCED MODEL TRAINING")
    logger.info("="*70 + "\n")
    
    # Prepare data
    X, y_1x2, y_btts, y_ou25, feature_names = prepare_advanced_training_data()
    
    # Split data
    X_train, X_test, y_train_1x2, y_test_1x2 = train_test_split(
        X, y_1x2, test_size=0.2, random_state=42, stratify=y_1x2
    )
    
    logger.info(f"\nTraining set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    
    # Initialize trainer
    trainer = AdvancedModelTrainer()
    
    # Scale features
    logger.info("\nScaling features...")
    X_train_scaled = trainer.scaler.fit_transform(X_train)
    X_test_scaled = trainer.scaler.transform(X_test)
    
    # Save scaler
    trainer.save_scaler()
    
    # Train models
    logger.info("\n" + "="*70)
    logger.info("TRAINING ADVANCED 1X2 MODELS")
    logger.info("="*70 + "\n")
    
    # 1. Advanced XGBoost
    logger.info("Training Advanced XGBoost...")
    xgb_model = trainer.create_advanced_xgboost()
    xgb_model, xgb_cv_scores = trainer.train_with_cross_validation(
        xgb_model, X_train_scaled, y_train_1x2, cv=5
    )
    xgb_test_score = xgb_model.score(X_test_scaled, y_test_1x2)
    logger.info(f"Test Accuracy: {xgb_test_score:.4f}\n")
    trainer.save_model(xgb_model, 'xgboost_advanced')
    
    # 2. Advanced LightGBM
    logger.info("Training Advanced LightGBM...")
    lgbm_model = trainer.create_advanced_lightgbm()
    lgbm_model, lgbm_cv_scores = trainer.train_with_cross_validation(
        lgbm_model, X_train_scaled, y_train_1x2, cv=5
    )
    lgbm_test_score = lgbm_model.score(X_test_scaled, y_test_1x2)
    logger.info(f"Test Accuracy: {lgbm_test_score:.4f}\n")
    trainer.save_model(lgbm_model, 'lgbm_advanced')
    
    # 3. Advanced Random Forest
    logger.info("Training Advanced Random Forest...")
    rf_model = trainer.create_advanced_random_forest()
    rf_model, rf_cv_scores = trainer.train_with_cross_validation(
        rf_model, X_train_scaled, y_train_1x2, cv=5
    )
    rf_test_score = rf_model.score(X_test_scaled, y_test_1x2)
    logger.info(f"Test Accuracy: {rf_test_score:.4f}\n")
    trainer.save_model(rf_model, 'rf_advanced')
    
    # 4. Gradient Boosting
    logger.info("Training Gradient Boosting...")
    gb_model = trainer.create_gradient_boosting()
    gb_model, gb_cv_scores = trainer.train_with_cross_validation(
        gb_model, X_train_scaled, y_train_1x2, cv=5
    )
    gb_test_score = gb_model.score(X_test_scaled, y_test_1x2)
    logger.info(f"Test Accuracy: {gb_test_score:.4f}\n")
    trainer.save_model(gb_model, 'gb_advanced')
    
    # 5. Neural Network
    logger.info("Training Deep Neural Network...")
    nn_model = trainer.create_neural_network(X_train_scaled.shape[1])
    nn_model.fit(X_train_scaled, y_train_1x2)
    nn_test_score = nn_model.score(X_test_scaled, y_test_1x2)
    logger.info(f"Test Accuracy: {nn_test_score:.4f}\n")
    trainer.save_model(nn_model, 'neural_net_1x2')
    
    # 6. Stacking Ensemble
    logger.info("Training Stacking Ensemble...")
    stacking_model = trainer.create_stacking_ensemble(X_train_scaled, y_train_1x2)
    stacking_model.fit(X_train_scaled, y_train_1x2)
    stacking_test_score = stacking_model.score(X_test_scaled, y_test_1x2)
    logger.info(f"Test Accuracy: {stacking_test_score:.4f}\n")
    trainer.save_model(stacking_model, 'stacking_1x2')
    
    # 7. Voting Ensemble
    logger.info("Training Voting Ensemble...")
    voting_model = trainer.create_voting_ensemble()
    voting_model.fit(X_train_scaled, y_train_1x2)
    voting_test_score = voting_model.score(X_test_scaled, y_test_1x2)
    logger.info(f"Test Accuracy: {voting_test_score:.4f}\n")
    trainer.save_model(voting_model, 'voting_1x2')
    
    # Feature Importance Analysis
    logger.info("\n" + "="*70)
    logger.info("FEATURE IMPORTANCE ANALYSIS")
    logger.info("="*70 + "\n")
    
    importance_df = trainer.get_feature_importance(xgb_model, feature_names)
    if importance_df is not None:
        logger.info("Top 20 Most Important Features:")
        logger.info(importance_df.head(20).to_string(index=False))
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("MODEL PERFORMANCE SUMMARY")
    logger.info("="*70 + "\n")
    
    results = [
        ("XGBoost Advanced", xgb_test_score, xgb_cv_scores.mean()),
        ("LightGBM Advanced", lgbm_test_score, lgbm_cv_scores.mean()),
        ("Random Forest Advanced", rf_test_score, rf_cv_scores.mean()),
        ("Gradient Boosting", gb_test_score, gb_cv_scores.mean()),
        ("Neural Network", nn_test_score, None),
        ("Stacking Ensemble", stacking_test_score, None),
        ("Voting Ensemble", voting_test_score, None)
    ]
    
    for name, test_score, cv_score in results:
        if cv_score:
            logger.info(f"{name:25s} - Test: {test_score:.4f}, CV: {cv_score:.4f}")
        else:
            logger.info(f"{name:25s} - Test: {test_score:.4f}")
    
    # Find best model
    best_model = max(results, key=lambda x: x[1])
    logger.info(f"\n🏆 Best Model: {best_model[0]} with {best_model[1]:.4f} accuracy")
    
    logger.info("\n" + "="*70)
    logger.info("✓ ADVANCED MODEL TRAINING COMPLETED!")
    logger.info("="*70 + "\n")
    
    logger.info("Models saved:")
    logger.info("  - xgboost_advanced.pkl")
    logger.info("  - lgbm_advanced.pkl")
    logger.info("  - rf_advanced.pkl")
    logger.info("  - gb_advanced.pkl")
    logger.info("  - neural_net_1x2.pkl")
    logger.info("  - stacking_1x2.pkl")
    logger.info("  - voting_1x2.pkl")
    logger.info("  - scaler.pkl")
    logger.info("\nThese models use advanced features and ensemble methods")
    logger.info("for significantly better prediction accuracy!\n")


def main():
    """Main function."""
    train_advanced_models()


if __name__ == '__main__':
    main()


