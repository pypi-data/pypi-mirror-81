class ws_settings:
    # Notification Levels
    NOTIFICATION_LEVEL_INFO = 0
    NOTIFICATION_LEVEL_SUCCESS = 1
    NOTIFICATION_LEVEL_ERROR = 2
    NOTIFICATION_LEVEL_WARNING = 3

    NOTIFICATION_LEVEL_CHOICES = (
        (NOTIFICATION_LEVEL_INFO, 'info'),
        (NOTIFICATION_LEVEL_SUCCESS, 'success'),
        (NOTIFICATION_LEVEL_ERROR, 'error'),
        (NOTIFICATION_LEVEL_WARNING, 'warning'),
    )

    NOTIFICATION_LEVEL_CHOICES_REVERSE = {
        'info': NOTIFICATION_LEVEL_INFO,
        'success': NOTIFICATION_LEVEL_SUCCESS,
        'error': NOTIFICATION_LEVEL_ERROR,
        'warning': NOTIFICATION_LEVEL_WARNING
    }
