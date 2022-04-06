import re
import os
from typing import List, Match


BUILDING_DOCS = 'BUILDING_DOCS' in os.environ
"""Set to True when the documents are being built and False when the CLI is run by a user."""


# All the options we allow for formats of references inside docstrings
# NOTICE: THE ORDER HERE MATTERS. The later regexes are included in the former
# ones, so we need to consume the larger ones first
PARSE_REGEXES = [
    r":(?P<reftype>[A-Za-z]+):`\s*(?P<name>[^<`]+)\s+<(?P<path>[^>`]+)>\s*`",
    r":(?P<reftype>[A-Za-z]+):`\s*(?P<path>[^`]+)\s*`",
    r"`\s*(?P<name>[^<`]+)\s+<(?P<path>[^>`]+)>\s*`",
    r"`\s*(?P<path>[^`]+)\s*`",
]

# In order to avoid replacing something we've replaced already, we can't just
# perform the replacements for each regex in PARSE_REGEXES one after the other.
# Therefore, instead, we combine them into a single, large regex, and use that
# for a single search & replace pass.
# However, Python named groups in a regular expression must be unique. You
# can't name two of them the same even if it's impossible for both to be
# present (e.g. "(?P<somename>A)|(?P<somename>B)").
# Therefore we attach an index suffix to each group name when we pack the
# regexes together, and then later we remove them from the matches.
# 
# The final result of pack_regexes(regexes) for three regexes is:
#   (?:modified_regex_0)|(?:modified_regex_1)|(?:modified_regex_2)
# where regexes are modified so that each group name "groupname" for regex #i
# (where i is the index) becomes "groupname_{i}", where "{i}" is the same
# index.
# 
# Note that this function assumes fair play - it *is* possible to break it by
# giving poorly formed regular expressions, so... don't.
def pack_regexes(regexes: List[Match]) -> str:
    """
    Pack multiple regular expressions to a single one that matches one of them.
    
    The matching priority corresponds to the order they are given in the list.
    Each Python named has an index suffixed to it in order to avoid collisions.

    Returns a string representing the packed regular expression.
    """
    
    modified_regexes = []
    for i, regex in enumerate(regexes):
        modified_regex = re.sub(r"\(\?P<([^>]+)>", f"(?P<\\1_{i}>", regex)
        modified_regex = f"(?:{modified_regex})"
        modified_regexes.append(modified_regex)
    
    return "|".join(modified_regexes)


def unpack_regex_groups(match: Match) -> dict:
    """
    Removed index suffixes from group names attached by pack_regexes().
    """
    results = {}
    for name, value in match.groupdict().items():  # type: str, str
        if value is not None:
            name = re.sub(r"(.*)_[0-9]+$", r"\1", name)
            results[name] = value
    
    return results

PARSE_REGEX = pack_regexes(PARSE_REGEXES)
"""Packed regular expression representing all reference format matching options."""


# Replacements we make when building the documentation
DOC_TEMPLATES = {
    # Using :opt: only works for options but produces a link in code formatting
    "opt": ":option:`{name} <{prelast} -{last}>`",
    "ref": ":ref:`{name} <{fullpath}>`",
}
"""Map of reference type to replacement text when building documentation."""
# Replacements we make when running the CLI
CLI_TEMPLATES = {reftype: "{name}" for reftype in DOC_TEMPLATES}
"""Map of reference type to replacement text when running the CLI."""
# The chosen templates to use, based on whether we're building documentation
# or just running the CLI
REF_TEMPLATES = DOC_TEMPLATES if BUILDING_DOCS else CLI_TEMPLATES
"""The active map of reference type to replacement text."""


# Aliases for people's convenience
REFTYPE_ALIASES = {
    "opt": ["option"],
    "ref": ["reference", "grp", "cmd", "env"],
}
for reftype in REFTYPE_ALIASES:
    for alias in REFTYPE_ALIASES[reftype]:
        REF_TEMPLATES[alias] = REF_TEMPLATES[reftype]


def transform_docstring(doc):
    f"""
    Replaces references in a docstring with their proper (CLI/docs) form.

    Given a docstring that contains Click references in one of the following formats:
        :type_of_reference:`Display Name Here <reference_path>`
        :type_of_reference:`reference_path`
        `Display Name Here <reference_path>`
        `reference_path`
    
    Where:
    - type_of_reference is one of the supported types; {', '.join(list(REF_TEMPLATES.keys()))}.
      If not provided - using one of the latter two options - this acts the same as "cli" for the corresponding one
      of the former two options
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

        # Since we packed multiple regexes into a single one and added indices
        # in order to avoid naming collisions, we need to remove those indices
        # in order to be able to treat all the results the same
        groups = unpack_regex_groups(match)

        # If we don't recognize the reference type we leave the text as i is
        reftype = groups.get('reftype', 'ref').lower()
        if reftype in REF_TEMPLATES:
            # If no name is provided use the path for display
            path = groups['path']
            name = groups.get('name', path)

            # Little workaround for displaying "--param" with two dashes
            # instead of an en-dash when using the default parameter path
            # as a name
            if BUILDING_DOCS and 'name' not in groups:
                name = name.replace('--', r'\\\\-\\\\-')
            
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
            fullpath = '-'.join(parts)  # Not using f"{prelast}-{last}" because prelast may be empty

            replacement = REF_TEMPLATES[reftype].format(
                name=name,
                prelast=prelast,
                last=last,
                fullpath=fullpath,
            )

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


# Perform the replacement here - this allows us to use
# "from clickmod import click" and have everything be ready automatically
add_docstring_transformations_to_click()
