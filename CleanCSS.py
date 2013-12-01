import sublime
import sublime_plugin

settings = sublime.load_settings("CleanCSS.sublime-settings")

def colonPad(s, desired_index):
	current_index = s.find(":")
	if 0 > current_index:
		return s
	parts = s.split(":",1)
	ruleName = parts[0].strip()
	colonDist = desired_index - len(ruleName) + 1

	return "".join([
		parts[0].rstrip(),
		" " * colonDist,
		": ",parts[1].lstrip()
	])

def getFarthestColonPos(lines):
	def getRuleNameLength(line):
		index = line.find(":")
		if 0 > index:
			return len(line)
		parts = line.split(":",1)
		return len(parts[0].strip())

	return max(list(map(getRuleNameLength, lines)))




class CleanCssCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.edit = edit
		self.settings = self.view.settings()

		#Iterate over each css rule in the file
		searchPoint = 0
		while True:
			cssRule = self.view.find('\{([^}]*)\}', searchPoint)
			if not cssRule:
				break
			self.formatRegion(cssRule)
			searchPoint = self.view.find('\{([^}]*)\}', searchPoint).end()

		#print "Finished"
		sublime.status_message('CleanCSS: Cleaning finished')

	def indentLine(self, line, indentation):
		if self.settings.get('translate_tabs_to_spaces'):
			return indentation + " " * int(self.settings.get('tab_size', 4)) + line.lstrip()
		return indentation + '\t' + line.lstrip()


	def formatRegion(self, region):
		def regionToLines(region):
			return list(map(lambda lineRegion: self.view.substr(lineRegion), self.view.lines(region)))
		result = []
		region = self.view.line(region)
		lines  = regionToLines(region)

		##grab the first line
		firstLine = lines.pop(0)

		#Jetpack out of there if there's a media rule
		if(firstLine.lstrip().startswith('@')):
			return

		#Get how the rule is currently indented
		ruleIndentation = firstLine.replace(firstLine.lstrip(), '')

		##Handles mutli-line rules
		if lines:
			results = self.extractComments(lines, ruleIndentation)
			result = self.cleanLines(results[0], ruleIndentation)
			result = self.createPartitionedRules(result, results[1])
			result.append(ruleIndentation + '}')

		result = [firstLine] + result
		self.view.replace(self.edit, region, '\n'.join(result))

	def extractComments(self, lines, indentation):
		comments = [self.indentLine('/*', indentation)]
		result = []
		inComments = False
		for line in lines:
			#find an open comment and no close on the same line
			if(line.find('/*')>0 and line.find('*/') < 0 and not inComments):
				parts = line.split('/*')
				if parts[0].strip():
					result.append(parts[0])
				if parts[1].strip():
					comments.append(self.indentLine(parts[1], indentation))
				inComments = True
				continue
			#find an close comment and no open on the same line
			if(line.find('/*')<0 and line.find('*/') > 0 and inComments):
				parts = line.split('*/')
				if parts[0].strip():
					comments.append(parts[0])
				if parts[1].strip():
					result.append(self.indentLine(parts[1], indentation))
				inComments = False
				continue
			if(not inComments):
				result.append(line)
			if(inComments):
				comments.append(line)
		comments.append(self.indentLine('*/', indentation))
		return [result, comments]

	#Takes an array of lines and indents, removes braces, and spaces out the colons
	def cleanLines(self, lines, indentation):
		#Uses the users settings to properly indent the line

		result = []
		for line in lines:
			#Remove any same line ending braces
			line = line.replace('}', '')
			#remove empty lines
			if not line.strip():
				continue
			line = self.indentLine(line, indentation)
			result.append(line)

		if not result:
			return result

		colonIndex = getFarthestColonPos(result)
		return list(map(lambda line:colonPad(line, colonIndex), result))


	def createPartitionedRules(self, lines, comments):
		ruleLists = settings.get('categories', [[]])

		def getLeftOvers(rules, allLines):
			for ruleList in rules:
				allLines = list(filter(lambda line:line not in set(ruleList), allLines))
			return [allLines]

		def filterAndSortRules(lines, ruleList):
			result = []
			for line in lines:
				for ruleIndex, rule in enumerate(ruleList):
					if line[0:line.find(':')].strip() == rule:
						result.append((ruleIndex, line))
						break
			result = sorted(result, key=lambda line: line[0])
			return list(map(lambda line:line[1], result))

		def telescoping_append(ls, val):
			ls.append(val)
			return ls

		def flatten(list):
			return [item for sublist in list for item in sublist]

		def joinArrays(listOfArrs, seperator):
			result = flatten([telescoping_append(temp,seperator) for temp in listOfArrs if temp])
			if(result):
				result.pop()
			return result

		result = [filterAndSortRules(lines,rl) for rl in ruleLists]
		result += getLeftOvers(result, lines)
		if len(comments) > 2:
			result.append(comments)

		rule_count = sum([len(x) for x in result])

		# add spaces between cateogires
		if(settings.get('add_space_between_categories') and
			settings.get('num_rules_to_collaspe') < rule_count):
			return joinArrays(result, '')
		return flatten(result)
