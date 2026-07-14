from app import CarAssemblyApp


def main(renderer=None, input_provider=None, delay_fn=None):
    CarAssemblyApp(renderer, input_provider, delay_fn).run()


if __name__ == "__main__":
    main()
