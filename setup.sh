#!/bin/sh

init_db()
{
    if [ ! -d "migrations" ]; then
        echo "Initialize db"
        python manage.py db init;
        python manage.py db migrate -m "init db";
        python manage.py db upgrade;
    else
        echo "Cant setup the Migrations folders exists"
    fi
}

manual(){
    echo "Manual"
    echo "      --db : To initialize the database"
    echo "      --help : To see the manual"
}

execute(){

case $1 in

    "--db")
        init_db
     ;;
     "--help")
        manual
    ;;
    *)
      echo -e "Unrecognised argument"
      exit 1

esac

}

[[ -z $1 ]] && manual || execute $1

