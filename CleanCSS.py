import sublime
import sublime_plugin

settings = sublime.load_settings("CleanCSS.sublime-settings")



def indentChar():
	#if self.settings.get('translate_tabs_to_spaces'):
	#	return " " * int(self.settings.get('tab_size', 4))
	return '\t'

def flatten(list, join=-1):
	result = list
	if(join != -1):
		result = []
		for item in list:
			result.append(item)
			result.append([join])
		if(len(result)):
			result.pop()
	return [item for sublist in result for item in sublist]


class CssStyle():
	def __init__(self, line, comments):
		self.line = line
		self.comments = comments
		self.category = ''
		self.sortOrder = 0

		cp = self.line.rfind(':')
		if(cp == -1):
			self.attr = self.line
			self.val = ''
		else:
			self.attr = self.line[:cp].rstrip()
			self.val  = self.line[cp+1:].lstrip()

		self.setStyleType()

	def getColonPosition(self):
		pos = self.line.rfind(':');
		if(pos == -1):
			return -1
		return len(self.line[:pos].rstrip())

	def verticalAlign(self, colonPos):
		if(not self.val):
			return
		pad  = colonPos - len(self.attr)
		self.line = self.attr + (pad * ' ') + ' : ' + self.val


	def setStyleType(self):
		categories = settings.get('categories', {})
		for category in categories:
			for index, attrName in enumerate(category["attributes"]):
				if(attrName == self.attr):
					self.category = category["name"]
					self.sortOrder = index

		if(not self.category):
			if(self.attr.startswith('.')):
				self.category = 'mixin'
			elif(self.attr.startswith('@import')):
				self.category = 'import'
			elif(self.attr.startswith('@')):
				self.category = 'variable'
			else:
				self.category = 'other'

	def output(self, indentCount):
		return self.comments + [(indentChar() * indentCount) + self.line]


class CssRule():
	def __init__(self, firstline, lines, comments, indentCount):
		self.leadingComments = comments
		self.tailingComments = []
		self.indentCount = indentCount
		self.rules = []
		self.styles = []
		self.firstline = firstline.strip()
		self.processLines(lines)

	def verticalAlignStyles(self) :
		farthestPos = -1
		for style in self.styles:
			cp = style.getColonPosition()
			if(cp > farthestPos):
				farthestPos = cp

		for style in self.styles:
			style.verticalAlign(farthestPos)

		return



	def extractRule(self, firstline, lines, comments):
		ruleCode = []
		braceCount = 1
		if(firstline.find('}') == -1):
			while len(lines) > 0:
				line = lines[0]
				if '{' in line:
					braceCount += 1
				if '}' in line:
					braceCount -= 1
				ruleCode.append(line)
				lines.pop(0)
				if braceCount == 0:
					break

		self.rules.append(CssRule(firstline, ruleCode, comments, self.indentCount + 1))
		return lines

	def processLines(self, lines):
		commentSlush = []
		inComment = False

		#loop through each line, determine if its a style, rule, or comment
		while len(lines) > 0:
			line = lines.pop(0)

			#comments
			if(inComment and line.find('*/') > -1):
				commentSlush.append(line)
				inComment = False
			elif(inComment):
				commentSlush.append(line)
			elif(line.strip().startswith('//') or (line.find('/*') > -1 and line.find('*/') > -1)): #single line comments
				commentSlush.append(line)
			elif( line.find('/*') > -1):
				commentSlush.append(line)
				inComment = True


			#Blank lines
			elif(not line or line.strip() == '}'):
				continue
			elif('{' in line):
				lines = self.extractRule(line, lines, commentSlush)
				commentSlush = []
			else:
				self.styles.append(CssStyle(line.strip(), commentSlush))
				commentSlush = []

		self.tailingComments = commentSlush

		return


	def output(self):
		result = []
		if(settings.get("vertically_align_selector_property_values")):
			self.verticalAlignStyles()

		spaceStyles = settings.get('add_space_between_categories')
		minStyles   = settings.get('min_styles_to_collaspe')

		#Output Styles
		if(len(self.styles)):
			formattedStyles = []
			categories = settings.get('categories', {})
			for category in categories:
				filtered = [style for style in self.styles if style.category == category["name"]]
				sort = sorted(filtered, key=lambda style:style.sortOrder)
				if(len(sort)):
					formattedStyles.append(flatten([style.output(self.indentCount + 1) for style in sort]))
			if(spaceStyles and minStyles <= len(self.styles)):
				result.append(flatten(formattedStyles, ''))
			else:
				result.append(flatten(formattedStyles))


		#Output Rules
		if(len(self.rules)):
			if(spaceStyles and minStyles <= len(self.rules)):
				result.append(flatten([rule.output() for rule in self.rules], ''))
			else:
				result.append(flatten([rule.output() for rule in self.rules]))

		if(spaceStyles and minStyles <= len(self.styles) + len(self.rules)):
			result = flatten(result,'')
		else:
			result = flatten(result)

		#Output comments and firstline
		result = self.leadingComments + [self.indentCount * indentChar() + self.firstline] + result + self.tailingComments

		#Output closing brace
		if(self.firstline.find('}') == -1):
			result.append(self.indentCount * indentChar() + '}')
		return result





class CleanCssCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.edit = edit
		self.settings = self.view.settings()

		#Get all liens in file
		region = sublime.Region(0, self.view.size())
		lines  = list(map(lambda lineRegion: self.view.substr(lineRegion), self.view.lines(region)))

		result = CssRule('', lines, [], -1).output()
		result.pop()
		self.view.replace(self.edit, region, '\n'.join(result))
		return
