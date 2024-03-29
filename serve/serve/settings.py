"""
Django settings for serve project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import datetime
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0sqax8#0yw19msr9xgir(1+$v-zeb^5de04+cy&#t0)hc3aj7b'

# SECURITY WARNING: don't run with debug turned on in production!
# 原来是True
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ["*"]

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "frontend/dist/"),
# ]




# Application definition

CORS_ALLOW_CREDENTIALS = True  # 解决跨域
CORS_ORIGIN_ALLOW_ALL = True  # 解决跨域
CORS_ALLOW_HEADERS = ("*")  # 解决跨域


TIME_ZONE = 'Asia/Shanghai' # 时区调整中国



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework',
    'django_filters',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'serve.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'serve.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',  # 数据库名字
        'USER': 'root',
        'PASSWORD': '123456789',
        'HOST': '127.0.0.1',  # 那台机器安装了MySQL
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 自定义 JWT Token 认证类
        'api.utils.jwt_customize.TokenAuth',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'USER_ID_FIELD': "id",
    'SIGNING_KEY': SECRET_KEY,
    'JWT_PUBLIC_KEY': SECRET_KEY,
    'JWT_PAYLOAD_HANDLER': "username",
    'JWT_AUTH_HEADER_PREFIX': 'JWT'
}


# STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
# STATIC_URL = 'static/'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')


STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),# 项目默认会有的路径，如果你部署的不仅是前端打包的静态文件，项目目录static文件下还有其他文件，最好不要删
    os.path.join(BASE_DIR, "dist/static"),# 加上这条
]
