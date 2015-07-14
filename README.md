CleanCSS is a [Sublime Text 3](http://www.sublimetext.com/3) package for beautifying your CSS. CleanCSS indents all your rules properly, aligns all the values by the colon, and sorts each property into 5 categories within each rule: content, positional, dimensional, appearance, and animation.

## Installation ##

### With Package Control ###

**Recommended install**. If you have the [Package Control](https://sublime.wbond.net/) package installed, you can install CleanCSS from inside Sublime Text itself. Open the Command Palette and select "Package Control: Install Package", then search for CleanCSS and you're done!

## Usage ##

You can clean a css file by accessing the CleanCSS command from the command palette

![](http://i.imgur.com/Ka6lDLR.gif)

or you can bind a key to the `clean_css` command in `Preferences -> Key Bindings - User` for ultra fast cleaning

	{"keys":["f6"], "command" : "clean_css"},

## Configuration ##

You can access the configuration settings by selecting `Preferences -> Package Settings -> CleanCSS`.

- `add_space_between_categories` *(Boolean)* If true, then an empty line will be inserted between categories

- `categories` *(Array)* Contains how CleanCSS should sort and group each CSS property.
