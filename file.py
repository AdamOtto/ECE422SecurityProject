import json
from Crypto.Hash import SHA256
from Crypto.Cipher import ARC2
def file_json(user,team,filename):
	try:
		f=open(filename)
		
		fname=filename
		data=cry_fdata(f,team)
		
		to_json={'user':user,'team':team,'fname':fname,'data':data}
		return to_json
	except:
		return None

def cry_fdata(f,team):
	
	h=SHA256.new()
	h.update(team)
	c=ARC2.new(h.hexdigest(),ARC2.MODE_ECB,"")
	data=f.read()
	
	if (len(data)%8==0):
		to_crypto=data
	else:
		remain=8-len(data)%8
		to_crypto=data+" "*remain
	
	
		
	return c.encrypt(to_crypto)

def dcry_fdata(f,team):
	h=SHA256.new()
	h.update(team)
	c=ARC2.new(h.hexdigest(),ARC2.MODE_ECB,"")
	return c.encrypt(f)
def loads(js):
	d=json.loads(js.decode('b'))
	fname=d['fname']+'1'
	team=d['team']
	data=dcry_fdata(d['data'],team)
	f=open(fname,'w')
	f.write(data)
	
if __name__ == '__main__':
	
	
	
		
