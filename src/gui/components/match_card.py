"""Modern match card component with professional design and hover effects."""
import customtkinter as ctk
from typing import Callable, Optional
from datetime import datetime
from gui.theme import theme


class ModernMatchCard(ctk.CTkFrame):
    """Professional match card with hover effects and detailed information."""
    
    def __init__(
        self,
        parent,
        match_data: dict,
        on_click: Optional[Callable] = None,
        show_prediction: bool = False,
        **kwargs
    ):
        """
        Initialize modern match card.
        
        Args:
            parent: Parent widget
            match_data: Dictionary containing match information
            on_click: Callback function when card is clicked
            show_prediction: Whether to show prediction information
        """
        super().__init__(
            parent,
            **theme.get_card_style(),
            **kwargs
        )
        
        self.match_data = match_data
        self.on_click = on_click
        self.show_prediction = show_prediction
        
        # Configure hover effect
        self.default_fg_color = theme.COLORS['bg_card']
        self.hover_fg_color = theme.COLORS['bg_hover']
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        if on_click:
            self.bind("<Button-1>", lambda e: on_click(match_data))
            self.configure(cursor="hand2")
        
        # Build card content
        self._build_card()
    
    def _build_card(self):
        """Build the card content with modern layout."""
        # Main container with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['md'])
        
        # Header section (League and Date)
        self._create_header(container)
        
        # Match section (Teams and Score)
        self._create_match_section(container)
        
        # Prediction section (if enabled)
        if self.show_prediction and 'prediction' in self.match_data:
            self._create_prediction_section(container)
        
        # Status badge
        self._create_status_badge(container)
    
    def _create_header(self, parent):
        """Create card header with league and date."""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, theme.SPACING['sm']))
        
        # League name
        league_label = ctk.CTkLabel(
            header_frame,
            text=self.match_data.get('league', 'Unknown League'),
            font=(theme.FONTS['primary'], theme.FONTS['size_sm'], theme.FONTS['weight_medium']),
            text_color=theme.COLORS['primary'],
            anchor="w"
        )
        league_label.pack(side="left")
        
        # Match date/time
        match_date = self.match_data.get('date')
        if isinstance(match_date, datetime):
            date_str = match_date.strftime("%b %d, %H:%M")
        else:
            date_str = str(match_date)
        
        date_label = ctk.CTkLabel(
            header_frame,
            text=date_str,
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_tertiary'],
            anchor="e"
        )
        date_label.pack(side="right")
    
    def _create_match_section(self, parent):
        """Create main match section with teams and score."""
        match_frame = ctk.CTkFrame(parent, fg_color="transparent")
        match_frame.pack(fill="x", pady=theme.SPACING['md'])
        
        # Configure grid
        match_frame.grid_columnconfigure(0, weight=1)
        match_frame.grid_columnconfigure(1, weight=0)
        match_frame.grid_columnconfigure(2, weight=1)
        
        # Home team
        home_team = self.match_data.get('home_team', 'Home Team')
        home_label = ctk.CTkLabel(
            match_frame,
            text=home_team,
            font=(theme.FONTS['primary'], theme.FONTS['size_lg'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="e"
        )
        home_label.grid(row=0, column=0, sticky="e", padx=theme.SPACING['md'])
        
        # Score or VS
        status = self.match_data.get('status', 'scheduled')
        if status == 'finished':
            home_goals = self.match_data.get('home_goals', 0)
            away_goals = self.match_data.get('away_goals', 0)
            score_text = f"{home_goals} : {away_goals}"
            score_color = theme.COLORS['text_primary']
        else:
            score_text = "VS"
            score_color = theme.COLORS['text_tertiary']
        
        score_frame = ctk.CTkFrame(
            match_frame,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md'],
            width=80,
            height=50
        )
        score_frame.grid(row=0, column=1, padx=theme.SPACING['md'])
        score_frame.grid_propagate(False)
        
        score_label = ctk.CTkLabel(
            score_frame,
            text=score_text,
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=score_color
        )
        score_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Away team
        away_team = self.match_data.get('away_team', 'Away Team')
        away_label = ctk.CTkLabel(
            match_frame,
            text=away_team,
            font=(theme.FONTS['primary'], theme.FONTS['size_lg'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        away_label.grid(row=0, column=2, sticky="w", padx=theme.SPACING['md'])
    
    def _create_prediction_section(self, parent):
        """Create prediction section with confidence indicators."""
        prediction = self.match_data.get('prediction', {})
        
        pred_frame = ctk.CTkFrame(
            parent,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md']
        )
        pred_frame.pack(fill="x", pady=(theme.SPACING['md'], 0))
        
        # Prediction header
        pred_header = ctk.CTkLabel(
            pred_frame,
            text="🎯 AI Prediction",
            font=(theme.FONTS['primary'], theme.FONTS['size_sm'], theme.FONTS['weight_medium']),
            text_color=theme.COLORS['text_secondary']
        )
        pred_header.pack(pady=(theme.SPACING['sm'], theme.SPACING['xs']))
        
        # Prediction values container
        pred_values = ctk.CTkFrame(pred_frame, fg_color="transparent")
        pred_values.pack(fill="x", padx=theme.SPACING['md'], pady=(0, theme.SPACING['sm']))
        
        # Configure grid for predictions
        pred_values.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Get prediction probabilities
        home_prob = prediction.get('home_win', 0) * 100
        draw_prob = prediction.get('draw', 0) * 100
        away_prob = prediction.get('away_win', 0) * 100
        
        # Home win
        self._create_prediction_badge(
            pred_values,
            "Home Win",
            f"{home_prob:.1f}%",
            theme.COLORS['success'],
            0
        )
        
        # Draw
        self._create_prediction_badge(
            pred_values,
            "Draw",
            f"{draw_prob:.1f}%",
            theme.COLORS['warning'],
            1
        )
        
        # Away win
        self._create_prediction_badge(
            pred_values,
            "Away Win",
            f"{away_prob:.1f}%",
            theme.COLORS['error'],
            2
        )
    
    def _create_prediction_badge(self, parent, label: str, value: str, color: str, column: int):
        """Create a prediction probability badge."""
        badge = ctk.CTkFrame(parent, fg_color="transparent")
        badge.grid(row=0, column=column, padx=theme.SPACING['xs'])
        
        value_label = ctk.CTkLabel(
            badge,
            text=value,
            font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_bold']),
            text_color=color
        )
        value_label.pack()
        
        label_label = ctk.CTkLabel(
            badge,
            text=label,
            font=(theme.FONTS['primary'], theme.FONTS['size_xs']),
            text_color=theme.COLORS['text_tertiary']
        )
        label_label.pack()
    
    def _create_status_badge(self, parent):
        """Create status badge (Live, Finished, Upcoming)."""
        status = self.match_data.get('status', 'scheduled')
        
        # Determine badge text and color
        if status == 'finished':
            badge_text = "Finished"
            badge_color = theme.COLORS['text_tertiary']
        elif status == 'in_play':
            badge_text = "● LIVE"
            badge_color = theme.COLORS['error']
        else:
            badge_text = "Upcoming"
            badge_color = theme.COLORS['info']
        
        badge = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        badge.pack(fill="x", pady=(theme.SPACING['sm'], 0))
        
        badge_label = ctk.CTkLabel(
            badge,
            text=badge_text,
            font=(theme.FONTS['primary'], theme.FONTS['size_xs'], theme.FONTS['weight_medium']),
            text_color=badge_color
        )
        badge_label.pack()
    
    def _on_enter(self, event):
        """Handle mouse enter event."""
        self.configure(fg_color=self.hover_fg_color)
        # Propagate to all child widgets
        for child in self.winfo_children():
            try:
                child.bind("<Button-1>", lambda e: self.on_click(self.match_data) if self.on_click else None)
            except:
                pass
    
    def _on_leave(self, event):
        """Handle mouse leave event."""
        self.configure(fg_color=self.default_fg_color)


class CompactMatchCard(ctk.CTkFrame):
    """Compact version of match card for lists."""
    
    def __init__(self, parent, match_data: dict, on_click: Optional[Callable] = None, **kwargs):
        """Initialize compact match card."""
        super().__init__(
            parent,
            fg_color=theme.COLORS['bg_card'],
            corner_radius=theme.RADIUS['md'],
            border_width=1,
            border_color=theme.COLORS['border'],
            height=60,
            **kwargs
        )
        
        self.match_data = match_data
        self.on_click = on_click
        
        if on_click:
            self.bind("<Button-1>", lambda e: on_click(match_data))
            self.configure(cursor="hand2")
        
        self.pack_propagate(False)
        self._build_compact_card()
    
    def _build_compact_card(self):
        """Build compact card layout."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['md'], pady=theme.SPACING['sm'])
        
        # Time
        match_date = self.match_data.get('date')
        if isinstance(match_date, datetime):
            time_str = match_date.strftime("%H:%M")
        else:
            time_str = "--:--"
        
        time_label = ctk.CTkLabel(
            container,
            text=time_str,
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_tertiary'],
            width=50
        )
        time_label.pack(side="left", padx=(0, theme.SPACING['md']))
        
        # Teams
        teams_text = f"{self.match_data.get('home_team', 'Home')} vs {self.match_data.get('away_team', 'Away')}"
        teams_label = ctk.CTkLabel(
            container,
            text=teams_text,
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        teams_label.pack(side="left", fill="x", expand=True)
        
        # Score or status
        status = self.match_data.get('status', 'scheduled')
        if status == 'finished':
            score_text = f"{self.match_data.get('home_goals', 0)}-{self.match_data.get('away_goals', 0)}"
            score_label = ctk.CTkLabel(
                container,
                text=score_text,
                font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_bold']),
                text_color=theme.COLORS['text_primary']
            )
            score_label.pack(side="right")
