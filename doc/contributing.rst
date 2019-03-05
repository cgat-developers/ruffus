.. _contribute:

============
Contributing
============

Contributions are very much encouraged and we greatly appreciate the time and effort people make to help maintain and support out tools. Every contribution helps, please dont be shy, we dont bite.

You can contribute to the development of our software in a number of different ways:

-------------------
Reporting bug fixes
-------------------

Bugs are annoying and reporting them will help us to fix your issue.

Bugs can be reported using the issue section in `github <https://github.com/cgat-developers/ruffus/issues>`_

When reporting issues, please include:

- Steps in your code/command that led to the bug so it can be reproduced.
- The error message from the log message.
- Any other helpful info, such as the system/cluster engine or version information.

-----------------------------------
Proposing a new feature/enhancement
-----------------------------------

If you wish to contribute a new feature to the CGAT-ruffus repository then the best way is to raise this as an issue and label it as an enhancement in `github <https://github.com/cgat-developers/ruffus/issues>`_

If you propose a new feature then please:

- Explain how your enhancement will work
- Describe as best as you can how you plan to implement this.
- If you dont think you have the necessary skills to implement this on your own then please say and we will try our best to help (or implement this for you). However, please be aware that this is a community developed software and our volunteers have other jobs. Therefore, we may not be able to  work as fast as you hoped.

-----------------------
Pull Request Guidelines
-----------------------

Why not contribute to our project, its a great way of making the project better, your help is always welcome. We follow the fork/pull request `model <https://guides.github.com/activities/forking>`_. To update our documentation, fix bugs or add extra enhancements you will need to create a pull request through github.

To create a pull request perform these steps:

1. Create a github account.
2. Create a personal fork of the project on github.
3. Clone the fork onto your local machine. Your remote repo on github is called ``origin``.
4. Add the orginal repository as a remote called ``upstream``.
5. If you made the fork a while ago then please make sure you ``git pull upstream`` to keep your repository up to date
6. Create a new branch to work on! We usually name our branches with capital first and last followed by a dash and something unique. For example: ``git checkout -b AC-new_doc``.
7. Impliment your fix/enhancement and make sure your code is effectively documented.
8. Our code has tests and these will be ran when a pull request is submitted, however you can run our tests before you make the pull request, we have a number written in the ``ruffus/test/`` directory. To run all test run: `cd ruffus/test && /bin/bash run_all_unit_tests.cmd`.
9. Add or change our documentation in the ``docs/`` directory.
10. Squash all of your commits into a single commit with git `interactive rebase <https://help.github.com/articles/about-git-rebase/>`_.
11. Push your branch to your fork on github ``git push origin``
12. From your fork in github.com, open a pull request in the correct branch.
13. ... This is where someone will review your changes and modify them or approve them ...
14. Once the pull request is approved and merged you can pull the changes from the ``upstream`` to your local repo and delete your branch.

.. note:: Always write your commit messages in the present tense. Your commit messages should describe what the commit does to the code and not what you did to the code.

