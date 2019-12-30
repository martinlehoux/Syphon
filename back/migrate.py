#! ./env/bin/python
from os.path import isdir, isfile, join
from os import mkdir, listdir, environ
import sqlite3

ENV = environ.get('ENV')

def setup():
    print("[   SETUP   ] Begin...")
    if not isdir('migrations'):
        mkdir('migrations')
        print("[   SETUP   ] 'migrations' folder created")
    if not isfile('migrations/history'):
        open('migrations/history', 'w').close()
        print("[  SETUP  ] 'migrations/history' file created")
    print("[   SETUP   ] OK")

def migrate():
    print(f"[  MIGRATE  ] Begin {ENV}.db migration...")
    migrations = [filename for filename in listdir('migrations') if filename.split('.').pop() == 'sql']
    migrations.sort()
    print(f"[  MIGRATE  ] migrations loaded: {len(migrations)}")
    done_migrations = [filename.strip() for filename in open('migrations/history', 'r').readlines()]
    print(f"[  MIGRATE  ] history loaded: {len(done_migrations)}")
    for migration in migrations:
        if migration in done_migrations:
            print(f"\t[x] {migration} already done, passing...")
        else:
            try:
                query = open(join('migrations', migration), 'r').read()
                conn = sqlite3.connect(f"{ENV}.db")
                cursor = conn.cursor()
                cursor.executescript(query)
                conn.commit()
                cursor.close()
                conn.close()
                print(f"\t[x] {migration} migration done !")
                open(join('migrations', 'history'), 'a').write(migration + "\n")
            except sqlite3.Error as err:
                print(f"\t[ ] {migration} migration failed: {err}")


if __name__ == "__main__":
    setup()
    migrate()
