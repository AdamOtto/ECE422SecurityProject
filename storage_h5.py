import h5py
import numpy as np
file_name='./serverhdf5/test.hdf5'
private_file="./serverhdf5/private/private.hdf5"
public_file="./serverhdf5/public/public.hdf5"
userdata_file="./serverhdf5/user/data.hdf5"
dt = h5py.special_dtype(vlen=unicode) 
field_type=[('uid','<i4'),('fname',dt),('context',dt)]
user_field=[('uid','<i4'),('name',dt),('pwd',dt),('group',dt)]
def open_private():
	f=h5py.File(private_file,'a')
	return f
def open_public():
	f=h5py.File(public_file,'a')
	return f
def open_user():
	f=h5py.File(userdata_file,'a')
	return f

def write_h5(f,uid,fid,des,context):
	if des in f:
		grp=f[des]
	else:
		return None
	data=np.array(grp["data"])
	userdata=data[data['uid']==uid]
	newdata=np.array([(uid,fid,context)],dtype=field_type)
	if (len(userdata)==0):
		data=np.append(data,newdata,axis=0)
	else:
		if (fid in userdata['fname']):
			index=np.where((data['uid']==uid)&(data['fname']==fid))[0][0]
			data[index]=newdata
		else:
			data=np.append(data,newdata,axis=0)
	grp["data"].resize(data.shape)
	grp["data"][...]=data
	return "success"
	
def initial(f):
	initialdata=np.array([(-1,"-1","the initial of hdf5")],dtype=field_type)
	
	f.create_dataset("data",data=initialdata,maxshape=(None,))
def ub_initial(f):
	initialdata=np.array([(-1,"-1","-1","the initial of hdf5")],dtype=user_field)
	f.create_dataset("data",data=initialdata,maxshape=(None,))
	f.close()
def reg_user(uid,name,pwd,team):
	f=open_user()
	data=f["data"]
	if (uid in data['uid'])and(name in data["name"]):
		return None
	else:
		newdata=np.array([(uid,name,pwd,team)],dtype=user_field)
		data=np.append(data,newdata,axis=0)
		f["data"].resize(data.shape)
		f["data"][...]=data
		f.close()
		return "sucess"
def log_in(user,pwd):
	f=open_user()
	data=f["data"]
	if user in data["name"]:
		index=np.where(data['name']==user)[0][0]
		cons=data[index]
		if cons['pwd'] ==pwd:
			return cons['uid'],cons['name'],cons['group']
		else:
			return None,None,None
	else:
		return None,None,None
def read_h5(f,des):
	if des in f:
		grp=f[des]
	else:
		return None
	return np.array(grp["data"])
def list_h5(f,des):
	a=[]
	if des in f:
		grp=f[des]
	else:
		return None
	for v in grp.values():
		if "/"+des+"/"+'data'== v.name or v.name == "/data":
			for fname in v['fname']:
				a.append(fname)
		else:
			a.append(v.name.replace("/"+des+"/",""))
	return a
	
def create_directory(f,des,loc=None):
	initialdata=np.array([(-1,"-1","the initial of hdf5")],dtype=field_type)
	if loc:
		grp=f[loc]
		if des in grp:
			return None
		sub=grp.create_group(des)
	else:
		if des in f:
			return None
		sub=f.create_group(des)
	sub.create_dataset("data",data=initialdata,maxshape=(None,))
	return "success!"
if __name__ == '__main__':
    f=open_user()
    ub_initial(f)
	
			
