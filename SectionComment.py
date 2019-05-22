import sublime, sublime_plugin
import re, collections

syntax_data = []

def build_comment_data(view, pt):
    shell_vars = view.meta_info("shellVariables", pt)
    if not shell_vars:
        return ([], [])

    # transform the list of dicts into a single dict
    all_vars = {}
    for v in shell_vars:
        if 'name' in v and 'value' in v:
            all_vars[v['name']] = v['value']

    line_comments = []
    block_comments = []

    # transform the dict into a single array of valid comments
    suffixes = [""] + ["_" + str(i) for i in range(1, 10)]
    for suffix in suffixes:
        start = all_vars.setdefault("TM_COMMENT_START" + suffix)
        end = all_vars.setdefault("TM_COMMENT_END" + suffix)
        mode = all_vars.setdefault("TM_COMMENT_MODE" + suffix)
        disable_indent = all_vars.setdefault("TM_COMMENT_DISABLE_INDENT" + suffix)

        if start and end:
            block_comments.append((start, end, disable_indent == 'yes'))
            block_comments.append((start.strip(), end.strip(), disable_indent == 'yes'))
        elif start:
            line_comments.append((start, disable_indent == 'yes'))
            line_comments.append((start.strip(), disable_indent == 'yes'))

    return (line_comments, block_comments)

class SectionCommentCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.edit = edit
		self.view.window().show_input_panel("Please name your section", "", self.on_done, None, None)

	def on_done(self, user_input):
		self.view.run_command("check_syntax", {"user_input": user_input})

class CheckSyntax(sublime_plugin.TextCommand):
	def run(self, edit, user_input):
		for region in self.view.sel():
			global syntax_data
			syntax_data = build_comment_data(self.view, region.begin())
			self.view.run_command("section_comment_insert", {"user_input": user_input})

