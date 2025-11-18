"""Modern navigation sidebar with icons and smooth transitions."""
import customtkinter as ctk
from typing import Callable
from gui.theme import theme


class NavigationButton(ctk.CTkButton):
    """Custom navigation button with modern styling and hover effects."""
    
    def __init__(self, parent, text: str, icon: str, command: Callable, **kwargs):
        """
        Initialize navigation button.
        
        Args:
            parent: Parent widget
            text: Button text
            icon: Icon/emoji for the button
            command: Callback function
        """
        super().__init__(
            parent,
            text=f"{icon}  {text}",
            command=command,
            height=50,
            corner_radius=theme.RADIUS['md'],
            fg_color="transparent",
            text_color=theme.COLORS['text_secondary'],
            hover_color=theme.COLORS['bg_hover'],
            anchor="w",
            font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_normal']),
            **kwargs
        )
        self.is_active = False
        self.default_fg_color = "transparent"
        self.active_fg_color = theme.COLORS['primary']
        
    def set_active(self, active: bool):
        """Set button active state with visual feedback."""
        self.is_active = active
        if active:
            self.configure(
                fg_color=theme.COLORS['primary'],
                text_color=theme.COLORS['text_primary'],
                hover_color=theme.COLORS['primary_hover']
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=theme.COLORS['text_secondary'],
                hover_color=theme.COLORS['bg_hover']
            )


class NavigationSidebar(ctk.CTkFrame):
    """Modern navigation sidebar with professional design."""
    
    def __init__(self, parent, navigate_callback: Callable):
        """
        Initialize navigation sidebar.
        
        Args:
            parent: Parent widget
            navigate_callback: Callback function for navigation
        """
        super().__init__(
            parent,
            width=280,
            corner_radius=0,
            fg_color=theme.COLORS['bg_secondary']
        )
        
        self.navigate_callback = navigate_callback
        self.buttons = {}
        self.current_page = None
        
        # Prevent sidebar from shrinking
        self.grid_propagate(False)
        
        # Create header
        self._create_header()
        
        # Create navigation buttons
        self._create_navigation_buttons()
        
        # Create footer
        self._create_footer()
    
    def _create_header(self):
        """Create modern header with app branding."""
        # Header frame
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=100
        )
        header_frame.pack(fill="x", padx=theme.SPACING['lg'], pady=(theme.SPACING['xl'], theme.SPACING['lg']))
        header_frame.pack_propagate(False)
        
        # App icon/logo
        logo_label = ctk.CTkLabel(
            header_frame,
            text="⚽",
            font=(theme.FONTS['primary'], 48),
            text_color=theme.COLORS['primary']
        )
        logo_label.pack(pady=(theme.SPACING['sm'], 0))
        
        # App title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Football AI",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Advanced Predictions",
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_tertiary']
        )
        subtitle_label.pack()
        
        # Separator line
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color=theme.COLORS['border']
        )
        separator.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['md'])
    
    def _create_navigation_buttons(self):
        """Create navigation buttons with icons."""
        # Navigation container
        nav_container = ctk.CTkFrame(self, fg_color="transparent")
        nav_container.pack(fill="both", expand=True, padx=theme.SPACING['md'], pady=theme.SPACING['sm'])
        
        # Navigation items with modern icons
        nav_items = [
            ("dashboard", "📊", "Dashboard"),
            ("matches", "⚽", "Matches"),
            ("predictions", "🎯", "Predictions"),
            ("statistics", "📈", "Statistics"),
            ("accuracy", "✓", "Accuracy"),
            ("tracker", "📋", "Bet Tracker"),
            ("settings", "⚙", "Settings"),
        ]
        
        for page_id, icon, label in nav_items:
            btn = NavigationButton(
                nav_container,
                text=label,
                icon=icon,
                command=lambda p=page_id: self._on_navigate(p)
            )
            btn.pack(fill="x", pady=theme.SPACING['xs'])
            self.buttons[page_id] = btn
        
        # Set dashboard as active by default
        self.set_active_page("dashboard")
    
    def _create_footer(self):
        """Create footer with version info and status."""
        # Separator line
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color=theme.COLORS['border']
        )
        separator.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['md'])
        
        # Footer frame
        footer_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=80
        )
        footer_frame.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        footer_frame.pack_propagate(False)
        
        # Status indicator
        status_frame = ctk.CTkFrame(
            footer_frame,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md']
        )
        status_frame.pack(fill="x", pady=theme.SPACING['sm'])
        
        status_indicator = ctk.CTkLabel(
            status_frame,
            text="● Online",
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['success']
        )
        status_indicator.pack(pady=theme.SPACING['sm'])
        
        # Version info
        version_label = ctk.CTkLabel(
            footer_frame,
            text="v2.0.0 Advanced",
            font=(theme.FONTS['primary'], theme.FONTS['size_xs']),
            text_color=theme.COLORS['text_tertiary']
        )
        version_label.pack()
    
    def _on_navigate(self, page_id: str):
        """
        Handle navigation button click.
        
        Args:
            page_id: ID of the page to navigate to
        """
        self.set_active_page(page_id)
        self.navigate_callback(page_id)
    
    def set_active_page(self, page_id: str):
        """
        Set the active page and update button states.
        
        Args:
            page_id: ID of the active page
        """
        # Deactivate all buttons
        for btn_id, btn in self.buttons.items():
            btn.set_active(btn_id == page_id)
        
        self.current_page = page_id
