from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def main():
    return "Bonjour et bienvenu!"


@app.route("/search")
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        return render_template('search_results.html', keyword=keyword)
    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run()
