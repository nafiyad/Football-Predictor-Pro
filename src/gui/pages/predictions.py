"""Modern predictions page with AI-powered insights."""
import customtkinter as ctk
from services.data_service import DataService
from services.prediction_service import PredictionService
from gui.components.match_card import ModernMatchCard
from gui.components.prediction_panel import PredictionDialog
from gui.theme import theme


class PredictionsPage(ctk.CTkScrollableFrame):
    """Modern predictions center with AI insights."""
    
    def __init__(self, parent):
        """Initialize predictions page."""
        super().__init__(parent, corner_radius=0, fg_color=theme.COLORS['bg_primary'])
        
        self.data_service = DataService()
        self.prediction_service = PredictionService()
        
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()
    
    def create_widgets(self):
        """Create page widgets."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=theme.SPACING['xl'], pady=theme.SPACING['xl'])
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            main_container,
            text="🎯 AI Predictions",
            font=(theme.FONTS['primary'], theme.FONTS['size_4xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        header_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        subtitle_label = ctk.CTkLabel(
            main_container,
            text="Advanced machine learning predictions for upcoming matches",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_tertiary'],
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(0, theme.SPACING['xl']))
        
        # Info card
        info_card = ctk.CTkFrame(main_container, **theme.get_card_style())
        info_card.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        info_container = ctk.CTkFrame(info_card, fg_color="transparent")
        info_container.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['md'])
        
        info_label = ctk.CTkLabel(
            info_container,
            text="💡 Click on any match to generate detailed AI predictions using 7 advanced models and 78 features",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_secondary'],
            wraplength=700,
            justify="left"
        )
        info_label.pack(anchor="w")
        
        # Predictions container
        self.predictions_container = ctk.CTkFrame(main_container, fg_color="transparent")
        self.predictions_container.pack(fill="both", expand=True)
    
    def refresh(self):
        """Refresh predictions."""
        try:
            self._load_predictions()
        except Exception as e:
            print(f"Error refreshing predictions: {e}")
    
    def _load_predictions(self):
        """Load upcoming matches for predictions."""
        try:
            # Clear existing
            for widget in self.predictions_container.winfo_children():
                widget.destroy()
            
            # Get upcoming matches
            matches = self.data_service.get_upcoming_matches(limit=20)
            
            if not matches:
                no_matches_label = ctk.CTkLabel(
                    self.predictions_container,
                    text="No upcoming matches available for prediction",
                    font=(theme.FONTS['primary'], theme.FONTS['size_lg']),
                    text_color=theme.COLORS['text_tertiary']
                )
                no_matches_label.pack(pady=theme.SPACING['xl'])
                return
            
            # Display matches
            for match in matches:
                match_data = {
                    'id': match.id,
                    'league': match.league.name if match.league else 'Unknown',
                    'home_team': match.home_team.name if match.home_team else 'Unknown',
                    'away_team': match.away_team.name if match.away_team else 'Unknown',
                    'date': match.date,
                    'status': match.status,
                    'home_goals': match.home_goals,
                    'away_goals': match.away_goals
                }
                
                card = ModernMatchCard(
                    self.predictions_container,
                    match_data=match_data,
                    on_click=self._show_prediction_dialog
                )
                card.pack(fill="x", pady=(0, theme.SPACING['md']))
        
        except Exception as e:
            print(f"Error loading predictions: {e}")
    
    def _show_prediction_dialog(self, match_data: dict):
        """Show prediction dialog."""
        try:
            dialog = PredictionDialog(self, match_data, self.prediction_service)
            dialog.focus()
        except Exception as e:
            print(f"Error showing prediction dialog: {e}")
