"""Main application window with modern, professional UI."""
import customtkinter as ctk
from gui.components.navigation import NavigationSidebar
from gui.pages.dashboard import DashboardPage
from gui.pages.matches import MatchesPage
from gui.pages.predictions import PredictionsPage
from gui.pages.statistics import StatisticsPage
from gui.pages.accuracy import AccuracyPage
from gui.pages.tracker import TrackerPage
from gui.pages.settings import SettingsPage
from gui.theme import theme
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FootballPredictorApp(ctk.CTk):
    """Modern, professional football prediction application."""
    
    def __init__(self):
        """Initialize application with industry-level UI."""
        super().__init__()
        
        # Apply modern theme
        self._apply_theme()
        
        # Window configuration
        self.title(f"⚽ {Config.APP_NAME}")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.minsize(Config.MIN_WIDTH, Config.MIN_HEIGHT)
        
        # Center window on screen
        self._center_window()
        
        # Configure grid layout with proper weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create navigation sidebar with modern design
        self.navigation = NavigationSidebar(self, self.navigate_to_page)
        self.navigation.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Create main content frame with modern styling
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=theme.COLORS['bg_primary']
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize pages dictionary
        self.pages = {}
        self.current_page = None
        
        # Create all pages
        self.create_pages()
        
        # Show dashboard by default
        self.show_page("dashboard")
        
        # Bind window events
        self.bind("<Configure>", self._on_window_resize)
        
        logger.info("Modern application initialized successfully")
    
    def _apply_theme(self):
        """Apply modern theme to the application."""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure custom colors
        self.configure(fg_color=theme.COLORS['bg_primary'])
    
    def _center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - Config.WINDOW_WIDTH) // 2
        y = (screen_height - Config.WINDOW_HEIGHT) // 2
        
        # Set position
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{x}+{y}")
    
    def _on_window_resize(self, event):
        """Handle window resize events."""
        if event.widget == self:
            # You can add responsive behavior here if needed
            pass
    
    def create_pages(self):
        """Create all application pages with modern design."""
        try:
            self.pages["dashboard"] = DashboardPage(self.main_frame)
            self.pages["matches"] = MatchesPage(self.main_frame)
            self.pages["predictions"] = PredictionsPage(self.main_frame)
            self.pages["statistics"] = StatisticsPage(self.main_frame)
            self.pages["accuracy"] = AccuracyPage(self.main_frame)
            self.pages["tracker"] = TrackerPage(self.main_frame)
            self.pages["settings"] = SettingsPage(self.main_frame)
            
            logger.info("All pages created successfully")
        except Exception as e:
            logger.error(f"Error creating pages: {e}")
            raise
    
    def show_page(self, page_name: str):
        """
        Show a specific page with smooth transition.
        
        Args:
            page_name: Name of the page to show
        """
        # Hide all pages
        for page in self.pages.values():
            page.grid_forget()
        
        # Show selected page
        if page_name in self.pages:
            self.pages[page_name].grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
            
            # Refresh page data
            try:
                self.pages[page_name].refresh()
            except Exception as e:
                logger.error(f"Error refreshing page {page_name}: {e}")
            
            self.current_page = page_name
            logger.info(f"Navigated to page: {page_name}")
        else:
            logger.warning(f"Page not found: {page_name}")
    
    def navigate_to_page(self, page_name: str):
        """
        Navigate to a page (callback for navigation).
        
        Args:
            page_name: Name of the page to navigate to
        """
        self.show_page(page_name)
    
    def run(self):
        """Run the application."""
        self.mainloop()
