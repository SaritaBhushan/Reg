# SET user_id
user_id=1378

# IMPORT FILES
import hashlib
from django.contrib.auth.models import User
from six import text_type


# SECRET_KEY is the “EDXAPP_EDXAPP_SECRET_KEY” of IITBomayX available in the file “home/edx/my-passwords.yml”.
SECRET_KEY = 'BjTwggREbpe2DnnDi7DwIDq62Evkx74d0JvypPqr9V3QOuPaw7zoranYvrwMm9VMpiKUewN4Kl0sNUCijZgVKHbWaZeQJPLMh5Rl'


user_obj = User.objects.get(id=user_id)
hasher = hashlib.md5()
hasher.update(SECRET_KEY.encode('utf-8'))
hasher.update(text_type(user_obj.id).encode('utf-8'))
anonymous_user_id = hasher.hexdigest()
