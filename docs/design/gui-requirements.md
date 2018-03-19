# GUI Requirements (not implementation decisions)

Landing View is Experiment View (single experiment)
- Prominent display of which one you are looking at
- Way to switch to different one by picking from a list of those in the 
  database.
- With filtering based on experiment name to reduce the choices.
- Save-as new name (essentially a copy)

Experiment View Main Needs
- Show the rules script in a text editor
- Make it clear you are supposed to edit the script
- Make it very obvious when there are syntax errors and help the user deal with
  them. (more later)
- Provide a way to see help/example material - taking up very little screen 
  space when quiescent.
- Some way of interactively selecting a block of rules and seeing, on a
  grid-like visualisation which cells, they collectively target. (more later)
- Automated save-as you type to the database.

Navigation links to auxilliary stuff (and back from)
- Edit the acceptable reagent names in the database
- Edit the pools available; pool name and list of reagents+conc

Feedback during editing - auto completion
- When you are typing in a reagent name or a units string, be offered
  autocompletion choices based on the known reagent names.
- Preferably without losing your typing context in the editor, or clicking
  somewhere away from the editor pane.
- Preferably being able to see all the choices available to you at the same
  time rather than having to navigate through them to see them
- Clear feedback when there are no legal autocompletion choices available
- Clear feedback when there are too many to be practical

Feedback during editing - syntax errors
- Provide feedback automatically whenever the user stops typing for 1 or 2
  seconds. (Their pause is what triggers it).
- Have discrete feedback when this is being fetched
- Describe the first problem encountered in the script only.
- Describe it with a comprehensive English message that includes the line
  number and position in the line of the problem
- Highlight (conspicuously) where the error occurs inside the editor 

Feedback during editing - effect of rules / results
- Only available when there are no errors in the script - show some apology to
  this effect in place of the visualisation when so.
- One or both of these mechanisms will exist:
- 1) When the user hovers over a rule, the grid-like visualisation will
  indicate which cells are targeted.
- 2) There will be some convenient way for the user to select one or more rows of
  text in the script editor.  In response the grid-like visualisation 
  described earlier will show which cells are thus targeted.

Organising text into aligned columns
- The editor will display the text using a mono-spaced font, so that it becomes
  feasible for the fields to be arranged neatly in columns by introducing
  suitable numbers of spaces between fields.
- The editor gui will offer an auto-align feature that will reformat the
  incumbent text thus.

Which things must be visible simultaneously?
- The script
- The grid-like visualisation
- The controls to switch or save-as an experiment
- The controls to access the auxilliary functions mentioned above

Auxilliary - Allowed Reagents and Primer Pools
- When you opt to use one of these auxilliary functions, the main area of the
  gui will switch from displaying the main xperiment view to display a view
  dedicated to this new function instead.
- Just what you can do in these views is tbd.

Overall aesthetic
- The GUI should show clearly what it is and what it is for.
- This likely means a concspicuous Jumbotron or such like, and some sense of
  some stuff being in the title / banner area, with other stuff not.
- The screen real estate should be partitioned to match the needs of each area.
- Colours should not be chosen arbitrarily, nor explicitly. Assuming that we are
  using Bootstrap CSS - use functional colour constants like WARNING, SELECTED,
  INFO etc. This makes sure things remain consistent and we don't end up with 
  an arbitrary colour riot.

Network communication failure
- If the GUI encounters problems behind the scenes when trying to connect to
  the back-end API web service, it should alert the user to this fact but
  attempt to resume.
