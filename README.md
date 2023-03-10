# **Flask Itea Project**

### What is implemented in this application:

<a name="top"></a>

1. [ ] Minimal templates - &#9989;
2. [ ] Blueprints, package structure - &#9989;
3. [ ] Forms and Validation - &#9989;
4. [ ] Database Peewee - &#9989;
5. [ ] Login and Authentication - &#9989;
6. [ ] User account profile - &#9989;
7. [ ] Posts - &#9989;
8. [ ] Pagination users - &#9989;, pagination posts - &#9989;, pagination user_posts - &#9989;
9. [ ]  Password reset Email - &#10060; / &#9989; <a href="#Email"> _Look at the end of the document_ </a> &#8659;
10. [ ] Error handlers - &#9989;
11.  [ ] Deleting any post with admin rights - &#10060;
12. [ ] Generation of users and posts - &#9989;
13. [ ] Api - &#9989;, examples of requests and responses in the <a href="API.md">API.md</a> file
14. [ ] Weather app - &#9989;
15. [ ] Data generation refactoring - &#9989;
16. [ ] <a href="#Integration_testing"> Integration testing </a> - &#9989;
17. [ ] Unit testing - &#10060; / &#9989;



-------------------------------
---



~~~shell
$ pip install -r requirements.txt
~~~

If not installed, then additionally install:
~~~shell
pip install python-dotenv
~~~

## Run server
~~~shell
flask run
~~~

## Run the app
`python web.py`

-------------------------------
---

Examples: 

![home_page.png](docs%2Fhome_page.png)

![blog_page.png](docs%2Fblog_page.png)

![admin_page.png](docs%2Fadmin_page.png)

![add_city.png](docs%2Fadd_city.png)

![user_cities_weather.png](docs%2Fuser_cities_weather.png)

![user_cities_details.png](docs%2Fuser_cities_details.png)

-------------------------------
---

### Selenium test:
<a name="Integration_testing"></a>

![tests_integration_animation.gif](docs%2Ftests_integration_animation.gif)

-------------------------------
---
-------------------------------
---
## Password recovery error
<a name="Email"></a>

![error email.png](docs%2Ferror%20email.png)


<a href="#top">UP</a>