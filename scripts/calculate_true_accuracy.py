"""
Calculate the true accuracy of the prediction system.
This script evaluates all models on real historical data.
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from database.connection import get_session, init_db
from models.database import Match, Prediction
from services.prediction_service import PredictionService
from services.backtest_service import BacktestService
from utils.logger import setup_logger

logger = setup_logger()


def calculate_accuracy():
    """Calculate true accuracy on all finished matches."""
    init_db()
    session = get_session()
    
    logger.info("=" * 80)
    logger.info("CALCULATING TRUE ACCURACY")
    logger.info("=" * 80)
    
    # Get all finished matches
    finished_matches = session.query(Match).filter_by(status='finished').all()
    
    logger.info(f"\nTotal finished matches in database: {len(finished_matches)}")
    
    if len(finished_matches) == 0:
        logger.warning("No finished matches found. Cannot calculate accuracy.")
        return
    
    # Initialize services
    prediction_service = PredictionService(session)
    
    # Check if models are loaded
    if not prediction_service.models_loaded:
        logger.error("ML models not loaded. Please train models first.")
        logger.info("Run: python scripts/train_advanced_models.py")
        return
    
    logger.info(f"Models loaded: {list(prediction_service.models.keys())}")
    
    # Generate predictions for all matches
    logger.info("\n" + "=" * 80)
    logger.info("GENERATING PREDICTIONS FOR ALL FINISHED MATCHES")
    logger.info("=" * 80)
    
    predictions = []
    skipped = 0
    
    for i, match in enumerate(finished_matches, 1):
        if i % 50 == 0:
            logger.info(f"Processing match {i}/{len(finished_matches)}...")
        
        try:
            # Get or create prediction
            prediction = prediction_service.get_match_prediction(match.id, force_refresh=False)
            if prediction:
                predictions.append(prediction)
            else:
                skipped += 1
        except Exception as e:
            logger.warning(f"Could not generate prediction for match {match.id}: {e}")
            skipped += 1
    
    logger.info(f"\n✓ Generated/Retrieved {len(predictions)} predictions")
    logger.info(f"✗ Skipped {skipped} matches (insufficient data)")
    
    if len(predictions) == 0:
        logger.error("No predictions could be generated.")
        return
    
    # Calculate accuracy metrics
    logger.info("\n" + "=" * 80)
    logger.info("CALCULATING ACCURACY METRICS")
    logger.info("=" * 80)
    
    # 1X2 Accuracy
    correct_1x2 = 0
    total_1x2 = 0
    
    # BTTS Accuracy
    correct_btts = 0
    total_btts = 0
    
    # Over/Under 2.5 Accuracy
    correct_ou25 = 0
    total_ou25 = 0
    
    # Confidence levels
    high_confidence_correct = 0
    high_confidence_total = 0
    
    for prediction in predictions:
        match = prediction.match
        
        if match.home_goals is None or match.away_goals is None:
            continue
        
        # Determine actual result
        if match.home_goals > match.away_goals:
            actual_result = 'home'
        elif match.home_goals < match.away_goals:
            actual_result = 'away'
        else:
            actual_result = 'draw'
        
        # Determine predicted result (highest probability)
        probs = {
            'home': prediction.home_win_prob,
            'draw': prediction.draw_prob,
            'away': prediction.away_win_prob
        }
        predicted_result = max(probs, key=probs.get)
        
        # 1X2 Accuracy
        if predicted_result == actual_result:
            correct_1x2 += 1
            if prediction.confidence >= 0.7:
                high_confidence_correct += 1
        total_1x2 += 1
        
        if prediction.confidence >= 0.7:
            high_confidence_total += 1
        
        # BTTS Accuracy
        if prediction.btts_prob is not None:
            actual_btts = (match.home_goals > 0 and match.away_goals > 0)
            predicted_btts = prediction.btts_prob > 0.5
            if actual_btts == predicted_btts:
                correct_btts += 1
            total_btts += 1
        
        # Over/Under 2.5 Accuracy
        if prediction.over_2_5_prob is not None:
            total_goals = match.home_goals + match.away_goals
            actual_over = total_goals > 2.5
            predicted_over = prediction.over_2_5_prob > 0.5
            if actual_over == predicted_over:
                correct_ou25 += 1
            total_ou25 += 1
    
    # Calculate percentages
    accuracy_1x2 = (correct_1x2 / total_1x2 * 100) if total_1x2 > 0 else 0
    accuracy_btts = (correct_btts / total_btts * 100) if total_btts > 0 else 0
    accuracy_ou25 = (correct_ou25 / total_ou25 * 100) if total_ou25 > 0 else 0
    accuracy_high_conf = (high_confidence_correct / high_confidence_total * 100) if high_confidence_total > 0 else 0
    
    # Calculate average confidence
    avg_confidence = sum(p.confidence for p in predictions) / len(predictions) * 100
    
    # Print results
    logger.info("\n" + "=" * 80)
    logger.info("📊 TRUE ACCURACY RESULTS")
    logger.info("=" * 80)
    
    logger.info(f"\n🎯 1X2 PREDICTIONS (Match Result)")
    logger.info(f"   Total Predictions: {total_1x2}")
    logger.info(f"   Correct: {correct_1x2}")
    logger.info(f"   Accuracy: {accuracy_1x2:.2f}%")
    
    logger.info(f"\n⚽ BOTH TEAMS TO SCORE (BTTS)")
    logger.info(f"   Total Predictions: {total_btts}")
    logger.info(f"   Correct: {correct_btts}")
    logger.info(f"   Accuracy: {accuracy_btts:.2f}%")
    
    logger.info(f"\n📈 OVER/UNDER 2.5 GOALS")
    logger.info(f"   Total Predictions: {total_ou25}")
    logger.info(f"   Correct: {correct_ou25}")
    logger.info(f"   Accuracy: {accuracy_ou25:.2f}%")
    
    logger.info(f"\n🎖️ HIGH CONFIDENCE PREDICTIONS (≥70%)")
    logger.info(f"   Total High Confidence: {high_confidence_total}")
    logger.info(f"   Correct: {high_confidence_correct}")
    logger.info(f"   Accuracy: {accuracy_high_conf:.2f}%")
    
    logger.info(f"\n💡 AVERAGE CONFIDENCE")
    logger.info(f"   {avg_confidence:.2f}%")
    
    # Overall summary
    logger.info("\n" + "=" * 80)
    logger.info("📋 SUMMARY")
    logger.info("=" * 80)
    
    overall_accuracy = (correct_1x2 + correct_btts + correct_ou25) / (total_1x2 + total_btts + total_ou25) * 100
    
    logger.info(f"\n✓ Overall System Accuracy: {overall_accuracy:.2f}%")
    logger.info(f"✓ Primary (1X2) Accuracy: {accuracy_1x2:.2f}%")
    logger.info(f"✓ Total Matches Evaluated: {total_1x2}")
    logger.info(f"✓ Models Used: {len(prediction_service.models)}")
    
    # Benchmark comparison
    logger.info("\n" + "=" * 80)
    logger.info("🏆 BENCHMARK COMPARISON")
    logger.info("=" * 80)
    logger.info(f"\nYour System: {accuracy_1x2:.2f}%")
    logger.info(f"Random Guess (33.3%): {'✓ BETTER' if accuracy_1x2 > 33.3 else '✗ WORSE'}")
    logger.info(f"Home Win Bias (45%): {'✓ BETTER' if accuracy_1x2 > 45 else '✗ WORSE'}")
    logger.info(f"Professional Tipsters (50-55%): {'✓ COMPETITIVE' if accuracy_1x2 > 50 else '✗ BELOW'}")
    logger.info(f"Expert Systems (55-60%): {'✓ EXCELLENT' if accuracy_1x2 > 55 else '✗ BELOW'}")
    
    # Performance rating
    logger.info("\n" + "=" * 80)
    logger.info("⭐ PERFORMANCE RATING")
    logger.info("=" * 80)
    
    if accuracy_1x2 >= 60:
        rating = "EXCEPTIONAL ⭐⭐⭐⭐⭐"
    elif accuracy_1x2 >= 55:
        rating = "EXCELLENT ⭐⭐⭐⭐"
    elif accuracy_1x2 >= 50:
        rating = "VERY GOOD ⭐⭐⭐"
    elif accuracy_1x2 >= 45:
        rating = "GOOD ⭐⭐"
    elif accuracy_1x2 >= 40:
        rating = "FAIR ⭐"
    else:
        rating = "NEEDS IMPROVEMENT"
    
    logger.info(f"\n{rating}")
    logger.info(f"\nNote: Football prediction is inherently difficult.")
    logger.info(f"Even professional systems rarely exceed 60% accuracy.")
    
    logger.info("\n" + "=" * 80)
    
    session.close()


if __name__ == "__main__":
    calculate_accuracy()


