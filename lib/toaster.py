from win10toast import ToastNotifier

toaster = ToastNotifier()

def show_toast(content: str) -> None:
    toaster.show_toast(content, "Test")