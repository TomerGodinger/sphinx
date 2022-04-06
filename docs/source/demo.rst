Auto-Documentation Demo
=======================

The purpose of this mock website is to demonstrate some options for
automatically generated documentation for a Python (Click-based) CLI tool.

This is in no way final in its form nor function, but it showcases most of the
main features I'm experimenting with. In particular this includes:

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

   In particular, the :doc:`/cli` page represents a command group that has both
   sub-groups as well as commands and options on its own. I'd like to know if the way
   I've presented it is clear or if there are any modifications you think would make it
   better.

#. **Levels of detail**: In the :doc:`/cli-starter` page you will find that the document
   is divided into three sections:

   * *Title ("starter")*: Shows the group name and the short description of what it does.
   * *Summary*: Shows the a summary of the commands with all of their short-form help.
   * *Details*: Shows the full description of all the commands along with their parameters
     and everything.
   
   Conversely, in the :doc:`/cli-main` page there is no short summary of the commands.
   I'd like to know if adding this short summary is desirable or not. It may be possible
   to change the formatting somewhat, add separators like the ones in :doc:`/cli`, if it
   makes it look better.

#. **Cross-referencing**: Various parts contain links to various other parts.
   I've added the ability to link to pretty much anything, but if there's something in
   particular you think could be added here, please let me know.

Please provide any feedback you have -- now is the best time to decide how we
want this documentation to be!

Thank you for taking the time to read this.