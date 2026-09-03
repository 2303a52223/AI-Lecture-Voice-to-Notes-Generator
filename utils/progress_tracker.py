"""
Progress Tracker - Utility for tracking and displaying operation progress
"""
import streamlit as st
from typing import Optional, Callable
import time


class ProgressTracker:
    """
    Manages progress tracking for long-running operations.
    Integrates seamlessly with Streamlit's progress, status, and spinner widgets.
    """
    
    def __init__(self):
        """Initialize progress tracker"""
        self.current_progress = 0.0
        self.current_status = ""
        self.start_time = None
    
    @staticmethod
    def create_progress_callback(progress_bar, status_text):
        """
        Create a progress callback function for use with async operations
        
        Args:
            progress_bar: Streamlit progress bar widget
            status_text: Streamlit container for status text
            
        Returns:
            Callable: Callback function that takes (progress_value, status_message)
        """
        def callback(progress: float, message: str = ""):
            """Update progress bar and status"""
            progress = max(0.0, min(1.0, progress))  # Clamp between 0 and 1
            progress_bar.progress(progress)
            if message:
                status_text.write(f"📍 {message}")
            return progress
        
        return callback
    
    @staticmethod
    def show_progress_stage(stage_num: int, total_stages: int, title: str, description: str = ""):
        """
        Display current progress stage in a container
        
        Args:
            stage_num: Current stage number (1-indexed)
            total_stages: Total number of stages
            title: Stage title
            description: Optional stage description
        """
        col1, col2 = st.columns([1, 10])
        with col1:
            st.metric("Stage", f"{stage_num}/{total_stages}")
        with col2:
            st.subheader(title)
            if description:
                st.caption(description)
    
    @staticmethod
    def get_elapsed_time(start_time: float) -> str:
        """
        Calculate and format elapsed time
        
        Args:
            start_time: Start time in seconds (time.time())
            
        Returns:
            str: Formatted elapsed time (e.g., "2m 34s")
        """
        elapsed = int(time.time() - start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    @staticmethod
    def estimate_remaining_time(elapsed: float, progress: float) -> Optional[str]:
        """
        Estimate remaining time based on current progress
        
        Args:
            elapsed: Elapsed time in seconds
            progress: Current progress (0.0-1.0)
            
        Returns:
            str: Estimated remaining time, or None if cannot estimate
        """
        if progress <= 0 or progress >= 1.0:
            return None
        
        total_time = elapsed / progress
        remaining = total_time - elapsed
        
        if remaining <= 0:
            return None
        
        remaining = int(remaining)
        minutes = remaining // 60
        seconds = remaining % 60
        
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    @staticmethod
    def show_processing_steps(steps: dict, current_step: Optional[str] = None):
        """
        Display a list of processing steps with status indicators
        
        Args:
            steps: Dict of {step_name: status} where status is 'pending', 'running', 'complete', 'error'
            current_step: Name of currently executing step
        """
        cols = st.columns([1, 8])
        for step_name, status in steps.items():
            if status == 'complete':
                icon = "✅"
                color = "green"
            elif status == 'running':
                icon = "⏳"
                color = "blue"
            elif status == 'error':
                icon = "❌"
                color = "red"
            else:  # pending
                icon = "⏹️"
                color = "gray"
            
            with cols[0]:
                st.write(icon)
            with cols[1]:
                st.write(f"<span style='color: {color}'>{step_name}</span>", unsafe_allow_html=True)


class ProgressContext:
    """
    Context manager for progress tracking during operations
    Provides visual feedback with progress bar and status updates
    """
    
    def __init__(self, title: str = "Processing...", total_steps: int = 1):
        """
        Initialize progress context
        
        Args:
            title: Title of the operation
            total_steps: Number of steps in the operation
        """
        self.title = title
        self.total_steps = total_steps
        self.current_step = 0
        self.container = None
        self.progress_bar = None
        self.status_text = None
        self.start_time = None
    
    def __enter__(self):
        """Enter context - create progress UI"""
        self.container = st.container()
        
        with self.container:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(self.title)
            with col2:
                st.caption(f"Step 1/{self.total_steps}")
            
            self.progress_bar = st.progress(0)
            self.status_text = st.empty()
        
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - finalize progress"""
        if self.progress_bar:
            self.progress_bar.progress(1.0)
        if self.status_text:
            elapsed = ProgressTracker.get_elapsed_time(self.start_time)
            self.status_text.write(f"✅ Completed in {elapsed}")
        return False
    
    def update(self, step: int, message: str = ""):
        """
        Update progress context
        
        Args:
            step: Current step number (1-indexed)
            message: Status message to display
        """
        self.current_step = step
        progress = min(step / self.total_steps, 0.99)
        
        if self.progress_bar:
            self.progress_bar.progress(progress)
        
        if self.status_text:
            elapsed = ProgressTracker.get_elapsed_time(self.start_time)
            remaining = ProgressTracker.estimate_remaining_time(
                time.time() - self.start_time, 
                progress
            )
            
            status_msg = message if message else f"Step {step}/{self.total_steps}"
            time_msg = f"  |  Elapsed: {elapsed}"
            if remaining:
                time_msg += f"  |  ETA: {remaining}"
            
            self.status_text.write(f"📍 {status_msg}{time_msg}")
    
    def step(self, message: str = ""):
        """Advance to next step"""
        self.update(self.current_step + 1, message)


def show_spinner_with_status(title: str, description: str = ""):
    """
    Streamlit context manager for showing spinner with status text
    
    Usage:
        with show_spinner_with_status("Processing", "Loading model..."):
            # Long operation here
            pass
    """
    import contextlib
    
    @contextlib.contextmanager
    def spinner_context():
        with st.spinner(title):
            if description:
                st.caption(description)
            yield
    
    return spinner_context()
