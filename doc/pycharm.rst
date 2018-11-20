.. _pycharm:

Some Hints for Developing with PyCharm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyCharm is a popular python editor. This is a quickstart guide setting up 
PyCharm for developing sksurgerynditracker.
This assumes you have PyCharm installed and configured to support virtual environments.

1. Start PyCharm
2. Select File > Open
3. Select the project's folder
4. Open in a new window
5. Open Preferences
6. Click on Project: [YourProject] and select Project Interpreter
7. At the right of the Project Interpreterm, click the cog
8. Select Add Local...
9. Select Virtual Environment
10. Choose a location for your virtual environment (for example, [YourHomeFolder]/VirtualEnvs/[YourProjectName])
11. Select a base interpreter (usually the latest version of Python 3).
12. Recommended settings: Do not inherit global site-packages, and do not make available to all projects.
13. Click OK
14. Click on Terminal
15. `pip install tox`
16. `tox`
17. Expand the project
18. Right-click on the Tests folder and choose "Run Unittests in tests". This will create a new configuration for running tests
19. Right-click on sksurgerynditracker and select Run sksurgerynditracker. This will create a new configuration for running the project.
20. Switch between the program and test configurations using the drop-down at the top of the screen, and the green arrow to run or the green bug to debug.

