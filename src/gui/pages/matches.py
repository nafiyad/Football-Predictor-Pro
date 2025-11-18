"""Modern matches page with filtering and search."""
import customtkinter as ctk
import tkinter as tk
from services.data_service import DataService
from gui.components.match_card import ModernMatchCard
from gui.components.prediction_panel import PredictionDialog
from services.prediction_service import PredictionService
from gui.theme import theme


class MatchesPage(ctk.CTkFrame):
    """Modern matches page with advanced filtering."""
    
    def __init__(self, parent):
        """Initialize matches page."""
        super().__init__(parent, corner_radius=0, fg_color=theme.COLORS['bg_primary'])
        
        self.data_service = DataService()
        self.prediction_service = PredictionService()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create page widgets."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=theme.SPACING['xl'], pady=theme.SPACING['xl'])
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            main_container,
            text="⚽ All Matches",
            font=(theme.FONTS['primary'], theme.FONTS['size_4xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        header_label.grid(row=0, column=0, sticky="w", pady=(0, theme.SPACING['md']))
        
        # Filter section
        filter_frame = ctk.CTkFrame(main_container, **theme.get_card_style())
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, theme.SPACING['lg']))
        
        filter_container = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_container.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['md'])
        
        # Status filter
        status_label = ctk.CTkLabel(
            filter_container,
            text="Status:",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_secondary']
        )
        status_label.pack(side="left", padx=(0, theme.SPACING['sm']))
        
        self.status_var = tk.StringVar(value="all")
        status_menu = ctk.CTkOptionMenu(
            filter_container,
            variable=self.status_var,
            values=["all", "scheduled", "finished", "in_play"],
            command=self._on_filter_change,
            fg_color=theme.COLORS['bg_tertiary'],
            button_color=theme.COLORS['primary'],
            button_hover_color=theme.COLORS['primary_hover'],
            width=150
        )
        status_menu.pack(side="left", padx=(0, theme.SPACING['lg']))
        
        # League filter
        league_label = ctk.CTkLabel(
            filter_container,
            text="League:",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_secondary']
        )
        league_label.pack(side="left", padx=(0, theme.SPACING['sm']))
        
        self.league_var = tk.StringVar(value="all")
        self.league_menu = ctk.CTkOptionMenu(
            filter_container,
            variable=self.league_var,
            values=["all"],
            command=self._on_filter_change,
            fg_color=theme.COLORS['bg_tertiary'],
            button_color=theme.COLORS['primary'],
            button_hover_color=theme.COLORS['primary_hover'],
            width=200
        )
        self.league_menu.pack(side="left")
        
        # Matches scrollable container
        self.matches_scroll = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent"
        )
        self.matches_scroll.grid(row=2, column=0, sticky="nsew")
    
    def _on_filter_change(self, value):
        """Handle filter change."""
        self.refresh()
    
    def refresh(self):
        """Refresh matches list."""
        try:
            self._load_matches()
            self._load_leagues()
        except Exception as e:
            print(f"Error refreshing matches: {e}")
    
    def _load_leagues(self):
        """Load available leagues for filter."""
        try:
            from database.connection import get_session
            from models.database import League
            
            session = get_session()
            leagues = session.query(League).all()
            
            league_names = ["all"] + [league.name for league in leagues]
            self.league_menu.configure(values=league_names)
            
            session.close()
        except Exception as e:
            print(f"Error loading leagues: {e}")
    
    def _load_matches(self):
        """Load and display matches."""
        try:
            # Clear existing matches
            for widget in self.matches_scroll.winfo_children():
                widget.destroy()
            
            # Get filter values
            status = self.status_var.get()
            league = self.league_var.get()
            
            # Get matches based on filters
            if status == "all":
                matches = self.data_service.get_all_matches(limit=100)
            elif status == "scheduled":
                matches = self.data_service.get_upcoming_matches(limit=100)
            else:
                matches = self.data_service.get_matches_by_status(status, limit=100)
            
            # Filter by league if needed
            if league != "all":
                matches = [m for m in matches if m.league and m.league.name == league]
            
            if not matches:
                no_matches_label = ctk.CTkLabel(
                    self.matches_scroll,
                    text="No matches found",
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
                    self.matches_scroll,
                    match_data=match_data,
                    on_click=self._show_prediction_dialog
                )
                card.pack(fill="x", pady=(0, theme.SPACING['md']))
        
        except Exception as e:
            print(f"Error loading matches: {e}")
    
    def _show_prediction_dialog(self, match_data: dict):
        """Show prediction dialog."""
        try:
            dialog = PredictionDialog(self, match_data, self.prediction_service)
            dialog.focus()
        except Exception as e:
            print(f"Error showing prediction dialog: {e}")
