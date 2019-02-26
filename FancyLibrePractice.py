from flask import request, Flask,redirect

app = Flask(__name__)

class Libre(Flask):
	def __init__(self):
		self.components = []
		self.host = "localhost"
		self.port = 8080
		self.loginId = None
		self.loggedIn = False
		self.filled = False
		self.fillings = dict()

thingy = Libre()

@app.route("/",methods=["GET","POST"])
def hello():
	eggs = request.form.get("loginId")
	if len(str(eggs)) >= 6 and eggs.isdigit():
		thingy.loggedIn = True
		thingy.loginId = eggs
		return redirect("/pantry",303)
	else:
		introhtml = []
		introhtml.append("<form method='POST'>")
		introhtml.append('''<body bgcolor="#222222">''')
		introhtml.append('''<p style="color:#17B890;">''')
		introhtml.append('''6-digit-ID''')
		introhtml.append('''</p>''')
		introhtml.append('''<input type="text" name = "loginId"></input>''')
		introhtml.append('''<input type="submit" style="border: none solid #000; background: #0892A5; -moz-border-radius: 0px; -webkit-border-radius: 0px; border-radius: 0px;"></input>''')
		introhtml.append('''</body>''')
		introhtml.append("</form>")
		return "".join(introhtml)
	

@app.route("/pantry", methods=["GET","POST"])
def pantry():
	if None not in [x[0] for x in request.form.values()]:
		thingy.filled = True
	if thingy.filled is True and request.method == 'POST':  # this block is only entered when the form is submitted
		orderedString = []
		orderedString.append('''<body bgcolor="222222">''')
		orderedString.append('''<h1 style="color:#17B890;">''')
		orderedString.append(thingy.loginId)
		orderedString.append('''</h1>''')
		thingy.fillings = request.form
		for key in thingy.fillings.keys():
			orderedString.append('''<h1 style="color:#17B890;">''')
			orderedString.append('''The '''+key+''' value is: '''+thingy.fillings[key].replace("_"," "))
			orderedString.append('''</h1>''')
		orderedString.append('''</body>''')
		return "".join(orderedString)
	finalhtmlbase = []
	finalhtmlbase.append("<form method='POST'>")
	with open("templater.html","r") as f:
		htmlskeleton = [k.strip("\n") for k in f.readlines()]
		for line in htmlskeleton:
			if "<body>" in line:
				line = '''<body bgcolor="222222">'''
			finalhtmlbase.append(line)
			if "<body" in line:
				finalhtmlbase.append("<div class = 'pull-right'>")
				with open("config.txt","r") as p:
					configlines = [k.strip("\n") for k in p.readlines()]
					for elem in configlines:
						item = elem.split(" = ")
						item[1] = item[1].split(",")
						finalhtmlbase.append("<select class='select' required name = "+item[0]+">")
						finalhtmlbase.append("<option value='' disabled selected>")
						finalhtmlbase.append(item[0])
						finalhtmlbase.append("</option>")
						thingy.fillings[item[0]] = None
						for group in item[1]:
							finalhtmlbase.append("<option value = "+group.replace(" ","_")+">")
							finalhtmlbase.append(group)
							finalhtmlbase.append("</option >")
						finalhtmlbase.append("</select>")
				finalhtmlbase.append("<input type='submit' value='Submit'>")
				#finalhtmlbase.append("Submit")
				finalhtmlbase.append("</input>")
				finalhtmlbase.append("</div>")
			# 	finalhtmlbase.append("<div class = 'pull-right'>")
			# 	finalhtmlbase.append('''<canvas id="myCanvas" width=screen.width height="100">''')
			# 	finalhtmlbase.append('''</canvas>''')
			# 	finalhtmlbase.append("</div>")
			# elif "</body>" in line:
			# 	finalhtmlbase.append('''<script>''')
			# 	finalhtmlbase.append('''var canvas = document.getElementById("myCanvas");''')
			# 	finalhtmlbase.append('''var ctx = canvas.getContext("2d");''')
			# 	finalhtmlbase.append('''ctx.fillStyle = "#F4FAFF";''')
			# 	finalhtmlbase.append('''ctx.fillRect(0, 0, 400, 75);''')
			#
			# 	finalhtmlbase.append('''</script>''')
	finalhtmlbase.append("</form>")
	return "".join(finalhtmlbase)

