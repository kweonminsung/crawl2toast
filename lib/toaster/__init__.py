from lib.toaster.wintoast import ToastNotifier

toaster = ToastNotifier()

def show_toast(title: str, content: str) -> None:
    try:
        toaster.show_toast(content, title, threaded=True)
    except TypeError:
        pass


def show_compressed_toast(title: str, content: str, count: int) -> None:
    try:
        toaster.show_toast(f"{content} 외 {count} 개의 알림이 있습니다.", title, threaded=True)
    except TypeError:
        pass