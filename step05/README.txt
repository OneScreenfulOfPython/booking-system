This is a very simple refactor. The functions which queried the database
have obvious commonality, so I've pulled out the common material and
parameterised it.

The end result should be exactly the same, because refactoring should
reorganise the codebase without affecting the functionality or API.