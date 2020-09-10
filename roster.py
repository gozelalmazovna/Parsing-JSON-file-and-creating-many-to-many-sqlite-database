#Parsing json file and creating many to many sqlite database

#Import libs
import sqlite3
import json

#Create database
conn = sqlite3.connect("rosterdb.sqlite")
cur = conn.cursor()

#Create new tables
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT UNIQUE);

CREATE TABLE Course(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT UNIQUE);

CREATE TABLE Member(
user_id INTEGER,
course_id INTEGER,
role INTEGER,
PRIMARY KEY(user_id,course_id));
''')

#Read json file
fname=input("Enter file name:")
fhand=open(fname).read()
js = json.loads(fhand)

#Insert each data into database
for each in js:
    name = each[0]
    title = each[1]
    role = each[2]

    print(name,title,role)

    cur.execute('''INSERT OR IGNORE INTO User(name)
    VALUES (?)''',(name,))
    cur.execute('''SELECT id FROM User WHERE name = ?''',(name,))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course(title)
    VALUES (?)''',(title,))
    cur.execute('''SELECT id FROM Course WHERE title = ?''',(title,))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO
    Member(user_id,course_id,role)
    VALUES (?,?,?)''',(user_id,course_id,role))

    conn.commit()

#Select JOIN results and print one example
cur.execute('''SELECT User.name,Member.role,Course.title FROM
User JOIN Member JOIN Course ON Member.user_id = User.id AND
Member.course_id = Course.id''')
print(cur.fetchone())
