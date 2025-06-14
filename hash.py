from streamlit_authenticator.utilities.hasher import Hasher

hashed_pw = Hasher(['your-password']).generate()
print(hashed_pw)
