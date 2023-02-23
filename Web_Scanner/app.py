from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_PORT']=3306
app.config['MYSQL_USER']= @fetched_dynamically
app.config['MYSQL_PASSWORD']= @fetched_dynamically
app.config['MYSQL_DB']='nuclei_scanner'
mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
def scan_target():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        target = request.form['target']

        cur.execute('INSERT INTO scan_info(target) VALUES(%s)',(target,))
        mysql.connection.commit()
    cur.execute('SELECT * FROM scan_info')
    allData = cur.fetchall()
    cur.close()
    return render_template('index.html',allData=allData)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute('SELECT DISTINCT target FROM scan_info')
    allData = cur.fetchall()
    cur.close()
    return render_template('dashboard.html',allData=allData)

@app.route('/subdomains/<string:target>')
def subdomains(target):
    cur = mysql.connection.cursor()
    cur.execute('SELECT subdomain FROM scan_info where target=%s',(target,))
    allData = cur.fetchall()
    cur.close()
    return render_template('subdomains.html',allData=allData)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
