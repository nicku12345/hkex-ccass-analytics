from hkex.app import HKEXApp


def create_app(env="DEV"):
    return HKEXApp.CreateApp(env)

if __name__ == "__main__":
    app = create_app()
