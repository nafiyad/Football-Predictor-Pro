"""Modern prediction display with advanced visualizations and confidence meters."""
import customtkinter as ctk
from models.database import Prediction
from utils.helpers import percentage_to_string, get_confidence_level, calculate_odds_from_probability
from gui.theme import theme
import math


class ConfidenceMeter(ctk.CTkFrame):
    """Circular confidence meter with animated progress."""
    
    def __init__(self, parent, confidence: float, **kwargs):
        """Initialize confidence meter."""
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.confidence = confidence
        
        # Create canvas for circular progress
        self.canvas = ctk.CTkCanvas(
            self,
            width=120,
            height=120,
            bg=theme.COLORS['bg_card'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        self._draw_meter()
    
    def _draw_meter(self):
        """Draw circular confidence meter."""
        # Background circle
        self.canvas.create_oval(
            10, 10, 110, 110,
            outline=theme.COLORS['border'],
            width=8
        )
        
        # Progress arc
        extent = (self.confidence * 360)
        color = self._get_confidence_color(self.confidence)
        
        self.canvas.create_arc(
            10, 10, 110, 110,
            start=90,
            extent=-extent,
            outline=color,
            width=8,
            style="arc"
        )
        
        # Center text
        self.canvas.create_text(
            60, 60,
            text=f"{int(self.confidence * 100)}%",
            font=(theme.FONTS['primary'], 24, "bold"),
            fill=theme.COLORS['text_primary']
        )
    
    def _get_confidence_color(self, confidence: float) -> str:
        """Get color based on confidence level."""
        if confidence >= 0.7:
            return theme.COLORS['success']
        elif confidence >= 0.5:
            return theme.COLORS['warning']
        else:
            return theme.COLORS['error']


class ProbabilityBar(ctk.CTkFrame):
    """Modern probability bar with gradient and percentage."""
    
    def __init__(self, parent, label: str, probability: float, color: str, **kwargs):
        """Initialize probability bar."""
        super().__init__(
            parent,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md'],
            height=60,
            **kwargs
        )
        
        self.pack_propagate(False)
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['md'], pady=theme.SPACING['sm'])
        
        # Label and percentage
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x")
        
        label_widget = ctk.CTkLabel(
            header_frame,
            text=label,
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        label_widget.pack(side="left")
        
        percentage_widget = ctk.CTkLabel(
            header_frame,
            text=f"{probability * 100:.1f}%",
            font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_bold']),
            text_color=color,
            anchor="e"
        )
        percentage_widget.pack(side="right")
        
        # Progress bar
        progress_bg = ctk.CTkFrame(
            container,
            fg_color=theme.COLORS['bg_primary'],
            corner_radius=theme.RADIUS['sm'],
            height=8
        )
        progress_bg.pack(fill="x", pady=(theme.SPACING['xs'], 0))
        
        progress_fill = ctk.CTkFrame(
            progress_bg,
            fg_color=color,
            corner_radius=theme.RADIUS['sm'],
            width=int(probability * progress_bg.winfo_reqwidth())
        )
        progress_fill.place(relx=0, rely=0, relheight=1, relwidth=probability)


class PredictionDialog(ctk.CTkToplevel):
    """Modern prediction dialog with advanced visualizations."""
    
    def __init__(self, parent, match_data: dict, prediction_service):
        """Initialize prediction dialog."""
        super().__init__(parent)
        
        self.match_data = match_data
        self.prediction_service = prediction_service
        
        # Window configuration
        self.title("Match Prediction")
        self.geometry("800x900")
        self.configure(fg_color=theme.COLORS['bg_primary'])
        
        # Center window
        self._center_window()
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Create content
        self._create_content()
        
        # Generate prediction
        self._generate_prediction()
    
    def _center_window(self):
        """Center the dialog on screen."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 800) // 2
        y = (self.winfo_screenheight() - 900) // 2
        self.geometry(f"800x900+{x}+{y}")
    
    def _create_content(self):
        """Create dialog content."""
        # Scrollable container
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=theme.COLORS['bg_primary']
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Content container
        self.content_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=theme.SPACING['xl'], pady=theme.SPACING['xl'])
    
    def _generate_prediction(self):
        """Generate and display prediction."""
        try:
            # Show loading
            loading_label = ctk.CTkLabel(
                self.content_frame,
                text="🔄 Generating AI Prediction...",
                font=(theme.FONTS['primary'], theme.FONTS['size_lg']),
                text_color=theme.COLORS['text_secondary']
            )
            loading_label.pack(pady=theme.SPACING['xl'])
            
            self.update()
            
            # Get match from database
            from database.connection import get_session
            from models.database import Match
            
            session = get_session()
            match = session.query(Match).filter_by(id=self.match_data['id']).first()
            
            if not match:
                loading_label.configure(text="❌ Match not found")
                session.close()
                return
            
            # Generate prediction
            prediction = self.prediction_service.get_match_prediction(match.id)
            session.close()
            
            # Clear loading
            loading_label.destroy()
            
            # Display prediction
            self._display_prediction(prediction)
            
        except Exception as e:
            print(f"Error generating prediction: {e}")
            loading_label.configure(text=f"❌ Error: {str(e)}")
    
    def _display_prediction(self, prediction: Prediction):
        """Display the prediction with modern UI."""
        # Match header
        self._create_match_header()
        
        # Confidence section
        self._create_confidence_section(prediction)
        
        # Main prediction section (1X2)
        self._create_1x2_section(prediction)
        
        # Other markets
        self._create_other_markets_section(prediction)
        
        # Predicted score
        self._create_score_section(prediction)
        
        # Action buttons
        self._create_action_buttons()
    
    def _create_match_header(self):
        """Create match header section."""
        header_frame = ctk.CTkFrame(
            self.content_frame,
            **theme.get_card_style()
        )
        header_frame.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        container = ctk.CTkFrame(header_frame, fg_color="transparent")
        container.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # League
        league_label = ctk.CTkLabel(
            container,
            text=self.match_data['league'],
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['primary']
        )
        league_label.pack(anchor="w")
        
        # Teams
        teams_frame = ctk.CTkFrame(container, fg_color="transparent")
        teams_frame.pack(fill="x", pady=theme.SPACING['md'])
        
        home_label = ctk.CTkLabel(
            teams_frame,
            text=self.match_data['home_team'],
            font=(theme.FONTS['primary'], theme.FONTS['size_2xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        home_label.pack(side="left", expand=True)
        
        vs_label = ctk.CTkLabel(
            teams_frame,
            text="VS",
            font=(theme.FONTS['primary'], theme.FONTS['size_lg']),
            text_color=theme.COLORS['text_tertiary']
        )
        vs_label.pack(side="left", padx=theme.SPACING['lg'])
        
        away_label = ctk.CTkLabel(
            teams_frame,
            text=self.match_data['away_team'],
            font=(theme.FONTS['primary'], theme.FONTS['size_2xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        away_label.pack(side="left", expand=True)
        
        # Date
        date_label = ctk.CTkLabel(
            container,
            text=self.match_data['date'].strftime("%A, %B %d at %H:%M"),
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_tertiary']
        )
        date_label.pack(anchor="w")
    
    def _create_confidence_section(self, prediction: Prediction):
        """Create confidence meter section."""
        conf_frame = ctk.CTkFrame(
            self.content_frame,
            **theme.get_card_style()
        )
        conf_frame.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        container = ctk.CTkFrame(conf_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="🎯 Prediction Confidence",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack(pady=(0, theme.SPACING['md']))
        
        # Confidence meter
        meter = ConfidenceMeter(container, prediction.confidence)
        meter.pack()
        
        # Confidence level text
        conf_level, conf_color = get_confidence_level(prediction.confidence)
        level_label = ctk.CTkLabel(
            container,
            text=conf_level,
            font=(theme.FONTS['primary'], theme.FONTS['size_lg'], theme.FONTS['weight_bold']),
            text_color=conf_color
        )
        level_label.pack(pady=(theme.SPACING['md'], 0))
    
    def _create_1x2_section(self, prediction: Prediction):
        """Create 1X2 prediction section."""
        section_frame = ctk.CTkFrame(
            self.content_frame,
            **theme.get_card_style()
        )
        section_frame.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        container = ctk.CTkFrame(section_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="⚽ Match Result (1X2)",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['lg']))
        
        # Probability bars
        ProbabilityBar(
            container,
            label="Home Win",
            probability=prediction.home_win_prob,
            color=theme.COLORS['success']
        ).pack(fill="x", pady=(0, theme.SPACING['sm']))
        
        ProbabilityBar(
            container,
            label="Draw",
            probability=prediction.draw_prob,
            color=theme.COLORS['warning']
        ).pack(fill="x", pady=(0, theme.SPACING['sm']))
        
        ProbabilityBar(
            container,
            label="Away Win",
            probability=prediction.away_win_prob,
            color=theme.COLORS['error']
        ).pack(fill="x")
    
    def _create_other_markets_section(self, prediction: Prediction):
        """Create other markets section."""
        section_frame = ctk.CTkFrame(
            self.content_frame,
            **theme.get_card_style()
        )
        section_frame.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        container = ctk.CTkFrame(section_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="📊 Other Markets",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['lg']))
        
        # BTTS
        if prediction.btts_prob:
            ProbabilityBar(
                container,
                label="Both Teams To Score",
                probability=prediction.btts_prob,
                color=theme.COLORS['info']
            ).pack(fill="x", pady=(0, theme.SPACING['sm']))
        
        # Over 2.5
        if prediction.over_2_5_prob:
            ProbabilityBar(
                container,
                label="Over 2.5 Goals",
                probability=prediction.over_2_5_prob,
                color=theme.COLORS['secondary']
            ).pack(fill="x")
    
    def _create_score_section(self, prediction: Prediction):
        """Create predicted score section."""
        if not prediction.predicted_home_goals or not prediction.predicted_away_goals:
            return
        
        section_frame = ctk.CTkFrame(
            self.content_frame,
            **theme.get_card_style()
        )
        section_frame.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        container = ctk.CTkFrame(section_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="🎲 Predicted Score",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack(pady=(0, theme.SPACING['md']))
        
        # Score
        score_label = ctk.CTkLabel(
            container,
            text=f"{prediction.predicted_home_goals:.1f} - {prediction.predicted_away_goals:.1f}",
            font=(theme.FONTS['primary'], theme.FONTS['size_4xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['primary']
        )
        score_label.pack()
    
    def _create_action_buttons(self):
        """Create action buttons."""
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(theme.SPACING['lg'], 0))
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            **theme.get_button_style('secondary'),
            command=self.destroy,
            height=45,
            font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_medium'])
        )
        close_btn.pack(fill="x")


class PredictionPanel(ctk.CTkFrame):
    """Legacy prediction panel for compatibility."""
    
    def __init__(self, parent, prediction: Prediction):
        """Initialize prediction panel."""
        super().__init__(parent, **theme.get_card_style())
        
        self.prediction = prediction
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()
    
    def create_widgets(self):
        """Create panel widgets."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew", padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="Match Prediction",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        # Confidence
        conf_level, conf_color = get_confidence_level(self.prediction.confidence)
        conf_label = ctk.CTkLabel(
            container,
            text=f"Confidence: {conf_level} ({self.prediction.confidence * 100:.1f}%)",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=conf_color
        )
        conf_label.pack(anchor="w", pady=(0, theme.SPACING['lg']))
        
        # Predictions
        ProbabilityBar(
            container,
            label="Home Win",
            probability=self.prediction.home_win_prob,
            color=theme.COLORS['success']
        ).pack(fill="x", pady=(0, theme.SPACING['sm']))
        
        ProbabilityBar(
            container,
            label="Draw",
            probability=self.prediction.draw_prob,
            color=theme.COLORS['warning']
        ).pack(fill="x", pady=(0, theme.SPACING['sm']))
        
        ProbabilityBar(
            container,
            label="Away Win",
            probability=self.prediction.away_win_prob,
            color=theme.COLORS['error']
        ).pack(fill="x")
