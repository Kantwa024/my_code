import firebase_admin

cred_obj = firebase_admin.credentials.Certificate('./search-engine-bb9f1-firebase-adminsdk-c4tzg-617aae3d8e.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': 'https://search-engine-bb9f1-default-rtdb.firebaseio.com/',
	'storageBucket': 'search-engine-bb9f1.appspot.com'
})

