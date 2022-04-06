import re
import os


BUILDING_DOCS = 'BUILDING_DOCS' in os.environ
PARSE_REGEX = r":(?P<reftype>[A-Za-z]+):`\s*(?:(?P<name>[^<`]+)\s+<(?P<path>[^>`]+)>|(?P<onlypath>[^`]+))\s*`"

class ClickModSettings:
    def __init__(self):
        self.html_prefix = ''

clickmod_settings = ClickModSettings()


# Replacements we make when building the documentation
DOC_TEMPLATES = {
    "opt": ":option:`{name} <{prelast} -{last}>`",
    "env": ":ref:`{name} <{fullpath}>`",
    "cmd": ":ref:`{name} <{fullpath}>`",
    "grp": ":ref:`{name} <{fullpath}>`",
    "ref": ":ref:`{name} <{fullpath}>`",
}
# Replacements we make when running the CLI
CLI_TEMPLATES = {reftype: "{name}" for reftype in DOC_TEMPLATES}
# The chosen templates to use, based on whether we're building documentation
# or just running the CLI
REF_TEMPLATES = DOC_TEMPLATES if BUILDING_DOCS else CLI_TEMPLATES

# Aliases for people's convenience
REFTYPE_ALIASES = {
    "opt": ["option"],
    "env": ["envvar"],
    "cmd": ["command"],
    "grp": ["group"],
}
for reftype in REFTYPE_ALIASES:
    for alias in REFTYPE_ALIASES[reftype]:
        REF_TEMPLATES[alias] = REF_TEMPLATES[reftype]


def transform_docstring(doc):
    f"""
    Replaces references in a docstring with their proper (CLI/docs) form.

    Given a docstring that contains Click references in the following format:
        :type_of_reference:`Display Name Here <reference_path>`
    Or:
        :type_of_reference:`reference_path`
    
    Where:
    - type_of_reference is one of the supported types; {', '.join(list(REF_TEMPLATES.keys()))}
    - "Display Name Here" is what the text should read, both in the CLI and in the docs formats (may contain spaces)
    - reference_path is a space-separated list of elements that make up "how to get" to the reference.
      For example, if type_of_reference is a Click option called "tool" for a command called "house" in the category
      "build" (i.e. you might run "build house -tool hammer"), then the path can be:
        build house tool
        build house -tool
        build house --tool
    
    The returned string will replace each reference with text suitable for the
    right form:
    - If we are currently running the CLI (the BUILDING_DOCS environment
      variable is not present), everything but the name will be removed.
    - If we are currently generating documentation (the BUILDING_DOCS
      environment variable is set), the reference will be replaced with text
      suitable for Sphinx and sphinx-click in order to generate a
      cross-reference link in the produced HTML documents.
    """

    pattern = re.compile(PARSE_REGEX)
    
    newdoc = ''  # We will aggregate the final text in this variable
    start = 0  # Current start index for text we take as-is (between matches)

    for match in re.finditer(pattern, doc):
        # end = where the copied text ends (start of match)
        # newstart = where the next copied text starts (end of match)
        end, newstart = match.span()
        newdoc += doc[start:end]

        replacement = ''  # What we will be replacing this reference with

        # If we don't recognize the reference type we leave the text as i is
        reftype = match.group('reftype').lower()
        if reftype in REF_TEMPLATES:
            name = None  # type: str
            path = None  # type: str

            # Check which of the two forms this reference is in (with or
            # without a display name)
            if match.group('name') is not None:
                # With a name, e.g. :option:`My Option <group command -option>`
                name = match.group('name')
                path = match.group('path')
            else:
                # Without a name, e.g. :option:`group command -option`
                # In this case we treat the path as the name as well
                name = match.group('onlypath')
                path = match.group('onlypath')
            
            # This is to let people use all the following paths:
            #   "main order-meat dish"
            #   "main order-meat -dish"
            #   "main order-meat --dish"
            path = path.replace(' --', ' ')
            path = path.replace(' -', ' ')

            # We assume the elements of the path (group, command, option) are
            # separated by whitespace
            parts = path.split()

            # The last element is the name of the actual thing we want to refer
            # to, and everything before it is the "command path" that leads up
            # to it
            prelast = '-'.join(parts[:-1])
            last = parts[-1]
            fullpath = '-'.join(parts)

            # The first element is the group that the reference belongs to
            first = parts[0]

            replacement = REF_TEMPLATES[reftype].format(
                name=name,
                first=first,
                prelast=prelast,
                last=last,
                fullpath=fullpath,
                html_prefix=clickmod_settings.html_prefix)

        else:
            replacement = doc[end:newstart]
        
        # Add the replacement and proceed to the next part
        newdoc += replacement
        start = newstart
    
    # Add the last part of the docstring (past the last replacement) and finish
    newdoc += doc[start:]
    return newdoc
        

def modify_command_decorator(wrapper_gen):
    """
    Inject docstring correction to Click .command() decorators.
    
    You run this on a group_object.command object, e.g.:
        group_object.command = modify_command_decorator(group_object.command)
    """
    
    def modified_wrapper(*args, **kwargs):
        wrapper = wrapper_gen(*args, **kwargs)

        def transformer(*args, **kwargs):
            w = wrapper(*args, **kwargs)
            if w.help is not None:
                w.help = transform_docstring(w.help)
            
            return w
        
        return transformer

    return modified_wrapper


def modify_group_decorator(wrapper_gen):
    """
    Inject docstring correction to Click .group() decorators.
    
    This makes it so all of the group's .command() decorators are modified to
    inject the docstring modifications.
    Since this is a property of the Click module's click object, we only need
    to do this once, and then any command in any group will have its docstrings
    updated to fit the current scenario automatically.
    
    You run this on Click's click.group, e.g.:
        click.group = modify_group_decorator(click.group)
    """
    
    def modified_wrapper(*args, **kwargs):
        wrapper = wrapper_gen(*args, **kwargs)

        def transformer(*args, **kwargs):
            w = wrapper(*args, **kwargs)
            w.command = modify_command_decorator(w.command)
            
            return w
        
        return transformer

    return modified_wrapper


# Utility function to perform the injection without needing to do anything else
import click
def add_docstring_transformations_to_click():
    click.group = modify_group_decorator(click.group)

add_docstring_transformations_to_click()
