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
def write_h5(f,uid,fid,context):
	data=np.array(f["data"])
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
	f["data"].resize(data.shape)
	f["data"][...]=data
	f.flush()
	
def initial(f):
	initialdata=np.array([(-1,-1,"the initial of hdf5")],dtype=field_type)
	f.create_dataset("data",data=initialdata,maxshape=(None,))
	
def read_h5(f):
	return np.array(f["data"])
if __name__ == '__main__':
	f=open_private()
	write_h5(f,-2,-2,u"write test3")
	test=read_h5(f)
	print(test)
			
