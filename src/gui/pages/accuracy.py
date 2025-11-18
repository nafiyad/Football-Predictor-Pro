"""Modern accuracy and backtesting page."""
import customtkinter as ctk
import tkinter as tk
from datetime import datetime, timedelta
from services.backtest_service import BacktestService
from gui.theme import theme


class AccuracyPage(ctk.CTkScrollableFrame):
    """Modern accuracy page with model performance metrics."""
    
    def __init__(self, parent):
        """Initialize accuracy page."""
        super().__init__(parent, corner_radius=0, fg_color=theme.COLORS['bg_primary'])
        
        self.backtest_service = BacktestService()
        
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
            text="✓ Model Accuracy",
            font=(theme.FONTS['primary'], theme.FONTS['size_4xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary'],
            anchor="w"
        )
        header_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        subtitle_label = ctk.CTkLabel(
            main_container,
            text="Comprehensive backtesting and performance analysis",
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_tertiary'],
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(0, theme.SPACING['xl']))
        
        # Controls card
        controls_card = ctk.CTkFrame(main_container, **theme.get_card_style())
        controls_card.pack(fill="x", pady=(0, theme.SPACING['xl']))
        
        controls_container = ctk.CTkFrame(controls_card, fg_color="transparent")
        controls_container.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Period selector
        period_label = ctk.CTkLabel(
            controls_container,
            text="Backtest Period:",
            font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_medium']),
            text_color=theme.COLORS['text_primary']
        )
        period_label.pack(anchor="w", pady=(0, theme.SPACING['sm']))
        
        period_frame = ctk.CTkFrame(controls_container, fg_color="transparent")
        period_frame.pack(fill="x", pady=(0, theme.SPACING['md']))
        
        self.period_var = tk.StringVar(value="30")
        periods = [
            ("Last 7 Days", "7"),
            ("Last 30 Days", "30"),
            ("Last 90 Days", "90"),
            ("All Time", "all")
        ]
        
        for label, value in periods:
            btn = ctk.CTkRadioButton(
                period_frame,
                text=label,
                variable=self.period_var,
                value=value,
                font=(theme.FONTS['primary'], theme.FONTS['size_base']),
                text_color=theme.COLORS['text_secondary']
            )
            btn.pack(side="left", padx=(0, theme.SPACING['lg']))
        
        # Run backtest button
        run_btn = ctk.CTkButton(
            controls_container,
            text="🔄 Run Backtest",
            command=self._run_backtest,
            **theme.get_button_style('primary'),
            height=45,
            font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_medium'])
        )
        run_btn.pack(fill="x")
        
        # Results container
        self.results_container = ctk.CTkFrame(main_container, fg_color="transparent")
        self.results_container.pack(fill="both", expand=True)
    
    def _run_backtest(self):
        """Run backtest analysis."""
        try:
            # Clear previous results
            for widget in self.results_container.winfo_children():
                widget.destroy()
            
            # Show loading
            loading_label = ctk.CTkLabel(
                self.results_container,
                text="🔄 Running backtest analysis...",
                font=(theme.FONTS['primary'], theme.FONTS['size_lg']),
                text_color=theme.COLORS['text_secondary']
            )
            loading_label.pack(pady=theme.SPACING['xl'])
            self.update()
            
            # Get period
            period = self.period_var.get()
            end_date = datetime.now()
            
            if period == "all":
                # Get earliest match date
                from database.connection import get_session
                from models.database import Match
                session = get_session()
                earliest_match = session.query(Match).order_by(Match.date).first()
                start_date = earliest_match.date if earliest_match else datetime.now() - timedelta(days=365)
                session.close()
            else:
                start_date = datetime.now() - timedelta(days=int(period))
            
            # Run backtest
            results = self.backtest_service.backtest_predictions(start_date=start_date, end_date=end_date)
            
            # Clear loading
            loading_label.destroy()
            
            # Display results
            self._display_results(results)
            
        except Exception as e:
            print(f"Error running backtest: {e}")
            loading_label.configure(text=f"❌ Error: {str(e)}")
    
    def _display_results(self, results: dict):
        """Display backtest results."""
        # Overall accuracy card
        accuracy_card = ctk.CTkFrame(self.results_container, **theme.get_card_style())
        accuracy_card.pack(fill="x", pady=(0, theme.SPACING['lg']))
        
        acc_container = ctk.CTkFrame(accuracy_card, fg_color="transparent")
        acc_container.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
        
        # Title
        title_label = ctk.CTkLabel(
            acc_container,
            text="📊 Overall Performance",
            font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
            text_color=theme.COLORS['text_primary']
        )
        title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
        
        # Metrics grid
        metrics_frame = ctk.CTkFrame(acc_container, fg_color="transparent")
        metrics_frame.pack(fill="x")
        
        for i in range(3):
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        # Total predictions
        self._create_metric_box(
            metrics_frame,
            "Total Predictions",
            str(results.get('total_predictions', 0)),
            0
        )
        
        # Correct predictions
        self._create_metric_box(
            metrics_frame,
            "Correct Predictions",
            str(results.get('correct_predictions', 0)),
            1
        )
        
        # Accuracy
        accuracy = results.get('accuracy', 0) * 100
        color = theme.COLORS['success'] if accuracy >= 50 else theme.COLORS['warning']
        self._create_metric_box(
            metrics_frame,
            "Accuracy",
            f"{accuracy:.1f}%",
            2,
            color
        )
        
        # Market breakdown
        if 'market_accuracy' in results:
            market_card = ctk.CTkFrame(self.results_container, **theme.get_card_style())
            market_card.pack(fill="x")
            
            market_container = ctk.CTkFrame(market_card, fg_color="transparent")
            market_container.pack(fill="x", padx=theme.SPACING['lg'], pady=theme.SPACING['lg'])
            
            title_label = ctk.CTkLabel(
                market_container,
                text="📈 Market Breakdown",
                font=(theme.FONTS['primary'], theme.FONTS['size_xl'], theme.FONTS['weight_bold']),
                text_color=theme.COLORS['text_primary']
            )
            title_label.pack(anchor="w", pady=(0, theme.SPACING['md']))
            
            for market, acc in results['market_accuracy'].items():
                self._create_market_row(market_container, market, acc)
    
    def _create_metric_box(self, parent, label: str, value: str, column: int, color: str = None):
        """Create a metric box."""
        box = ctk.CTkFrame(
            parent,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md']
        )
        box.grid(row=0, column=column, sticky="ew", padx=(0, theme.SPACING['md'] if column < 2 else 0))
        
        value_label = ctk.CTkLabel(
            box,
            text=value,
            font=(theme.FONTS['primary'], theme.FONTS['size_3xl'], theme.FONTS['weight_bold']),
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
    
    def _create_market_row(self, parent, market: str, accuracy: float):
        """Create a market accuracy row."""
        row = ctk.CTkFrame(
            parent,
            fg_color=theme.COLORS['bg_tertiary'],
            corner_radius=theme.RADIUS['md'],
            height=50
        )
        row.pack(fill="x", pady=(0, theme.SPACING['sm']))
        row.pack_propagate(False)
        
        market_label = ctk.CTkLabel(
            row,
            text=market.upper(),
            font=(theme.FONTS['primary'], theme.FONTS['size_base']),
            text_color=theme.COLORS['text_primary']
        )
        market_label.pack(side="left", padx=theme.SPACING['md'])
        
        acc_value = accuracy * 100
        acc_color = theme.COLORS['success'] if acc_value >= 50 else theme.COLORS['warning']
        
        acc_label = ctk.CTkLabel(
            row,
            text=f"{acc_value:.1f}%",
            font=(theme.FONTS['primary'], theme.FONTS['size_base'], theme.FONTS['weight_bold']),
            text_color=acc_color
        )
        acc_label.pack(side="right", padx=theme.SPACING['md'])
    
    def refresh(self):
        """Refresh page."""
        pass  # Backtest runs on demand
