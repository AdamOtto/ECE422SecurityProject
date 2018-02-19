import h5py
import numpy as np
file_name='./serverhdf5/test.hdf5'
private_file="./serverhdf5/private/private.hdf5"
public_file="./serverhdf5/public/private.hdf5"
dt = h5py.special_dtype(vlen=unicode) 
field_type=[('uid','<i4'),('fid','<i4'),('context',dt)]
def open_private():
	f=h5py.File(private_file,'a')
	return f
def open_public():
	f=h5py.File(public_file,'a')
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
		if (fid in userdata['fid']):
			index=np.where((data['uid']==uid)&(data['fid']==fid))[0][0]
			data[index]=newdata
		else:
			data=np.append(data,newdata,axis=0)
	grp["data"].resize(data.shape)
	grp["data"][...]=data
	
	
def initial(f):
	initialdata=np.array([(-1,-1,"the initial of hdf5")],dtype=field_type)
	grp=f.create_group("test")
	grp.create_dataset("data",data=initialdata,maxshape=(None,))
	
def read_h5(f,des):
	if des in f:
		grp=f[des]
	else:
		return None
	return np.array(grp["data"])
def create_directory(f,des,loc=None):
	initialdata=np.array([(-1,-1,"the initial of hdf5")],dtype=field_type)
	if loc:
		grp=f[loc]
		sub=grp.create_group(des)
	else:
		sub=f.create_group(des)
	sub.create_dataset("data",data=initialdata,maxshape=(None,))
if __name__ == '__main__':
	f=open_private()
	test=read_h5(f,"test")
	print("test:\n")
	print(test)
	print("\n")
	test=read_h5(f,"test1")
	print("test1:\n")
	print(test)
	print("\n")
	test=read_h5(f,"uid/test/test1")
	print("test/test1:\n")
	print(test)
	print("\n")
	
			
