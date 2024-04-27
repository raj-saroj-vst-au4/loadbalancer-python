from flask import Flask
import os
app = Flask(__name__)

osport = port=int(os.environ.get("PORT", 5000))
# Global variable to keep track of the count
route_count = 0


@app.route("/")
def service():
    global route_count
    route_count += 1

    # Write the count to a file
    with open("route_count.txt", "w") as file:
        file.write("Access count: ")
        file.write(str(route_count))
        file.write("\n")

    html = '<html><body><h1>Hello World!</h1><p>Access count: ' + \
            str(route_count) + '</p></body></html>' # + \
            # '<img src="https://media.giphy.com/media/3o7TKz9bX9v6hZ8NSA/giphy.gif">' + \
            # '</body></html>'
    return html

if __name__ == "__main__":
    app.run(debug=True, port=osport)