      # Drop existing table when there
     conn<-getCONN(dest_db,dest_user,dest_odbc)
     sqlcmd<-paste0("DROP TABLE IF EXISTS ",dbschema,".",dtINname,";")
     print(try(dbSendUpdate(conn,sqlcmd),TRUE))
#      system(paste0(execsql,dbname," -c ",sqlcmd))
     # Auto-create Database statement for Postgresql
     createstring<-PSQLcreate(dtIN,dtINname,pgmlvl)
     # Create new table in Postgresql
     sqlcmd<-paste0("CREATE TABLE ",dbschema,".",dtINname,"(",createstring,");")
     print(try(dbSendUpdate(conn,sqlcmd),TRUE))
     dbDisconnect(conn)
     # Write dt to .csv of same name
     setwd(DBpath)
     if (file.exists(dtINname)){
       print(paste("(",pgmlvl,")File exists...will delete file: ",dtINname))
       system(paste0("rm ",DBpath,"/",dtINname,"*"))
     }
     if(cleandt) {dtIN<-cleanData(dtIN,pgmlvl)}

     writeCSV(dtIN,dtINname,pgmlvl)
     # Copy the .csv to the new Postgresql Table
#      if(str_trim(remotehost)==localhost_name) {
        conn<-getCONN(dest_db,dest_user,dest_odbc)
        sqlcmd<-paste0("COPY ",dbschema,".",dtINname," FROM '",getwd(),"/",dtINname,".csv' WITH (FORMAT CSV, DELIMITER ',', NULL 'NaN', HEADER)")
        print(try(dbSendUpdate(conn,sqlcmd),TRUE))
        dbDisconnect(conn)
#       } else {
#          syscmd<-paste0("psql -h ",remotehost," -d ",dbname," -U ",dbuser," -p ",remoteport," -c '\\COPY ",dbschema,".",dtINname," FROM '",getwd(),"/",dtINname,".csv' WITH DELIMITER ',', NULL 'NaN', HEADER'")
#          print(try(system(syscmd),TRUE))
#          }
     print(paste0("(",pgmlvl,")Write Table ",nrow(dtIN)," observations with ",ncol(dtIN)," variables to table>> ",dtINname))
     # Table cleanup code--indexes, key constraints