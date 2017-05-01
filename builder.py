#!/usr/bin/python2

import argparse
import sys
import os
from os import path
import jinja2
import yaml

no_text = ("This part is currently undocumented.\n\n"
           "Help us to make the documentation more complete and add "
           "informations here. \n\n"
           "Check #url for more information!")


# Util ------------------------------------------------------------------------
def relative(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def only_instances(instances):
    return [i["class"] for i in instances]


def ensure_dir(*args):
    ensure = path.join(*args)

    if not path.exists(ensure):
        os.makedirs(ensure)


def save_file(filepath, content):
    print("{:45} [generated]".format(filepath))
    with open(filepath, 'w+') as hdl:
        hdl.seek(0)
        if isinstance(content, list):
            hdl.write("\n".join(content))
        else:
            hdl.write(content)
        hdl.truncate()


def to_yaml(descs):
    if isinstance(descs, basestring):
        return descs
    if isinstance(descs, list) and "__or__" in descs:
        desc = ""
        for d in descs:
            if d == "__or__":
                desc = desc + "\n**Or** ---\n"
                continue
            desc = desc + to_yaml(d)
        return desc
    return yaml.dump(descs, default_flow_style=False, default_style=None)


def text_if(maybe_text, replace=""):
    if maybe_text is None:
        return replace
    return maybe_text


def text_block_if(maybe_text):
    return text_if(maybe_text, no_text)


# generator ------------------------------------------------------------------

def command_vars(command):
    commandline = command.argument_parser().format_help().split("\n")
    help        = text_if(command.help)
    description = text_block_if(command.__doc__)
    name        = command.name[0]

    vars = {
        "name": name,
        "help": help,
        "description": description,
        "commandline": commandline
    }
    return (name, vars)


def generate_commands(loader, mgr, output):
    toc = []

    overview_path = path.join(output, "commands.rst")
    single_path   = lambda n: path.join(output, "commands", n + ".rst")

    overview = loader.get_template("commands.rst.tpl")
    single   = loader.get_template("command.rst.tpl")

    for command in only_instances(mgr.get_commands()):
        (name, vars) = command_vars(command)
        toc.append(path.join("commands", name))

        save_file(single_path(name), single.render(vars))

    save_file(overview_path, overview.render({"toc": toc}))


def attribute_vars(component, attr):
    has_docs    = attr.__doc__ is not None
    description = attr.keys.structure("description")
    example     = text_if(attr.keys.structure("example"), "No example")

    link = ":doc:`/" + "/".join(["components", component, attr.atype]) + "`"

    vars = {
        "has_docs": has_docs,
        "link": link,
        "required": "No",
        "default": text_if(attr.defaults, "No default"),
        "name": attr.atype,
        "key_desc": to_yaml(description).split("\n"),
        "key_example": to_yaml(example).split("\n"),
        "example": text_if(attr.example, None),
        "docs": attr.__doc__
    }
    vars["key_desc_len"] = len(vars["key_desc"])
    vars["key_example_len"] = len(vars["key_example"])

    return (has_docs, vars)


def generate_attribute(component, attr, single, output):
    single_path = path.join(output, attr.atype + ".rst")

    has_docs, vars = attribute_vars(component, attr)

    if has_docs:
        save_file(single_path, single.render(vars))
    return vars


def component_vars(component):
    doc        = text_block_if(component.__doc__)
    short_desc = text_if(component.short_description)

    vars = {
        "name": component.ctype,
        "require_components": component.requires,
        "require_attributes": component.required_attributes,
        "short_desc": short_desc,
        "doc": doc,
        "attrs": [],
    }
    return (component.ctype, vars)


def generate_components(loader, mgr, output):
    toc = []

    docu_path   = path.join(output, "documentation.rst")
    single_path = lambda n: path.join(output, "components", n + ".rst")

    docu   = loader.get_template("documentation.rst.tpl")
    single = loader.get_template("component.rst.tpl")
    attrib = loader.get_template("attribute.rst.tpl")

    for component in only_instances(mgr.get_components()):
        name, vars = component_vars(component)

        attrib_path = path.join(output,"components", name)
        ensure_dir(output, "components", name)

        attributes = only_instances(mgr.get_attributes(component.ctype))
        attributes = sorted(attributes, lambda a, b: a.atype > b.atype)

        for attr in attributes:
            avars = generate_attribute(name, attr, attrib, attrib_path)

            # Add required information
            if attr.atype in component.required_attributes:
                avars["required"] = "Yes"
            vars["attrs"].append(avars)

        toc.append(path.join("components", name))
        save_file(single_path(name), single.render(vars))

    save_file(docu_path, docu.render({"toc": toc}))


# Main ------------------------------------------------------------------------

def cli_options_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", dest="source", required=True,
                        help="Path to xii sources")
    parser.add_argument("-o", "--output", dest="output", required=True,
                        help="Output directory")
    return parser


def main():
    options = cli_options_parser().parse_args()

    # load extension manager from source distribution
    sys.path.append(options.source)
    print("{}".format(sys.path))
    from xii.extension import ExtensionManager

    ext_mgr = ExtensionManager()
    ext_mgr.add_builtin_path()
    ext_mgr.load()

    # prepare jinja environment
    from_file = jinja2.FileSystemLoader(relative("templates"))

    loader = jinja2.Environment(loader=from_file,
                             trim_blocks=True,
                             lstrip_blocks=True,
                             undefined=jinja2.StrictUndefined)
    loader.filters['fill'] = lambda str, len: str.ljust(len)

    generate_commands(loader, ext_mgr, options.output)
    generate_components(loader, ext_mgr, options.output)

if __name__ == "__main__":
    main()
