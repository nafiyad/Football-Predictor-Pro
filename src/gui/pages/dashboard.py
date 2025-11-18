"""Modern dashboard page with advanced statistics and visualizations."""
import customtkinter as ctk
from services.data_service import DataService
from services.stats_service import StatsService
from gui.components.match_card import ModernMatchCard
from gui.components.prediction_panel import PredictionDialog
from services.prediction_service import PredictionService
from gui.theme import theme
from datetime import datetime, timedelta


class StatCard(ctk.CTkFrame):
    """Modern statistics card with icon and trend indicator."""
    
    def __init__(self, parent, title: str, value: str, icon: str, trend: str = None, **kwargs):
        """Initialize stat card."""
        super().__init__(
            parent,
            **theme.get_card_style(),
            **kwargs
        )
        
        # Container with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Icon
        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=(theme.FONTS['primary'], 32)
        )
        icon_label.pack(anchor="w")
        
        # Value
        self.value_label = ctk.CTkLabel(
            container,
            text=value,
            font=(theme.FONTS['primary'], theme.FONTS['size_3xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        self.value_label.pack(anchor="w", pady=(theme.SPACING['xs'], 0))
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text=title,
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_tertiary']
        )
        title_label.pack(anchor="w")
        
        # Trend indicator (if provided)
        self.trend_label = None
        if trend:
            trend_color = theme.COLORS['success'] if '+' in trend else theme.COLORS['error']
            self.trend_label = ctk.CTkLabel(
                container,
                text=trend,
                font=(theme.FONTS['primary'], theme.FONTS['size_sm'], theme.FONTS['weight_medium']),
                text_color=trend_color
            )
            self.trend_label.pack(anchor="w", pady=(theme.SPACING['xs'], 0))
    
    def update_value(self, value: str, trend: str = None):
        """Update card value and trend."""
        self.value_label.configure(text=value)
        if trend and self.trend_label:
            trend_color = theme.COLORS['success'] if '+' in trend else theme.COLORS['error']
            self.trend_label.configure(text=trend, text_color=trend_color)


class DashboardPage(ctk.CTkScrollableFrame):
    """Modern dashboard with advanced statistics and live data."""
    
    def __init__(self, parent):
        """Initialize dashboard page."""
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=theme.COLORS['bg_primary']
        )
        
        self.data_service = DataService()
        self.stats_service = StatsService()
        self.prediction_service = PredictionService()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        self.stat_cards = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Create modern dashboard widgets."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=theme.SPACING['xl'], pady=theme.SPACING['xl'])
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header section
        self._create_header(main_container)
        
        # Statistics cards section
        self._create_stats_section(main_container)
        
        # Quick insights section
        self._create_insights_section(main_container)
        
        # Upcoming matches section
        self._create_matches_section(main_container)
    
    def _create_header(self, parent):
        """Create modern header with greeting and date."""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, theme.SPACING['xl']))
        
        # Greeting and title
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good Morning"
        elif current_hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{greeting} 👋",
            font=(theme.FONTS['primary'], theme.FONTS['size_4xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=f"Today is {datetime.now().strftime('%A, %B %d, %Y')}",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_tertiary'],
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(theme.SPACING['xs'], 0))
    
    def _create_stats_section(self, parent):
        """Create statistics cards section."""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, theme.SPACING['xl']))
        
        # Configure grid for 4 columns
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Create stat cards
        self.stat_cards['predictions'] = StatCard(
            stats_frame,
            title="Total Predictions",
            value="0",
            icon="🎯"
        )
        self.stat_cards['predictions'].grid(row=0, column=0, sticky="ew", padx=(0, theme.SPACING['md']))
        
        self.stat_cards['accuracy'] = StatCard(
            stats_frame,
            title="Model Accuracy",
            value="0%",
            icon="✓"
        )
        self.stat_cards['accuracy'].grid(row=0, column=1, sticky="ew", padx=(0, theme.SPACING['md']))
        
        self.stat_cards['roi'] = StatCard(
            stats_frame,
            title="ROI",
            value="0%",
            icon="💰"
        )
        self.stat_cards['roi'].grid(row=0, column=2, sticky="ew", padx=(0, theme.SPACING['md']))
        
        self.stat_cards['matches'] = StatCard(
            stats_frame,
            title="Upcoming Matches",
            value="0",
            icon="⚽"
        )
        self.stat_cards['matches'].grid(row=0, column=3, sticky="ew")
    
    def _create_insights_section(self, parent):
        """Create quick insights section."""
        insights_frame = ctk.CTkFrame(
            parent,
            **theme.get_card_style()
        )
        insights_frame.grid(row=2, column=0, sticky="ew", pady=(0, theme.SPACING['xl']))
        
        # Container with padding
        container = ctk.CTkFrame(insights_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Section title
        title_label = ctk.CTkLabel(
            container,
            text="📊 Quick Insights",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        # Insights content
        self.insights_container = ctk.CTkFrame(container, fg_color="transparent")
        self.insights_container.pack(fill="x")
        
        # Placeholder insights
        self._add_insight("🏆 Best performing model: Random Forest (51.92% accuracy)")
        self._add_insight("📈 78 advanced features used for predictions")
        self._add_insight("🎯 7 ensemble models working together")
        self._add_insight("💡 Real-time data from 5 major leagues")
    
    def _add_insight(self, text: str):
        """Add an insight item."""
        insight_frame = ctk.CTkFrame(
            self.insights_container,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md'],
            height=40
        )
        insight_frame.pack(fill="x", pady=(0, theme.SPACING['sm']))
        insight_frame.pack_propagate(False)
        
        insight_label = ctk.CTkLabel(
            insight_frame,
            text=text,
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_secondary'],
            anchor="w"
        )
        insight_label.pack(side="left", padx=theme.SPACING['md'], fill="x", expand=True)
    
    def _create_matches_section(self, parent):
        """Create upcoming matches section."""
        # Section header
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.grid(row=3, column=0, sticky="ew", pady=(0, theme.SPACING['md']))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚽ Upcoming Matches",
            font=(theme.FONTS['primary'], theme.FONTS['size_2xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(side="left")
        
        view_all_btn = ctk.CTkButton(
            header_frame,
            text="View All →",
            **theme.get_button_style('outline'),
            width=120,
            height=36
        )
        view_all_btn.pack(side="right")
        
        # Matches container
        self.matches_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.matches_container.grid(row=4, column=0, sticky="ew")
    
    def refresh(self):
        """Refresh dashboard data."""
        try:
            # Update statistics
            self._update_statistics()
            
            # Load upcoming matches
            self._load_upcoming_matches()
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
    
    def _update_statistics(self):
        """Update statistics cards."""
        try:
            # Get prediction count
            from database.connection import get_session
            from models.database import Prediction, Match
            
            session = get_session()
            
            # Total predictions
            total_predictions = session.query(Prediction).count()
            self.stat_cards['predictions'].update_value(str(total_predictions))
            
            # Model accuracy (from recent predictions)
            recent_predictions = session.query(Prediction).join(Match).filter(
                Match.status == 'finished'
            ).limit(100).all()
            
            if recent_predictions:
                correct = sum(1 for p in recent_predictions if self._is_prediction_correct(p))
                accuracy = (correct / len(recent_predictions)) * 100
                self.stat_cards['accuracy'].update_value(f"{accuracy:.1f}%")
            
            # Upcoming matches count
            upcoming_count = session.query(Match).filter(
                Match.status == 'scheduled',
                Match.date >= datetime.now()
            ).count()
            self.stat_cards['matches'].update_value(str(upcoming_count))
            
            session.close()
        except Exception as e:
            print(f"Error updating statistics: {e}")
    
    def _is_prediction_correct(self, prediction) -> bool:
        """Check if a prediction was correct."""
        match = prediction.match
        if not match or match.home_goals is None or match.away_goals is None:
            return False
        
        # Determine actual result
        if match.home_goals > match.away_goals:
            actual = 'home'
        elif match.home_goals < match.away_goals:
            actual = 'away'
        else:
            actual = 'draw'
        
        # Get predicted result
        probs = {
            'home': prediction.home_win_prob,
            'draw': prediction.draw_prob,
            'away': prediction.away_win_prob
        }
        predicted = max(probs, key=probs.get)
        
        return predicted == actual
    
    def _load_upcoming_matches(self):
        """Load and display upcoming matches."""
        try:
            # Clear existing matches
            for widget in self.matches_container.winfo_children():
                widget.destroy()
            
            # Get upcoming matches
            matches = self.data_service.get_upcoming_matches(limit=6)
            
            if not matches:
                no_matches_label = ctk.CTkLabel(
                    self.matches_container,
                    text="No upcoming matches found",
                    font=(theme.FONTS['primary'], theme.FONTS['size_base']),
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
                    self.matches_container,
                    match_data=match_data,
                    on_click=self._show_prediction_dialog
                )
                card.pack(fill="x", pady=(0, theme.SPACING['md']))
        
        except Exception as e:
            print(f"Error loading matches: {e}")
    
    def _show_prediction_dialog(self, match_data: dict):
        """Show prediction dialog for a match."""
        try:
            dialog = PredictionDialog(self, match_data, self.prediction_service)
            dialog.focus()
        except Exception as e:
            print(f"Error showing prediction dialog: {e}")
