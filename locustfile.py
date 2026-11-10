#!/usr/bin/env python3
"""
Kitty Corp Locust Enterprise Integration Script
Run with: locust -f locustfile.py --host=https://thekittycorp.com
"""
from locust import HttpUser, task, between
import random

class KittyCorpUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def load_home(self):
        self.client.get("/", headers={"User-Agent": "KittyCorp-Locust/2.0"})

    @task(1)
    def load_assets(self):
        self.client.get("/index.html", headers={"User-Agent": "KittyCorp-Locust/2.0"})
