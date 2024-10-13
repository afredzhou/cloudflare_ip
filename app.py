from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def show_iplist():
    with open('iplist.txt', 'r') as f:
        iplist_data = f.read()

    return render_template('templates/iplist.html', iplist_data=iplist_data)


if __name__ == '__main__':
    app.run(debug=True)
