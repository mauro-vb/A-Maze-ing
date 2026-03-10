import sys

def extract_config() -> dict:
    try:
        config: dict = {}
        with open(sys.argv[1], 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                key, value = line.split('=')
                config[key] = value
        return config
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
