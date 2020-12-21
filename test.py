from plyer.utils import platform
from plyer import notification
def failed():
    notification.notify(
        title='CanvasCal failed to run',
        message='Please run setup.exe',
        app_name='CanvasCal',
        #app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
    )

failed()