class SectionCommentInsert(sublime_plugin.TextCommand):
	letters = collections.defaultdict(dict)
	letters['a'][0] = "   ###   "
	letters['a'][1] = "  ## ##  "
	letters['a'][2] = " ##   ## "
	letters['a'][3] = "##     ##"
	letters['a'][4] = "#########"
	letters['a'][5] = "##     ##"
	letters['a'][6] = "##     ##"

	letters['b'][0] = "######## "
	letters['b'][1] = "##     ##"
	letters['b'][2] = "##     ##"
	letters['b'][3] = "######## "
	letters['b'][4] = "##     ##"
	letters['b'][5] = "##     ##"
	letters['b'][6] = "######## "

	letters['c'][0] = " ###### "
	letters['c'][1] = "##    ##"
	letters['c'][2] = "##      "
	letters['c'][3] = "##      "
	letters['c'][4] = "##      "
	letters['c'][5] = "##    ##"
	letters['c'][6] = " ###### "

	letters['d'][0] = "####### "
	letters['d'][1] = "##    ##"
	letters['d'][2] = "##    ##"
	letters['d'][3] = "##    ##"
	letters['d'][4] = "##    ##"
	letters['d'][5] = "##    ##"
	letters['d'][6] = "####### "

	letters['e'][0] = "########"
	letters['e'][1] = "##      "
	letters['e'][2] = "##      "
	letters['e'][3] = "######  "
	letters['e'][4] = "##      "
	letters['e'][5] = "##      "
	letters['e'][6] = "########"

	letters['f'][0] = "########"
	letters['f'][1] = "##      "
	letters['f'][2] = "##      "
	letters['f'][3] = "######  "
	letters['f'][4] = "##      "
	letters['f'][5] = "##      "
	letters['f'][6] = "##      "

	letters['g'][0] = " ###### "
	letters['g'][1] = "##    ##"
	letters['g'][2] = "##      "
	letters['g'][3] = "##  ####"
	letters['g'][4] = "##    ##"
	letters['g'][5] = "##    ##"
	letters['g'][6] = " ###### "

	letters['h'][0] = "##    ##"
	letters['h'][1] = "##    ##"
	letters['h'][2] = "##    ##"
	letters['h'][3] = "########"
	letters['h'][4] = "##    ##"
	letters['h'][5] = "##    ##"
	letters['h'][6] = "##    ##"

	letters['i'][0] = "########"
	letters['i'][1] = "   ##   "
	letters['i'][2] = "   ##   "
	letters['i'][3] = "   ##   "
	letters['i'][4] = "   ##   "
	letters['i'][5] = "   ##   "
	letters['i'][6] = "########"

	letters['j'][0] = "      ##"
	letters['j'][1] = "      ##"
	letters['j'][2] = "      ##"
	letters['j'][3] = "      ##"
	letters['j'][4] = "##    ##"
	letters['j'][5] = "##    ##"
	letters['j'][6] = " ###### "

	letters['k'][0] = "##    ##"
	letters['k'][1] = "##   ## "
	letters['k'][2] = "##  ##  "
	letters['k'][3] = "#####   "
	letters['k'][4] = "##  ##  "
	letters['k'][5] = "##   ## "
	letters['k'][6] = "##    ##"

	letters['l'][0] = "##      "
	letters['l'][1] = "##      "
	letters['l'][2] = "##      "
	letters['l'][3] = "##      "
	letters['l'][4] = "##      "
	letters['l'][5] = "##      "
	letters['l'][6] = "########"

	letters['m'][0] = "##    ##"
	letters['m'][1] = "###  ###"
	letters['m'][2] = "########"
	letters['m'][3] = "## ## ##"
	letters['m'][4] = "##    ##"
	letters['m'][5] = "##    ##"
	letters['m'][6] = "##    ##"

	letters['n'][0] = "##    ##"
	letters['n'][1] = "###   ##"
	letters['n'][2] = "####  ##"
	letters['n'][3] = "## ## ##"
	letters['n'][4] = "##  ####"
	letters['n'][5] = "##   ###"
	letters['n'][6] = "##    ##"

	letters['o'][0] = " ###### "
	letters['o'][1] = "##    ##"
	letters['o'][2] = "##    ##"
	letters['o'][3] = "##    ##"
	letters['o'][4] = "##    ##"
	letters['o'][5] = "##    ##"
	letters['o'][6] = " ###### "

	letters['p'][0] = "####### "
	letters['p'][1] = "##    ##"
	letters['p'][2] = "##    ##"
	letters['p'][3] = "####### "
	letters['p'][4] = "##      "
	letters['p'][5] = "##      "
	letters['p'][6] = "##      "

	letters['q'][0] = " ###### "
	letters['q'][1] = "##    ##"
	letters['q'][2] = "##    ##"
	letters['q'][3] = "##    ##"
	letters['q'][4] = "##  # ##"
	letters['q'][5] = "##   ## "
	letters['q'][6] = " #### ##"

	letters['r'][0] = "####### "
	letters['r'][1] = "##    ##"
	letters['r'][2] = "##    ##"
	letters['r'][3] = "####### "
	letters['r'][4] = "##  ##  "
	letters['r'][5] = "##   ## "
	letters['r'][6] = "##    ##"

	letters['s'][0] = " ###### "
	letters['s'][1] = "##    ##"
	letters['s'][2] = "##      "
	letters['s'][3] = " ###### "
	letters['s'][4] = "      ##"
	letters['s'][5] = "##    ##"
	letters['s'][6] = " ###### "

	letters['t'][0] = "########"
	letters['t'][1] = "   ##   "
	letters['t'][2] = "   ##   "
	letters['t'][3] = "   ##   "
	letters['t'][4] = "   ##   "
	letters['t'][5] = "   ##   "
	letters['t'][6] = "   ##   "

	letters['u'][0] = "##    ##"
	letters['u'][1] = "##    ##"
	letters['u'][2] = "##    ##"
	letters['u'][3] = "##    ##"
	letters['u'][4] = "##    ##"
	letters['u'][5] = "##    ##"
	letters['u'][6] = " ###### "

	letters['v'][0] = "##     ##"
	letters['v'][1] = "##     ##"
	letters['v'][2] = "##     ##"
	letters['v'][3] = "##     ##"
	letters['v'][4] = " ##   ## "
	letters['v'][5] = "  ## ##  "
	letters['v'][6] = "   ###   "

	letters['w'][0] = "##      ##"
	letters['w'][1] = "##  ##  ##"
	letters['w'][2] = "##  ##  ##"
	letters['w'][3] = "##  ##  ##"
	letters['w'][5] = "##  ##  ##"
	letters['w'][4] = "##  ##  ##"
	letters['w'][6] = " ###  ### "

	letters['x'][0] = "##    ##"
	letters['x'][1] = " ##  ## "
	letters['x'][2] = "  ####  "
	letters['x'][3] = "   ##   "
	letters['x'][4] = "  ####  "
	letters['x'][5] = " ##  ## "
	letters['x'][6] = "##    ##"

	letters['y'][0] = "##    ##"
	letters['y'][1] = " ##  ## "
	letters['y'][2] = "  ####  "
	letters['y'][3] = "   ##   "
	letters['y'][4] = "   ##   "
	letters['y'][5] = "   ##   "
	letters['y'][6] = "   ##   "

	letters['z'][0] = "########"
	letters['z'][1] = "     ## "
	letters['z'][2] = "    ##  "
	letters['z'][3] = "   ##   "
	letters['z'][4] = "  ##    "
	letters['z'][5] = " ##     "
	letters['z'][6] = "########"

	letters['0'][0] = "  ####  "
	letters['0'][1] = " ##  ## "
	letters['0'][2] = "##    ##"
	letters['0'][3] = "##    ##"
	letters['0'][4] = "##    ##"
	letters['0'][5] = " ##  ## "
	letters['0'][6] = "  ####  "

	letters['1'][0] = "   ##   "
	letters['1'][1] = " ####   "
	letters['1'][2] = "   ##   "
	letters['1'][3] = "   ##   "
	letters['1'][4] = "   ##   "
	letters['1'][5] = "   ##   "
	letters['1'][6] = "########"

	letters['2'][0] = " ###### "
	letters['2'][1] = "##    ##"
	letters['2'][2] = "      ##"
	letters['2'][3] = " ###### "
	letters['2'][4] = "##      "
	letters['2'][5] = "##      "
	letters['2'][6] = "########"

	letters['3'][0] = " ###### "
	letters['3'][1] = "##    ##"
	letters['3'][2] = "      ##"
	letters['3'][3] = " ###### "
	letters['3'][4] = "      ##"
	letters['3'][5] = "##    ##"
	letters['3'][6] = " ###### "

	letters['4'][0] = "##      "
	letters['4'][1] = "##   ## "
	letters['4'][2] = "##   ## "
	letters['4'][3] = "##   ## "
	letters['4'][4] = "########"
	letters['4'][5] = "     ## "
	letters['4'][6] = "     ## "

	letters['5'][0] = "########"
	letters['5'][1] = "##      "
	letters['5'][2] = "##      "
	letters['5'][3] = "####### "
	letters['5'][4] = "      ##"
	letters['5'][5] = "##    ##"
	letters['5'][6] = " ###### "

	letters['6'][0] = " ###### "
	letters['6'][1] = "##    ##"
	letters['6'][2] = "##      "
	letters['6'][3] = "####### "
	letters['6'][4] = "##    ##"
	letters['6'][5] = "##    ##"
	letters['6'][6] = " ###### "

	letters['7'][0] = "########"
	letters['7'][1] = "##    ##"
	letters['7'][2] = "    ##  "
	letters['7'][3] = "   ##   "
	letters['7'][4] = "  ##    "
	letters['7'][5] = "  ##    "
	letters['7'][6] = "  ##    "

	letters['8'][0] = " ###### "
	letters['8'][1] = "##    ##"
	letters['8'][2] = "##    ##"
	letters['8'][3] = " ###### "
	letters['8'][4] = "##    ##"
	letters['8'][5] = "##    ##"
	letters['8'][6] = " ###### "

	letters['9'][0] = " ###### "
	letters['9'][1] = "##    ##"
	letters['9'][2] = "##    ##"
	letters['9'][3] = " #######"
	letters['9'][4] = "      ##"
	letters['9'][5] = "##    ##"
	letters['9'][6] = " ###### "

	letters['-'][0] = "        "
	letters['-'][1] = "        "
	letters['-'][2] = "        "
	letters['-'][3] = "########"
	letters['-'][4] = "        "
	letters['-'][5] = "        "
	letters['-'][6] = "        "

	letters['+'][0] = "        "
	letters['+'][1] = "   ##   "
	letters['+'][2] = "   ##   "
	letters['+'][3] = "########"
	letters['+'][4] = "   ##   "
	letters['+'][5] = "   ##   "
	letters['+'][6] = "        "

	letters['='][0] = "        "
	letters['='][1] = "        "
	letters['='][2] = "########"
	letters['='][3] = "        "
	letters['='][4] = "########"
	letters['='][5] = "        "
	letters['='][6] = "        "

	letters['_'][0] = "        "
	letters['_'][1] = "        "
	letters['_'][2] = "        "
	letters['_'][3] = "        "
	letters['_'][4] = "        "
	letters['_'][5] = "        "
	letters['_'][6] = "########"

	letters['('][0] = "  ###"
	letters['('][1] = " ##  "
	letters['('][2] = "##   "
	letters['('][3] = "##   "
	letters['('][4] = "##   "
	letters['('][5] = " ##  "
	letters['('][6] = "  ###"

	letters[')'][0] = "###  "
	letters[')'][1] = "  ## "
	letters[')'][2] = "   ##"
	letters[')'][3] = "   ##"
	letters[')'][4] = "   ##"
	letters[')'][5] = "  ## "
	letters[')'][6] = "###  "

	letters['['][0] = "######"
	letters['['][1] = "##    "
	letters['['][2] = "##    "
	letters['['][3] = "##    "
	letters['['][4] = "##    "
	letters['['][5] = "##    "
	letters['['][6] = "######"

	letters[']'][0] = "######"
	letters[']'][1] = "    ##"
	letters[']'][2] = "    ##"
	letters[']'][3] = "    ##"
	letters[']'][4] = "    ##"
	letters[']'][5] = "    ##"
	letters[']'][6] = "######"

	letters['{'][0] = "  ####"
	letters['{'][1] = " ##   "
	letters['{'][2] = " ##   "
	letters['{'][3] = "###   "
	letters['{'][4] = " ##   "
	letters['{'][5] = " ##   "
	letters['{'][6] = "  ####"

	letters['}'][0] = "####  "
	letters['}'][1] = "   ## "
	letters['}'][2] = "   ## "
	letters['}'][3] = "   ###"
	letters['}'][4] = "   ## "
	letters['}'][5] = "   ## "
	letters['}'][6] = "####  "

	letters['|'][0] = " ## "
	letters['|'][1] = " ## "
	letters['|'][2] = " ## "
	letters['|'][3] = " ## "
	letters['|'][4] = " ## "
	letters['|'][5] = " ## "
	letters['|'][6] = " ## "

	letters['!'][0] = "####"
	letters['!'][1] = "####"
	letters['!'][2] = "####"
	letters['!'][3] = " ## "
	letters['!'][4] = "    "
	letters['!'][5] = "####"
	letters['!'][6] = "####"

	letters['?'][0] = " ####### "
	letters['?'][1] = "##     ##"
	letters['?'][2] = "      ## "
	letters['?'][3] = "    ###  "
	letters['?'][4] = "   ##    "
	letters['?'][5] = "         "
	letters['?'][6] = "   ##    "

	letters[','][0] = "    "
	letters[','][1] = "    "
	letters[','][2] = "    "
	letters[','][3] = "####"
	letters[','][4] = "####"
	letters[','][5] = " ## "
	letters[','][6] = "##  "

	letters['.'][0] = "   "
	letters['.'][1] = "   "
	letters['.'][2] = "   "
	letters['.'][3] = "   "
	letters['.'][4] = "   "
	letters['.'][5] = "###"
	letters['.'][6] = "###"

	letters[':'][0] = " ## "
	letters[':'][1] = "####"
	letters[':'][2] = " ## "
	letters[':'][3] = "    "
	letters[':'][4] = " ## "
	letters[':'][5] = "####"
	letters[':'][6] = " ## "

	letters[';'][0] = "####"
	letters[';'][1] = "####"
	letters[';'][2] = "    "
	letters[';'][3] = "####"
	letters[';'][4] = "####"
	letters[';'][5] = " ## "
	letters[';'][6] = "##  "

	letters["'"][0] = "####"
	letters["'"][1] = "####"
	letters["'"][2] = " ## "
	letters["'"][3] = "##  "
	letters["'"][4] = "    "
	letters["'"][5] = "    "
	letters["'"][6] = "    "

	letters['"'][0] = "#### ####"
	letters['"'][1] = "#### ####"
	letters['"'][2] = " ##   ## "
	letters['"'][3] = "         "
	letters['"'][4] = "         "
	letters['"'][5] = "         "
	letters['"'][6] = "         "

	letters['@'][0] = " ####### "
	letters['@'][1] = "##     ##"
	letters['@'][2] = "## ### ##"
	letters['@'][3] = "## ### ##"
	letters['@'][4] = "## ##### "
	letters['@'][5] = "##       "
	letters['@'][6] = " ####### "

	letters['#'][0] = "  ## ##  "
	letters['#'][1] = "  ## ##  "
	letters['#'][2] = "#########"
	letters['#'][3] = "  ## ##  "
	letters['#'][4] = "#########"
	letters['#'][5] = "  ## ##  "
	letters['#'][6] = "  ## ##  "

	letters['$'][0] = " ######## "
	letters['$'][1] = "##  ##  ##"
	letters['$'][2] = "##  ##    "
	letters['$'][3] = " ######## "
	letters['$'][4] = "    ##  ##"
	letters['$'][5] = "##  ##  ##"
	letters['$'][6] = " ######## "

	letters['%'][0] = "#####   ##  "
	letters['%'][1] = "## ##  ##   "
	letters['%'][2] = "##### ##    "
	letters['%'][3] = "     ##     "
	letters['%'][4] = "    ## #####"
	letters['%'][5] = "   ##  ## ##"
	letters['%'][6] = "  ##   #####"

	letters['^'][0] = "  ###  "
	letters['^'][1] = " ## ## "
	letters['^'][2] = "##   ##"
	letters['^'][3] = "       "
	letters['^'][4] = "       "
	letters['^'][5] = "       "
	letters['^'][6] = "       "

	letters['&'][0] = "  ####   "
	letters['&'][1] = " ##  ##  "
	letters['&'][2] = "  ####   "
	letters['&'][3] = " ####    "
	letters['&'][4] = "##  ## ##"
	letters['&'][5] = "##   ##  "
	letters['&'][6] = " ####  ##"

	letters['*'][0] = "         "
	letters['*'][1] = " ##   ## "
	letters['*'][2] = "  ## ##  "
	letters['*'][3] = "#########"
	letters['*'][4] = "  ## ##  "
	letters['*'][5] = " ##   ## "
	letters['*'][6] = "         "

	letters['`'][0] = "####"
	letters['`'][1] = "####"
	letters['`'][2] = " ## "
	letters['`'][3] = "  ##"
	letters['`'][4] = "    "
	letters['`'][5] = "    "
	letters['`'][6] = "    "

	letters['~'][0] = " ####     "
	letters['~'][1] = "##  ##  ##"
	letters['~'][2] = "     #### "
	letters['~'][3] = "          "
	letters['~'][4] = "          "
	letters['~'][5] = "          "
	letters['~'][6] = "          "

	def run(self, edit, user_input):
		plugin_settings_file = "SectionComment.sublime-settings"
		plugin_settings = sublime.load_settings(plugin_settings_file)

		fill_char = plugin_settings.get("fill_char")
		prefer_line_comments = plugin_settings.get("prefer_line_comments")
		letter_spacing = plugin_settings.get("letter_spacing")

		if letter_spacing < 1:
			letter_spacing = 1

		space_size = plugin_settings.get("space_size")

		true_space_size = space_size - (letter_spacing*2)

		if true_space_size < 1:
			true_space_size = 1

		for i in range(7):
			self.letters[' '][i] = " " * true_space_size


		has_line = len(syntax_data[0]) > 0
		has_block = len(syntax_data[1]) > 0

		if(prefer_line_comments and has_line): has_block = 0

		if has_block:
			block_prefix = syntax_data[1][0][0]
			block_suffix = syntax_data[1][0][1]
		elif has_line:
			line_prefix = syntax_data[0][0][0]
		else:
			has_block = True
			block_prefix = "/*"
			block_suffix = "*/"

		available_letters = re.escape(''.join(self.letters.keys()))
		user_input = re.sub(r'[^'+available_letters+']', r'', user_input.lower())
		section_comment = ""

		for line in range(0,7):
			is_first_letter = True
			for char in user_input:
				if not has_block and is_first_letter:
					section_comment += line_prefix
					is_first_letter = False

				ascii_letter = self.letters[char][line].replace('#', fill_char)
				section_comment += ascii_letter + " "*letter_spacing

			if line != 6:
				section_comment += "\n"

		if has_block:
			comment_data = block_prefix + "\n" + section_comment + "\n" + block_suffix
		else:
			comment_data = section_comment

		self.view.insert(edit, self.view.sel()[0].begin(), comment_data)
