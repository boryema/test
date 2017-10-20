import mechanize



br = mechanize.Browser()
br.open('http://127.0.0.1:8000/travelagent/conversation')
br.set_handle_robots(False) # ignore robots

response = br.response()

#Select a form
br.select_form('forvirtual')
br.set_all_readonly(False)
#Filling in the fields of the form
br.form['message'] = "CESLeA"
# br.form['track'] = ""
# br.form['called'] = ""

br.submit(id = "send")