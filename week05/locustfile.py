from locust import HttpUser, between, task

STATIC_ASSETS = [
    "/",
    "/sample.html",
    "/style.css",
    "/main.js",
    "/cn_week05_test.png",
]


class User(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def load_index(self):
        self.client.get("/", name="page:/")

    @task(2)
    def load_static_assets(self):
        for asset in STATIC_ASSETS[1:]:
            with self.client.get(
                asset, name=f"static:{asset}", catch_response=True
            ) as resp:
                if resp.status_code >= 400:
                    resp.failure(f"{asset} failed with {resp.status_code}")
