from hkex.app import HKEXApp


def create_app():
    return HKEXApp.CreateApp()

if __name__ == "__main__":
    app = create_app()
