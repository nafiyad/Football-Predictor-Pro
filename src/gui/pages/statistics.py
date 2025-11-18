"""Modern statistics page with interactive charts and visualizations."""
import customtkinter as ctk
from gui.theme import theme
from services.stats_service import StatsService
from services.data_service import DataService
from datetime import datetime


class StatisticCard(ctk.CTkFrame):
    """Card displaying a single statistic with visual appeal."""
    
    def __init__(self, parent, title: str, value: str, subtitle: str = "", icon: str = "📊", **kwargs):
        """Initialize statistic card."""
        super().__init__(parent, **theme.get_card_style(), **kwargs)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['md'])
        
        # Icon
        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=(theme.FONTS['primary'], 28)
        )
        icon_label.pack(anchor="w")
        
        # Value
        value_label = ctk.CTkLabel(
            container,
            text=value,
            font=(theme.FONTS['primary'], theme.FONTS['size_3xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        value_label.pack(anchor="w", pady=(theme.SPACING['xs'], 0))
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text=title,
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_tertiary']
        )
        title_label.pack(anchor="w")
        
        # Subtitle (if provided)
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                container,
                text=subtitle,
                font=(theme.FONTS['primary'], theme.FONTS['size_xs']),
                text_color=theme.COLORS['text_tertiary']
            )
            subtitle_label.pack(anchor="w", pady=(theme.SPACING['xs'], 0))


class StatisticsPage(ctk.CTkScrollableFrame):
    """Modern statistics page with comprehensive data visualization."""
    
    def __init__(self, parent):
        """Initialize statistics page."""
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=theme.COLORS['bg_primary']
        )
        
        self.stats_service = StatsService()
        self.data_service = DataService()
        
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()
    
    def create_widgets(self):
        """Create page widgets."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=theme.SPACING['xl'], pady=theme.SPACING['xl'])
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header
        self._create_header(main_container)
        
        # Overview statistics
        self._create_overview_section(main_container)
        
        # League statistics
        self._create_league_section(main_container)
        
        # Model performance
        self._create_model_section(main_container)
    
    def _create_header(self, parent):
        """Create page header."""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, theme.SPACING['xl']))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Statistics & Analytics",
            font=(theme.FONTS['primary'], theme.FONTS['size_4xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Comprehensive analysis of predictions and performance",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_tertiary'],
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(theme.SPACING['xs'], 0))
    
    def _create_overview_section(self, parent):
        """Create overview statistics section."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.grid(row=1, column=0, sticky="ew", pady=(0, theme.SPACING['xl']))
        
        # Section title
        title_label = ctk.CTkLabel(
            section_frame,
            text="Overview",
            font=(theme.FONTS['primary'], theme.FONTS['size_2xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(section_frame, fg_color="transparent")
        stats_grid.pack(fill="x")
        
        for i in range(4):
            stats_grid.grid_columnconfigure(i, weight=1)
        
        # Placeholder cards
        self.overview_cards = {}
        
        self.overview_cards['total_matches'] = StatisticCard(
            stats_grid,
            title="Total Matches Analyzed",
            value="0",
            icon="⚽"
        )
        self.overview_cards['total_matches'].grid(row=0, column=0, sticky="ew", padx=(0, theme.SPACING['md']))
        
        self.overview_cards['predictions'] = StatisticCard(
            stats_grid,
            title="Predictions Made",
            value="0",
            icon="🎯"
        )
        self.overview_cards['predictions'].grid(row=0, column=1, sticky="ew", padx=(0, theme.SPACING['md']))
        
        self.overview_cards['accuracy'] = StatisticCard(
            stats_grid,
            title="Overall Accuracy",
            value="0%",
            icon="✓"
        )
        self.overview_cards['accuracy'].grid(row=0, column=2, sticky="ew", padx=(0, theme.SPACING['md']))
        
        self.overview_cards['confidence'] = StatisticCard(
            stats_grid,
            title="Avg Confidence",
            value="0%",
            icon="📈"
        )
        self.overview_cards['confidence'].grid(row=0, column=3, sticky="ew")
    
    def _create_league_section(self, parent):
        """Create league statistics section."""
        section_frame = ctk.CTkFrame(
            parent,
            **theme.get_card_style()
        )
        section_frame.grid(row=2, column=0, sticky="ew", pady=(0, theme.SPACING['xl']))
        
        container = ctk.CTkFrame(section_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Section title
        title_label = ctk.CTkLabel(
            container,
            text="🏆 League Performance",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        # League list container
        self.league_container = ctk.CTkFrame(container, fg_color="transparent")
        self.league_container.pack(fill="x")
    
    def _create_model_section(self, parent):
        """Create model performance section."""
        section_frame = ctk.CTkFrame(
            parent,
            **theme.get_card_style()
        )
        section_frame.grid(row=3, column=0, sticky="ew")
        
        container = ctk.CTkFrame(section_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Section title
        title_label = ctk.CTkLabel(
            container,
            text="🤖 Model Performance",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        # Model info
        models_info = [
            ("Random Forest Advanced", "51.92%", theme.COLORS['success']),
            ("Stacking Ensemble", "49.23%", theme.COLORS['success']),
            ("Advanced XGBoost", "48.46%", theme.COLORS['warning']),
            ("Voting Ensemble", "48.08%", theme.COLORS['warning']),
            ("Gradient Boosting", "47.31%", theme.COLORS['warning']),
            ("Neural Network", "45.77%", theme.COLORS['error']),
            ("Advanced LightGBM", "45.38%", theme.COLORS['error']),
        ]
        
        for model_name, accuracy, color in models_info:
            model_frame = ctk.CTkFrame(
                container,
                fg_color=theme.COLORS['bg_tertiary'],
                corner_radius=theme.RADIUS['md'],
                height=50
            )
            model_frame.pack(fill="x", pady=(0, theme.SPACING['sm']))
            model_frame.pack_propagate(False)
            
            model_label = ctk.CTkLabel(
                model_frame,
                text=model_name,
                font=(theme.FONTS['primary'], theme.FONTS['size_base']),
                text_color=theme.COLORS['text_primary'],
                anchor="w"
            )
            model_label.pack(side="left", padx=theme.SPACING['md'])
            
            accuracy_label = ctk.CTkLabel(
                model_frame,
                text=accuracy,
                font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_bold']),
                text_color=color,
                anchor="e"
            )
            accuracy_label.pack(side="right", padx=theme.SPACING['md'])
    
    def refresh(self):
        """Refresh statistics data."""
        try:
            self._load_statistics()
        except Exception as e:
            print(f"Error refreshing statistics: {e}")
    
    def _load_statistics(self):
        """Load and display statistics."""
        try:
            from database.connection import get_session
            from models.database import Match, Prediction
            
            session = get_session()
            
            # Total matches
            total_matches = session.query(Match).filter_by(status='finished').count()
            self.overview_cards['total_matches'].value_label.configure(text=str(total_matches))
            
            # Total predictions
            total_predictions = session.query(Prediction).count()
            self.overview_cards['predictions'].value_label.configure(text=str(total_predictions))
            
            # Calculate accuracy
            predictions = session.query(Prediction).join(Match).filter(
                Match.status == 'finished'
            ).all()
            
            if predictions:
                correct = sum(1 for p in predictions if self._is_prediction_correct(p))
                accuracy = (correct / len(predictions)) * 100
                self.overview_cards['accuracy'].value_label.configure(text=f"{accuracy:.1f}%")
                
                # Average confidence
                avg_confidence = sum(p.confidence for p in predictions) / len(predictions)
                self.overview_cards['confidence'].value_label.configure(text=f"{avg_confidence * 100:.1f}%")
            
            session.close()
            
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def _is_prediction_correct(self, prediction) -> bool:
        """Check if prediction was correct."""
        match = prediction.match
        if not match or match.home_goals is None or match.away_goals is None:
            return False
        
        if match.home_goals > match.away_goals:
            actual = 'home'
        elif match.home_goals < match.away_goals:
            actual = 'away'
        else:
            actual = 'draw'
        
        probs = {
            'home': prediction.home_win_prob,
            'draw': prediction.draw_prob,
            'away': prediction.away_win_prob
        }
        predicted = max(probs, key=probs.get)
        
        return predicted == actual
