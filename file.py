import json
def file_json(user,team,filename):
	try:
		f=open(filename)
		fname=filename
		data=cry_fdata(f)
		
		to_json={'user':user,'team':team,'fname':fname,'data':data}
		return json.dumps(to_json)
	except:
		return None

def cry_fdata(f):
	return f.read()
def dcry_fname(f):
	return f
def dcry_fdata(f):
	return f
def loads(js):
	d=json.loads(js)
	fname=dcry_fname(d['fname'])
	data=dcry_fdata(d['data'])
	f=open(fname,'w')
	f.write(data)
	
if __name__ == '__main__':
	test=file_json("test","123","test1.txt")
	print(test)
	test2=file_json("test","123","test2.txt")
	print (test2)
	
		
