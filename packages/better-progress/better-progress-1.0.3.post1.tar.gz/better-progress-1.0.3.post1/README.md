# Better-Progress

A progress bar that actually doesn't make assumptions.

This package is heavily inspired by the [progress](https://github.com/verigak/progress/) package. However, unlike progress, this package handles progress bars in a sane and user-friendly way.

## Basic usage
### Progress bars
``` py
from better_progress import Bar

progress_bar = Bar.Bar(max_value)
print(progress_bar)
```

### Fillers
``` py
from better_progress import Filler

filler = Filler.Filler(max_value)
print(filler)
```

### Spinners
``` py
from better_progress import Spinner

#...

spinner = Spinner.Spinner()
while working:
    #...
    spinner.next()
    print(spinner)
```

## Comparisons between progress and better-progress
* Viewing the progress bar
    * Progress: the default behavior is to print out the progress bar to stdout upon iteration. There is no other way to get a string representation of the progress bar.
    * Better-progress: nothing is printed out to stdout. Instead, the user can get a string of the progress bar by simply getting the string representation of any of the classes provided in the library.
* Documentation
    * Progress: No docstrings, documentation in the repository is severely lacking. Many properties are expected to be in kwargs, making it incredibly difficult to read through the source by hand.
    * Better-progress: Docstrings for every module, class, and function. Nothing should come as a surprise to the user. No reliance on kwargs, except where it makes sense. Type hints are also provided for every parameter and function return.
* Usage in your code
    * Progress: Because it automatically prints to stdout, the user needs to work around the library, potentially changing the structure they already have in place.
    * Better-progress: Because this library only tracks state and gives a string upon request, the library can work around the user. The user doesn't need to make any big changes to get the library to work for them.
* Other features
    * Progress has many other features aside from producing a progress bar. It tracks the average time between increments, the elapsed time since starting, and the ETA until completion.
    * Better-progress does not have these features. The philosophy is that this is a package that lets the user create a pretty progress bar, nothing more. If the user wants any of these features, they would be simple enough to include alongside where they use the progress bar.
