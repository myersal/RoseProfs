-*- coding: utf-8 -*-

#create connection
client = pyorient.OrientDB("localhost", 2424);
session_id = client.connect( "admin", "admin" );
 
#create a databse 
client.db_create( db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY );

#open databse 
client.db_open( DB_Demo, "admin", "admin" );

#create class 
cluster_id = client.command( "create class my_class extends V" );

#create property
cluster_id = client.command( "create property my_class.id Integer" );
cluster_id = client.command( "create property my_class.name String" );

#insert record
client.command("insert into my_class ( 'id','’name' ) values( 1201, 'satish')");