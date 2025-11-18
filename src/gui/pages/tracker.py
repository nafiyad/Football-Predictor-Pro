"""Modern betting tracker page."""
import customtkinter as ctk
from services.data_service import DataService
from services.stats_service import StatsService
from gui.theme import theme


class TrackerPage(ctk.CTkScrollableFrame):
    """Modern betting tracker with performance metrics."""
    
    def __init__(self, parent):
        """Initialize tracker page."""
        super().__init__(parent, corner_radius=0, fg_color=theme.COLORS['bg_primary'])
        
        self.data_service = DataService()
        self.stats_service = StatsService()
        
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
            text="📋 Bet Tracker",
            font=(theme.FONTS['primary'], theme.FONTS['size_4xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        header_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        subtitle_label = ctk.CTkLabel(
            main_container,
            text="Track your bets and analyze performance",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_tertiary'],
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(0, theme.SPACING['xl']))
        
        # Stats overview
        stats_card = ctk.CTkFrame(main_container, **theme.get_card_style())
        stats_card.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        stats_container = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_container.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        title_label = ctk.CTkLabel(
            stats_container,
            text="📊 Overview",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_container, fg_color="transparent")
        stats_grid.pack(fill="x")
        
        for i in range(4):
            stats_grid.grid_columnconfigure(i, weight=1)
        
        self._create_stat_box(stats_grid, "Total Bets", "0", 0)
        self._create_stat_box(stats_grid, "Won", "0", 1, theme.COLORS['success'])
        self._create_stat_box(stats_grid, "Lost", "0", 2, theme.COLORS['error'])
        self._create_stat_box(stats_grid, "Win Rate", "0%", 3)
        
        # Coming soon message
        coming_soon_card = ctk.CTkFrame(main_container, **theme.get_card_style())
        coming_soon_card.pack(fill="x")
        
        coming_soon_container = ctk.CTkFrame(coming_soon_card, fg_color="transparent")
        coming_soon_container.pack(fill="both", expand=True, padx=theme.SPACING['xl'], pady=theme.SPACING['xl'])
        
        icon_label = ctk.CTkLabel(
            coming_soon_container,
            text="🚀",
            font=(theme.FONTS['primary'], 64)
        )
        icon_label.pack(pady=(theme.SPACING['lg'], theme.SPACING['md']))
        
        title_label = ctk.CTkLabel(
            coming_soon_container,
            text="Bet Tracking Coming Soon",
            font=(theme.FONTS['primary'], theme.FONTS['size_2xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack()
        
        desc_label = ctk.CTkLabel(
            coming_soon_container,
            text="Track your bets, analyze performance, and optimize your betting strategy",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_tertiary'],
            wraplength=500
        )
        desc_label.pack(pady=theme.SPACING['md'])
    
    def _create_stat_box(self, parent, label: str, value: str, column: int, color: str = None):
        """Create a stat box."""
        box = ctk.CTkFrame(
            parent,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md']
        )
        box.grid(row=0, column=column, sticky="ew", padx=(0, theme.SPACING['md'] if column < 3 else 0))
        
        value_label = ctk.CTkLabel(
            box,
            text=value,
            font=(theme.FONTS['primary'], theme.FONTS['size_2xl'], theme.FONTS['weight_bold']),
            text_color=color or theme.COLORS['text_primary']
        )
        value_label.pack(pady=(theme.SPACING['md'], theme.SPACING['xs']))
        
        label_label = ctk.CTkLabel(
            box,
            text=label,
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_tertiary']
        )
        label_label.pack(pady=(0, theme.SPACING['md']))
    
    def refresh(self):
        """Refresh tracker data."""
        pass  # To be implemented
