import storage_h5 as h
h.open_user()
uid,name,team=h.log_in("test","pwd")
print uid,name,team
	
