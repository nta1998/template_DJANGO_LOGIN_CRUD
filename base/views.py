import json
from .serializers import MyTokenObtainPairSerializer, FacebookSerializer, PostSerializer
from .models import FacebookUsers, Post
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth.models import User
#####
import openai
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

##############################################################################

class LoginWeb:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "pass")
        self.login_button = (By.NAME, "login")

    def enter_email(self, email):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_field)).send_keys(email)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.login_button)).click()

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.post_input = (By.TAG_NAME, "p")
        self.post_field = (By.XPATH, "//span[contains(text(),'your mind')]")
        self.post_button = (By.XPATH,"//span[contains(text(),'Post')]")
        self.post_text = (By.CLASS_NAME, "x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld")
        self.logo = (By.XPATH, "//a[@aria-label='Facebook']")

    def home_page(self):
        WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(self.logo)).click()
    def click_input(self):
        WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(self.post_field)).click()

    def enter_post(self, post):
        WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(self.post_input)).send_keys(post)

    def click_post(self):
        WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable(self.post_button)).click()

    def get_post_text(self):
        return WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(self.post_text)).text()

    def post_message(self, message):
        self.click_input()
        self.enter_post(message)
        self.click_post()
# ---register--


@api_view(['POST'])
def register(request):
    user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password']
    )
    user.is_active = True
    user.is_staff = True
    user.save()
    return Response("new user born")
# ---login--


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# ---full crud for login users--


@permission_classes([IsAuthenticated])
class webactionView(APIView):
    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        def post_m(post, email, password):
            option = Options()
            option.add_argument('--disable-notifications')
            openai.api_key = "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"
            # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=option)
            driver = webdriver.Chrome(chrome_options=option)
            # executable_path=ChromeDriverManager().install(), chrome_options=option)
            user_email = email
            user_password = password
            login_page = LoginWeb(driver)
            driver.get("http://www.facebook.com")
            login_page.login(user_email, user_password)
            home_page = HomePage(driver)
            home_page.home_page()
            home_page.post_message(post)
        msg = request.data["postAi"]
        users = request.data["users"]
        for user in users:
            y= json.loads(user)
            print(y)
            try:
                post_m(msg, y["email"], y["password"])
                return Response("post", status=status.HTTP_201_CREATED)
            except:pass
        return Response("error", status=status.HTTP_400_BAD_REQUEST)
# ---full crud for login users post--

@permission_classes([IsAuthenticated])
class postcrudView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        data = (request.data)
        openai.api_key = "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"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Write me a post about {data["post"]} in {data["line"]} line long ',
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        msg1 = response.choices[0].text
        serializer = PostSerializer(
            data={"post": msg1}, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class usersView(APIView):
    """
    This class handle the CRUD operations for MyModel

    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objec
        """
        user = request.user
        print(user)
        my_model = user.facebookusers_set.all()
        # my_model = facebookUsers.objects.all()
        serializer = FacebookSerializer(my_model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        # usr =request.user
        # print(usr)
        serializer = FacebookSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = FacebookUsers.objects.get(id=id)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
