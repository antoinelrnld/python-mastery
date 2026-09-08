def print_table(objects: list[object], attr_names: list[str]):
    print(('%10s ' * len(attr_names) % tuple(attr_names)).rstrip())
    print(('---------- ' * len(attr_names)).rstrip())
    for o in objects:
        values = tuple(getattr(o, attr) for attr in attr_names)
        print(('%10s ' * len(attr_names) % values).rstrip())
