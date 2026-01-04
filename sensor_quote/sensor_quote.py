import json
import subprocess
import requests
import os
from datetime import date
from plugins.base_plugin.base_plugin import BasePlugin


class SensorQuote(BasePlugin):
    def __init__(self):
        super().__init__()
        self.zen_quote_api = "https://zenquotes.io/api/random"

    def generate_image(self, settings, device_config):
        """Generate image with sensor data on top and zen quote on bottom"""

        # Display dimensions
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        # Fetch sensor data
        sensor_data = self._fetch_sensor_data(
            settings.get("ssh_host"),
            settings.get("ssh_user"),
            settings.get("json_path")
        )

        # Fetch quote
        quote_data = self._fetch_zen_quote()

        template_params = {
            "sensor_data": sensor_data,
            "quote_data": quote_data,
            "plugin_settings": settings,
            "icon_path": self.get_plugin_dir("icons/11924923.png")
        }

        image = self.render_image(dimensions, "sensor_quote.html", "sensor_quote.css", template_params)

        if not image:
            raise RuntimeError("Failed to take screenshot, please check logs.")
        return image

    # ------------------------------------------------------------
    # DATA FETCHING
    # ------------------------------------------------------------

    def _fetch_sensor_data(self, host, user, json_path):
        if not json_path:
            raise ValueError("JSON path is required")

        if host and user:
            # Fetch data via SSH
            command = [
                "ssh",
                "-o", "StrictHostKeyChecking=no",
                f"{user}@{host}",
                f"cat {json_path}"
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr)

            json_content = result.stdout

        else:
            # Load data from a local file
            try:
                with open(json_path, 'r') as f:
                    json_content = f.read()
            except FileNotFoundError:
                raise RuntimeError(f"Local JSON file not found at: {json_path}")
            except Exception as e:
                raise RuntimeError(f"Error reading local JSON file: {e}")

        data = json.loads(json_content)

        return data

    def _fetch_zen_quote(self):
        today = date.today()
        cache_file = self.get_plugin_dir("quote_cache.json")

        # Try to load from cache
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                try:
                    cached_data = json.load(f)
                    cached_date = date.fromisoformat(cached_data.get("date"))
                    if cached_date == today and "quote" in cached_data and "title" in cached_data["quote"]:
                        return cached_data["quote"]
                except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                    # Invalid cache file, proceed to fetch new quote
                    pass

        # Fetch new quote
        try:
            response = requests.get(
                self.zen_quote_api,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            if data:
                quote = data[0]
            else:
                quote = {"q": "Silence is also an answer.", "a": "Zen"}
        except requests.RequestException:
            quote = {"q": "Silence is also an answer.", "a": "Zen"}

        quote["title"] = f"Quote of the day ({today.strftime('%d/%m/%y')})"

        # Save to cache
        try:
            with open(cache_file, 'w') as f:
                json.dump({"date": today.isoformat(), "quote": quote}, f)
        except IOError:
            # Could not write cache file, but we can still proceed with the fetched quote
            pass

        return quote


    def generate_settings_template(self):
        template = super().generate_settings_template()
        template["style_settings"] = True
        return template
