from entity import *

class Function:

	def __init__(this, header, params):
		this.header = header
		this.params = params
		this.body = ''

	def __str__(this):
		return this.header+':\n\tparams: '+str(this.params)+'\n\n'+this.body

	def create_instance(this):
		pass

def create_function(name, params, refs, body):
	'''create a new function with a leading path, any number of parameters, a global reference dictionary, and a body'''

	cmds = []
	refs = refs.copy()

	def tokenize(line):
		return line.split(' ')

	def evaluate_command(tokens):

		# assignment
		if tokens[1] == '=':
			refs[name+'_'+tokens[0]] = evaluate_expression(name+'_'+tokens[0], tokens[2:])

		# vanilla command
		else:
			for i in xrange(len(tokens)):
				token = name+'_'+tokens[i]
				if token in refs:
					if refs[token] == None:
						tokens[i] = select_entity(token)
					else:
						tokens[i] = refs[token]

			cmds.append(' '.join(tokens))

	def evaluate_expression(destination, tokens):

		if destination in refs and refs[destination] == None:
			cmds.append(clear_tag(destination))

		if len(tokens) == 1:
			token = name+'_'+tokens[0]
			# entity
			if tokens[0][0] == '@':
				cmds.append('tag %s add %s' % (tokens[0], destination))
				return None

			# ref to entity
			elif token in refs and refs[token] == None:
				cmds.append('tag %s add %s' % (select_entity(token), destination))
				return None

			# ref to constant
			elif token in refs:
				return refs[token]

			# constant
			else:
				return ' '.join(tokens)

		else:
			return ' '.join(tokens)

	# handle params
	for p in params:
		if params[p]:
			refs[name+'_'+p] = None

	# generate body
	for line in body.split('\n'):
		line = line.strip()
		if len(line) == 0: continue
		evaluate_command(tokenize(line))

	f = Function(name, params)
	f.body = '\n'.join(cmds)
	return f