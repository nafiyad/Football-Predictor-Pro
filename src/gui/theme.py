"""
Professional theme configuration for the football prediction app.
Industry-standard design system with modern colors, typography, and spacing.
"""

from typing import Dict, Any


class ModernTheme:
    """Modern, professional theme with industry-standard design."""
    
    # Color Palette - Professional Dark Theme
    COLORS = {
        # Primary Colors
        'primary': '#3B82F6',           # Bright Blue
        'primary_hover': '#2563EB',     # Darker Blue
        'primary_light': '#60A5FA',     # Light Blue
        'primary_dark': '#1E40AF',      # Deep Blue
        
        # Secondary Colors
        'secondary': '#8B5CF6',         # Purple
        'secondary_hover': '#7C3AED',   # Darker Purple
        'accent': '#10B981',            # Green
        'accent_hover': '#059669',      # Darker Green
        
        # Success/Warning/Error
        'success': '#10B981',           # Green
        'warning': '#F59E0B',           # Orange
        'error': '#EF4444',             # Red
        'info': '#3B82F6',              # Blue
        
        # Background Colors
        'bg_primary': '#0F172A',        # Very Dark Blue
        'bg_secondary': '#1E293B',      # Dark Blue-Gray
        'bg_tertiary': '#334155',       # Medium Blue-Gray
        'bg_card': '#1E293B',           # Card Background
        'bg_hover': '#334155',          # Hover State
        
        # Text Colors
        'text_primary': '#F8FAFC',      # Almost White
        'text_secondary': '#CBD5E1',    # Light Gray
        'text_tertiary': '#94A3B8',     # Medium Gray
        'text_disabled': '#64748B',     # Dark Gray
        
        # Border Colors
        'border': '#334155',            # Medium Blue-Gray
        'border_light': '#475569',      # Lighter Border
        'border_focus': '#3B82F6',      # Focus Border
        
        # Prediction Colors
        'win': '#10B981',               # Green
        'draw': '#F59E0B',              # Orange
        'loss': '#EF4444',              # Red
        
        # Chart Colors
        'chart_1': '#3B82F6',           # Blue
        'chart_2': '#8B5CF6',           # Purple
        'chart_3': '#10B981',           # Green
        'chart_4': '#F59E0B',           # Orange
        'chart_5': '#EF4444',           # Red
        'chart_6': '#06B6D4',           # Cyan
    }
    
    # Typography
    FONTS = {
        'primary': 'Segoe UI',
        'secondary': 'Arial',
        'monospace': 'Consolas',
        
        # Font Sizes
        'size_xs': 11,
        'size_sm': 12,
        'size_base': 14,
        'size_lg': 16,
        'size_xl': 18,
        'size_2xl': 24,
        'size_3xl': 30,
        'size_4xl': 36,
        
        # Font Weights
        'weight_normal': 'normal',
        'weight_medium': 'bold',
        'weight_bold': 'bold',
    }
    
    # Spacing System (8px base)
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        '2xl': 48,
        '3xl': 64,
    }
    
    # Border Radius
    RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16,
        'full': 999,
    }
    
    # Shadows
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
    }
    
    # Animation Durations (milliseconds)
    ANIMATION = {
        'fast': 150,
        'normal': 250,
        'slow': 350,
    }
    
    @classmethod
    def get_button_style(cls, variant: str = 'primary') -> Dict[str, Any]:
        """Get button style configuration."""
        styles = {
            'primary': {
                'fg_color': cls.COLORS['primary'],
                'hover_color': cls.COLORS['primary_hover'],
                'text_color': cls.COLORS['text_primary'],
                'corner_radius': cls.RADIUS['md'],
                'border_width': 0,
            },
            'secondary': {
                'fg_color': cls.COLORS['bg_tertiary'],
                'hover_color': cls.COLORS['bg_hover'],
                'text_color': cls.COLORS['text_primary'],
                'corner_radius': cls.RADIUS['md'],
                'border_width': 0,
            },
            'success': {
                'fg_color': cls.COLORS['success'],
                'hover_color': cls.COLORS['accent_hover'],
                'text_color': cls.COLORS['text_primary'],
                'corner_radius': cls.RADIUS['md'],
                'border_width': 0,
            },
            'outline': {
                'fg_color': 'transparent',
                'hover_color': cls.COLORS['bg_hover'],
                'text_color': cls.COLORS['text_primary'],
                'corner_radius': cls.RADIUS['md'],
                'border_width': 2,
                'border_color': cls.COLORS['border'],
            },
        }
        return styles.get(variant, styles['primary'])
    
    @classmethod
    def get_card_style(cls) -> Dict[str, Any]:
        """Get card style configuration."""
        return {
            'fg_color': cls.COLORS['bg_card'],
            'corner_radius': cls.RADIUS['lg'],
            'border_width': 1,
            'border_color': cls.COLORS['border'],
        }
    
    @classmethod
    def get_input_style(cls) -> Dict[str, Any]:
        """Get input field style configuration."""
        return {
            'fg_color': cls.COLORS['bg_tertiary'],
            'border_color': cls.COLORS['border'],
            'text_color': cls.COLORS['text_primary'],
            'corner_radius': cls.RADIUS['md'],
            'border_width': 1,
        }


# Export theme instance
theme = ModernTheme()


