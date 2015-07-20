CleanCSS is a [Sublime Text 3](http://www.sublimetext.com/3) package for beautifying your CSS. CleanCSS indents all your rules properly, aligns all the values by the colon, and sorts each property into categories within each rule:

* Imports (for LESS)
* Variables (for LESS)
* Mixins (for LESS)
* Content
* Positional
* Dimensional
* Appearance
* Animation

## Installation ##

CleanCSS is on [Package Control](https://packagecontrol.io/packages/CleanCSS), so just open the Command Palette and select "Package Control: Install Package", then search for CleanCSS and you're done!

## Usage ##

You can clean a css file by accessing the CleanCSS command from the command palette

![](http://i.imgur.com/Ka6lDLR.gif)

or you can bind a key to the `clean_css` command in `Preferences -> Key Bindings - User` for ultra fast cleaning

	{"keys":["f6"], "command" : "clean_css"},

## Configuration ##

You can access the configuration settings by selecting `Preferences -> Package Settings -> CleanCSS`.

- `add_space_between_categories` *(Boolean)* If true, then an empty line will be inserted between categories
- `add_space_between_rules` *(Boolean)* Adds spaces inbetween each css rule.
- `min_styles_to_collaspe` *(Number)* If the rule has equal to or less styles, it won't add the category spacing.
- `vertically_align_selector_property_values` *(Boolean)* If true, will align the colons of each style within each rule
- `categories` *(Array)* Contains how CleanCSS should sort and group each CSS property. Feel free to customize this as you like. Ordering of the properities in here will dictate how the properties are ordered when you clean the file.
