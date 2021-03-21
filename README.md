# terminal
Sharing things I like to use in terminal

better_sessions allows you to call terminal commands like clear, ls, and cwd from inside an interactive Python session. To use this file, call it from your.pythonrc file then set your .pythonrc file in your .bash_profile as PYTHONSTARTUP.

I think it's great to alias these scripts in .bash_profile so they can be called like:

alias define="python3 <path>/define_word.py -d"
```
$ define [term]
```
OR
  
alias wiki="python3 <path>/wiki.py -s"
```
$ wiki [term/phrase]
```
Note: Although the wiki script does handle some disambiguation, it's ugly and not perfect.
