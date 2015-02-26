# Debug-Dokku.alt-Mongodb-Flask-Python
My experiences, notes and sample code trying to debug MongoDB Flask Apps in Dokku-alt

Debugging  Dokku-alt / MONGODB / Flask / Python /  
===============================================

I have been trying for about 12 hours to debug my mongodb flask application with virtually no success...
and then it hit me - assume EVERYTHING is broken and work backwards.

I have recorded my experience to assist others including sharing my test code in the hope that it reduces someone else's frustration in debugging similar problems. The internal server error and lack of logging that beyond expectations.

===============================================

**Internal Server Error**

***The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.***

===============================================

NOTE: During this painful process __my favorite command line__ became

```bash
 git add * ; git commit -m "aa"; git push dokku master
```

My Debugging Checklist
-------------------

* [CHECK]  Are my imports were working
* [CHECK]  Is mongodb loaded into dokku
* [CHECK]  Is mongodb linked to my dokku app
* [CHECK]  Is mongodb console for my dokku app working
* [CHECK]  does my dokku environment have an environment variable for MONGODB_URL

* ** [FAIL!]  does dokku user have authorization to connect via MONGODB_URL **


##mongodb appears to be available in dokku

```bash
marchon@modulo:~$ dokku | grep mongodb
    mongodb:console <app> <db>                      Launch console for MongoDB container
    mongodb:create <db>                             Create a MongoDB database
    mongodb:delete <db>                             Delete specified MongoDB database
    mongodb:dump <app> <db> <collection>            Dump database collection in bson for an app
    mongodb:export <app> <db> <collection>          Export database collection for an app
    mongodb:import <app> <db> <collection>          Import database collection for an app
    mongodb:info <app> <db>                         Display application informations
    mongodb:link <app> <db>                         Link database to app
    mongodb:list <app>                              List linked databases
    mongodb:restart                                 Restart MongoDB container (for example to switch image)
    mongodb:unlink <app> <db>                       Unlink database from app
```

##mongodb appears to have a link to my dokku app

```bash
  marchon@modulo:~$ dokku mongodb:list todo
  todo
```
##connecting to the mongodb shell for my app and database works

```bash
  marchon@modulo:~$ dokku mongodb:console todo todo
  MongoDB shell version: 2.4.12
  connecting to: mongodb:27017/todo
  Welcome to the MongoDB shell.
```

##does dokku app instance have mongodb environment variables
mongodb environment for my dokku app appears to have settings for host, port, username, password, and database

```bash
  marchon@modulo:~$ dokku mongodb:info todo todo

  echo "       Host: mongodb"
  echo "       Port: 27017"
  echo "       User: todo"
  echo "       Password: mB09Ma7QMja45Bgc"
  echo "       Database: todo"
  echo
  echo "       MONGODB_URL=mongodb://todo:mB09Ma7QMja45Bgc@mongodb:27017/todo"
```

##do the dokku mongodb instance environment variables appear within the instance at runtime

Checked with - inside of default route execution

```python
      d['URL'] = os.environ['MONGODB_URL']
```

```python
@app.route('/')
def show_all():
   try:
     tasks = db.Task.find()
     return render_template('list.html', tasks=tasks)
   except Exception, e:
     d = {}
     d['Error'] = e.message
     d['URL'] = os.environ['MONGODB_URL']
     return render_template('page_not_found.html',d=d)
```
# [FAIL!]  does dokku user have authorization to connect via MONGODB_URL

commands for this user profile appear to lack authorization
```bash
dokku mongodb:console todo todo
  MongoDB shell version: 2.4.12
  connecting to: mongodb:27017/todo
  Welcome to the MongoDB shell.
  For interactive help, type "help".
  For more comprehensive documentation, see
  	http://docs.mongodb.org/
  Questions? Try the support group
  	http://groups.google.com/group/mongodb-user

    > use todo
    switched to db todo

    > show profile
    Thu Feb 26 08:53:01.577 count failed: { "ok" : 0, "errmsg" : "unauthorized" } at src/mongo/shell/query.js:180

    > show dbs
    Thu Feb 26 08:52:26.084 listDatabases failed:{ "ok" : 0, "errmsg" : "unauthorized" } at src/mongo/shell/mongo.js:46

    > show users
    Thu Feb 26 08:52:37.417 error: { "$err" : "not authorized for query on todo.system.users", "code" : 16550 } at src/mongo/shell/query.js:128

    > show profile
    Thu Feb 26 08:52:48.089 count failed: { "ok" : 0, "errmsg" : "unauthorized" } at src/mongo/shell/query.js:180

    > use todo
    switched to db todo

    > show profile
    Thu Feb 26 08:53:01.577 count failed: { "ok" : 0, "errmsg" : "unauthorized" } at src/mongo/shell/query.js:180

    > show logs
    Thu Feb 26 08:53:14.769 TypeError: Cannot read property 'length' of undefined at src/mongo/shell/utils.js:808

    > use system
    switched to db system
    > show collections
    Thu Feb 26 08:53:54.229 error: {
    	"$err" : "not authorized for query on system.system.namespaces",
    	"code" : 16550
    } at src/mongo/shell/query.js:128
```
