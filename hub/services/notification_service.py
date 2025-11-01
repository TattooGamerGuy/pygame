"""
Notification service.

Manages in-game notifications, alerts, and messages.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
import time
import uuid


class NotificationPriority(Enum):
    """Notification priority levels."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Notification:
    """Notification data."""
    id: str
    message: str
    priority: NotificationPriority
    title: Optional[str] = None
    duration_ms: Optional[int] = None
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    _dismissed: bool = False
    
    @property
    def is_dismissed(self) -> bool:
        """Check if notification is dismissed."""
        return self._dismissed
    
    def dismiss(self) -> None:
        """Dismiss notification."""
        self._dismissed = True


class NotificationService:
    """Service for managing notifications."""
    
    def __init__(self):
        """Initialize notification service."""
        self._notifications: List[Notification] = []
        self._max_notifications = 5
        self.on_notification_dismissed: Optional[Callable[[str], None]] = None
    
    def show(
        self,
        message: str,
        priority: NotificationPriority = NotificationPriority.INFO,
        title: Optional[str] = None,
        duration_ms: Optional[int] = 3000
    ) -> Notification:
        """
        Show a notification.
        
        Args:
            message: Notification message
            priority: Notification priority
            title: Optional title
            duration_ms: Auto-dismiss duration (None = persistent)
            
        Returns:
            Created notification
        """
        notification = Notification(
            id=str(uuid.uuid4()),
            message=message,
            priority=priority,
            title=title,
            duration_ms=duration_ms
        )
        
        self._notifications.append(notification)
        
        # Limit number of notifications
        while len(self._notifications) > self._max_notifications:
            old_notification = self._notifications.pop(0)
            if self.on_notification_dismissed:
                self.on_notification_dismissed(old_notification.id)
        
        return notification
    
    def dismiss(self, notification_id: str) -> bool:
        """
        Dismiss a notification.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            True if dismissed
        """
        for notification in self._notifications:
            if notification.id == notification_id:
                notification.dismiss()
                self._notifications.remove(notification)
                
                if self.on_notification_dismissed:
                    self.on_notification_dismissed(notification_id)
                
                return True
        return False
    
    def get_active_notifications(self) -> List[Notification]:
        """Get all active notifications."""
        current_time = time.time()
        
        # Remove expired notifications
        active = []
        for notification in self._notifications:
            if notification.is_dismissed:
                continue
            
            if notification.duration_ms:
                elapsed = (current_time - notification.timestamp) * 1000
                if elapsed >= notification.duration_ms:
                    notification.dismiss()
                    if self.on_notification_dismissed:
                        self.on_notification_dismissed(notification.id)
                    continue
            
            active.append(notification)
        
        # Update internal list
        self._notifications = active
        
        return active.copy()
    
    @property
    def queue_size(self) -> int:
        """Get number of active notifications."""
        return len(self.get_active_notifications())
    
    def clear_all(self) -> None:
        """Clear all notifications."""
        for notification in self._notifications:
            notification.dismiss()
            if self.on_notification_dismissed:
                self.on_notification_dismissed(notification.id)
        self._notifications.clear()
    
    def set_max_notifications(self, max_count: int) -> None:
        """Set maximum number of notifications."""
        self._max_notifications = max(1, max_count)

