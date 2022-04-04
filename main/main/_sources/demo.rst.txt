Auto-Documentation Demo
=======================

The purpose of this mock website is to demonstrate some options for
automatically generated documentation for a Python (Click-based) CLI tool.

This is in no way final in its form nor function, but it showcases most of the
main features we're experimenting with. In particular this includes:

#. **Versioned pages**: At the top-left you should see the current version of
   the CLI, along with the option to select a version. This is so you can tell
   if you're looking at the documentation for the version you're working with.
   The CLI tool itself will also have a new ``--version`` flag that will show
   its version for this purpose.

   .. note::

      This specific page only exists in the "main" version, so you will not
      find if you switch to previous versions.

#. **Separation into command groups**: The documentation for each group has
   been placed on its own page. This should make it easier to focus on specific
   parts.

#. **Levels of detail**: In the :doc:`/cli-starter` page you will find that it
   is divided into three sections:

   * Title ("starter"): Shows the group name and the short description of what it does.
   * Summary: Shows the Title section along with a summary of the commands with all of
     their short-form help.
   * Details: Shows the Title section along with a full description of all the commands
     along with their parameters and everything.
   
   There is obviously some redundancy here, which stems from how the generation
   program is implemented. It does let you see a high-level overview of the
   commands though, which may be nice. It might be possible to change it so
   that the Title section isn't included in each of the other sections, but
   doing so seems problematic at the time so we have not done it for now.

   Conversely, in the :doc:`/cli-main` page there is only the Details section.
   The aforementioned redundancy is not present there, but there is also no
   short display of the available commands.

#. **Cross-referencing**: Various parts contain links to various other parts.
   This is actually a rather problematic feature and may very well not be
   included in the final product unless it's important enough or we find some
   workaround for the problems it entails.

Please provide any feedback you have -- now is the best time to decide how we
want this documentation to be!

Thank you for taking the time to read this.