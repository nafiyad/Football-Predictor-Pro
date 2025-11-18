"""Modern loading animations and progress indicators."""
import customtkinter as ctk
from gui.theme import theme
import math


class LoadingSpinner(ctk.CTkFrame):
    """Animated loading spinner."""
    
    def __init__(self, parent, size: int = 40, **kwargs):
        """Initialize loading spinner."""
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.size = size
        self.angle = 0
        self.is_animating = False
        
        # Create canvas
        self.canvas = ctk.CTkCanvas(
            self,
            width=size,
            height=size,
            bg=theme.COLORS['bg_primary'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Draw initial spinner
        self._draw_spinner()
    
    def _draw_spinner(self):
        """Draw the spinner."""
        self.canvas.delete("all")
        
        # Draw arc
        self.canvas.create_arc(
            5, 5, self.size - 5, self.size - 5,
            start=self.angle,
            extent=270,
            outline=theme.COLORS['primary'],
            width=3,
            style="arc"
        )
    
    def start(self):
        """Start animation."""
        self.is_animating = True
        self._animate()
    
    def stop(self):
        """Stop animation."""
        self.is_animating = False
    
    def _animate(self):
        """Animate the spinner."""
        if not self.is_animating:
            return
        
        self.angle = (self.angle + 10) % 360
        self._draw_spinner()
        
        self.after(50, self._animate)


class LoadingOverlay(ctk.CTkFrame):
    """Full-screen loading overlay with spinner and message."""
    
    def __init__(self, parent, message: str = "Loading...", **kwargs):
        """Initialize loading overlay."""
        super().__init__(
            parent,
            fg_color=(theme.COLORS['bg_primary'], theme.COLORS['bg_primary'] + "CC"),
            **kwargs
        )
        
        # Center container
        container = ctk.CTkFrame(
            self,
            fg_color=theme.COLORS['bg_card'],
            corner_radius=theme.RADIUS['lg'],
            border_width=1,
            border_color=theme.COLORS['border']
        )
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Spinner
        self.spinner = LoadingSpinner(container, size=60)
        self.spinner.pack(padx=theme.SPACING['xl'], pady=(theme.SPACING['xl'], theme.SPACING['md']))
        
        # Message
        self.message_label = ctk.CTkLabel(
            container,
            text=message,
            font=(theme.FONTS['primary'], theme.FONTS['size_lg']),
            text_color=theme.COLORS['text_primary']
        )
        self.message_label.pack(padx=theme.SPACING['xl'], pady=(0, theme.SPACING['xl']))
        
        # Start animation
        self.spinner.start()
    
    def update_message(self, message: str):
        """Update loading message."""
        self.message_label.configure(text=message)
    
    def destroy(self):
        """Destroy overlay and stop animation."""
        self.spinner.stop()
        super().destroy()


class ProgressBar(ctk.CTkFrame):
    """Modern progress bar with percentage."""
    
    def __init__(self, parent, **kwargs):
        """Initialize progress bar."""
        super().__init__(
            parent,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md'],
            height=30,
            **kwargs
        )
        
        self.progress = 0
        
        # Progress fill
        self.fill = ctk.CTkFrame(
            self,
            fg_color=theme.COLORS['primary'],
            corner_radius=theme.RADIUS['md']
        )
        
        # Percentage label
        self.label = ctk.CTkLabel(
            self,
            text="0%",
            font=(theme.FONTS['primary'], theme.FONTS['size_sm'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")
    
    def set_progress(self, progress: float):
        """Set progress (0.0 to 1.0)."""
        self.progress = max(0.0, min(1.0, progress))
        
        # Update fill
        self.fill.place(relx=0, rely=0, relheight=1, relwidth=self.progress)
        
        # Update label
        self.label.configure(text=f"{int(self.progress * 100)}%")
        
        # Update
        self.update()


class Tooltip(ctk.CTkToplevel):
    """Modern tooltip for hover information."""
    
    def __init__(self, widget, text: str):
        """Initialize tooltip."""
        super().__init__(widget)
        
        self.withdraw()
        self.overrideredirect(True)
        
        # Configure appearance
        self.configure(fg_color=theme.COLORS['bg_tertiary'])
        
        # Tooltip label
        label = ctk.CTkLabel(
            self,
            text=text,
            font=(theme.FONTS['primary'], theme.FONTS['size_sm']),
            text_color=theme.COLORS['text_primary'],
            corner_radius=theme.RADIUS['sm']
        )
        label.pack(padx=theme.SPACING['sm'], pady=theme.SPACING['xs'])
        
        # Bind events
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)
        widget.bind("<Motion>", self._move)
    
    def _show(self, event):
        """Show tooltip."""
        self.deiconify()
        self._move(event)
    
    def _hide(self, event):
        """Hide tooltip."""
        self.withdraw()
    
    def _move(self, event):
        """Move tooltip to cursor position."""
        x = event.x_root + 10
        y = event.y_root + 10
        self.geometry(f"+{x}+{y}")


def add_tooltip(widget, text: str):
    """Add a tooltip to a widget."""
    return Tooltip(widget, text)


