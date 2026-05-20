"""Visualization for match timeline and risk charts."""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import base64
from io import BytesIO

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class MatchTimelineChart:
    """Generate match timeline visualizations."""
    
    def __init__(self):
        self.colors = {
            'win': '#2ecc71',
            'draw': '#f39c12',
            'loss': '#e74c3c',
            'home': '#3498db',
            'away': '#9b59b6'
        }
    
    def create_timeline_chart(self, team_name: str, timeline_data: List[Dict], save_path: Optional[str] = None) -> Optional[str]:
        """Create match timeline showing win probability over last 10 fixtures."""
        if not timeline_data:
            return None
        
        dates = [datetime.fromisoformat(d['date']) for d in timeline_data]
        win_probs = [d.get('win_probability', 0.5) for d in timeline_data]
        results = [d.get('result', 'D') for d in timeline_data]
        bar_colors = [self.colors.get(r.lower(), '#95a5a6') for r in results]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(dates)), win_probs, color=bar_colors, alpha=0.7, edgecolor='black')
        
        if len(win_probs) > 1:
            z = np.polyfit(range(len(win_probs)), win_probs, 2)
            p = np.poly1d(z)
            ax.plot(range(len(dates)), p(range(len(dates))), color='red', linestyle='--', alpha=0.7, label='Trend'
        
        ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
        ax.set_xlabel('Last 10 Matches')
        ax.set_ylabel('Win Probability')
        ax.set_title(f'{team_name} - Win Probability Trend')
        ax.set_ylim(0, 1)
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['win'], label='Win'),
            Patch(facecolor=self.colors['draw'], label='Draw'),
            Patch(facecolor=self.colors['loss'], label='Loss')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            return save_path
        
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_base64
    
    def create_probability_gauge(self, home_prob: float, draw_prob: float, away_prob: float) -> str:
        """Create probability gauge visualization."""
        labels = ['Home Win', 'Draw', 'Away Win']
        probs = [home_prob, draw_prob, away_prob]
        colors = [self.colors['home'], self.colors['draw'], self.colors['away']]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        y_pos = np.arange(len(labels))
        ax.barh(y_pos, probs, color=colors, alpha=0.8, edgecolor='black')
        
        for i, prob in enumerate(probs):
            ax.text(prob + 0.02, i, f'{prob:.1%}', va='center', fontweight='bold')
        
        ax.set_xlabel('Probability')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlim(0, 1)
        ax.set_title('Match Outcome Probabilities')
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_base64
    
    def create_form_comparison(self, home_stats: Dict, away_stats: Dict) -> str:
        """Create side-by-side form comparison."""
        categories = ['Goals Scored', 'Goals Conceded', 'Win Rate', 'Clean Sheet %']
        
        home_vals = [
            home_stats.get('avg_goals_scored', 0),
            home_stats.get('avg_goals_conceded', 0),
            home_stats.get('win_rate', 0),
            home_stats.get('clean_sheet_rate', 0)
        ]
        away_vals = [
            away_stats.get('avg_goals_scored', 0),
            away_stats.get('avg_goals_conceded', 0),
            away_stats.get('win_rate', 0),
            away_stats.get('clean_sheet_rate', 0)
        ]
        
        x = np.arange(len(categories))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(x - width/2, home_vals, width, label=home_stats.get('name', 'Home'), color=self.colors['home'], alpha=0.8)
        ax.bar(x + width/2, away_vals, width, label=away_stats.get('name', 'Away'), color=self.colors['away'], alpha=0.8)
        
        ax.set_ylabel('Value')
        ax.set_title('Team Statistics Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_base64