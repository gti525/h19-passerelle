#!/bin/sh

init_db()
{
    if [ ! -d "migrations" ]; then
        echo "Initialize db"
        python manage.py db init;
        python manage.py db migrate -m "init db";
        python manage.py db upgrade;
    else
        echo "Cant setup the Migrations folders exists. Run again with --reset_db"
    fi
}

reset_db(){
    echo "Resetting db"
    if [  -d "migrations/" ]; then
        echo "Removing migrations folder"
        rm -rf "migrations/"
    fi


    psql -U postgres -d h19passerelle -c "DROP TABLE IF EXISTS \"user\" CASCADE "
    psql -U postgres -d h19passerelle -c "DROP TABLE IF EXISTS \"merchant\" CASCADE "
    psql -U postgres -d h19passerelle -c "DROP TABLE IF EXISTS \"admin\" CASCADE "
    psql -U postgres -d h19passerelle -c "DROP TABLE IF EXISTS \"transaction\" CASCADE "

    init_db

}
manual(){
    echo "Manual"
    echo "      --db : To initialize the database"
    echo "      --reset_db : To reset the database"
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
    "--reset_db")
        reset_db
    ;;
    *)
      echo -e "Unrecognised argument"
      exit 1

esac

}

[[ -z $1 ]] && manual || execute $1

