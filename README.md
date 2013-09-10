CleanCSS is a [Sublime Text 2](http://www.sublimetext.com/2) package for beautifying your CSS. CleanCSS indents all your rules properly, alings all the values by the colon, and sorts each property into 5 categories within each rule: content, positional, dimensional, appearance, and animation.

## Installation ##

### With Package Control ###

**Recommended install**. If you have the [Package Control](https://sublime.wbond.net/) package installed, you can install CleanCSS from inside Sublime Text itself. Open the Command Palette and select "Package Control: Install Package", then search for CleanCSS and you're done!

### Without Package Control ###

Go to your Sublime Text 2 Packages directory and clone the repository using the command below:

    git clone https://github.com/stolksdorf/CleanCSS.git

## Usage ##

You can clean a css file by accessing the CleanCSS command from the command palette

![](http://i.imgur.com/Ka6lDLR.gif)

or you can bind a key to the `clean_css` command in `Preferences -> Key Bindings - User` for ultra fast cleaning

	{"keys":["f6"], "command" : "clean_css"},

## Configuration ##

You can access the configuration settings by selecting `Preferences -> Package Settings -> CleanCSS`.

- `add_space_between_categories` *(Boolean)* If true, then an empty line will be inserted between categories

- `categories` *(Array)* Contains how CleanCSS should sort and group each CSS property.

## Notes ##
**Media queries don't work yet**. I've had some trouble getting them to format properly. I'll be fixing this soon.

