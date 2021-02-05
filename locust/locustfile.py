#locust -f locust.py
import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)
    host = "http://localhost:8081"

    @task(3)
    def index_page(self):
        self.client.get("/")
        self.client.get("/?p=1")
        #self.client.get("/?cat=1")
        

    @task
    def view_cat(self):
        #item_id = random.randint(1, 10000)
        #self.client.get(f"/item?id={item_id}", name="/item")
        self.client.get("/?cat=1")

    @task(2)
    def create_post(self):
        post = {
            "title": "Auto Post by Locust.io",
            "status": "draft",
            "content": "This is a automatic post by Locust.io",
            "categories": 5,
            "tags": "1,4,23",
            "date": "2015-05-05T10:00:00", # YYYY-MM-DDTHH:MM:SS
		    "excerpt": "Read this awesome post",
		    "password": "12$45",    
		    "slug": "new-test-post"
        }
        self.client.post("/wp-admin/post.php", post)




    def on_start(self):
        self.client.post("/wp-login.php", {"log":"admin", "pwd":"admin"})
