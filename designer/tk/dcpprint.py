import dataclasses
import pprint


def dcppformat(x, indent=0):
    def parts():
        if dataclasses.is_dataclass(x):
            yield type(x).__name__ + "("

            def fields():
                for field in dataclasses.fields(x):
                    nindent = indent + len(field.name) + 4
                    value = getattr(x, field.name)
                    rep_value = dcppformat(value)
                    yield " " * (indent + 3) + indent_body_chars(
                        "{}={}".format(field.name, rep_value), indent=nindent
                    )

            yield ",\n".join(fields())
            yield " " * indent + ")"
        else:
            yield pprint.pformat(x)

    return "\n".join(parts())


def indent_chars(x, indent=1):
    return "\n".join(" " * indent + p for p in x.split("\n"))


def indent_body_chars(x, indent=4):
    a, *b = x.split("\n")
    if b:
        return a + "\n" + indent_chars("\n".join(b), indent=indent,)
    else:
        return a


def dcpprint(x, indent=4):
    print(dcppformat(x, indent=indent))
