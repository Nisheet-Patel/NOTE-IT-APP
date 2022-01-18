from website import create_app
import json
with open("config.json") as file:
    CONFIG = json.load(file)
file.close()

app = create_app(CONFIG)

if __name__ == "__main__":
    app.run(debug=True)