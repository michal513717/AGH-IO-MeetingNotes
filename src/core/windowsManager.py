from pygetwindow import getAllTitles, getWindowsWithTitle

class WindowsManager():

    @staticmethod
    def get_active_windows() -> list[str]:
        return list(filter(None, getAllTitles()))
    
    @staticmethod
    def get_active_meetins_applications() -> list[str]:
        return [app for app in WindowsManager.get_active_windows() if any(meeting in app.lower() for meeting in ['webex', 'google', 'zoom'])]
    
    @staticmethod
    def get_window_rect(title):
        """
        Retrieves the dimensions and position of the specified application window.

        :returns: A dictionary containing the keys 'left', 'top', 'width', and 'height' for the window's dimensions.
        :rtype: dict

        :raises ValueError: If no window with the specified title is found.
        """
        windows = getWindowsWithTitle(title)

        if not windows:
            raise ValueError(f"Window with title '{title}' not found.")

        window = windows[0]
        return {
            'left': window.left,
            'top': window.top,
            'width': window.width,
            'height': window.height
        }
    
    @staticmethod
    def position_window(title, x, y):
        """
        Positions the specified application window at the specified coordinates.

        :param title: The title of the window.
        :param x: The x-coordinate of the window.
        :param y: The y-coordinate of the window.
        """
        try:
            windows = getWindowsWithTitle(title)

            if not windows:
                raise ValueError(f"Window with title '{title}' not found.")

            window = windows[0]
            window.activate()
            window.moveTo(x, y)

        except Exception as e:
            print(f"Error during positioning window: {e}")

    @staticmethod
    def position_window_default(title):
        """
        Positions the specified application window at the default coordinates.

        :param title: The title of the window.
        """
        WindowsManager.position_window(title, 0, 0)

    @staticmethod
    def get_window_rect(title):
        """
        Retrieves the dimensions and position of the specified application window.

        :returns: A dictionary containing the keys 'left', 'top', 'width', and 'height' for the window's dimensions.
        :rtype: dict

        :raises ValueError: If no window with the specified title is found.
        """
        windows = getWindowsWithTitle(title)

        if not windows:
            raise ValueError(f"Window with title '{title}' not found.")

        window = windows[0]
        return {
            'left': window.left,
            'top': window.top,
            'width': window.width,
            'height': window.height
        }