create table users(
       id integer primary key autoincrement,
       username varchar(200),
       password varchar(MAX),
       permissions int
);


create table trip(
       id integer primary key autoincrement,
       start_time date,
       end_time date,
       no_of_fish integer,
       location varchar(100)
);


create table fish_caught(
       id integer primary key autoincrement,
       trip_id integer,
       fish_type    integer, 
       fish_weight  integer,
       fish_length  integer,
       lure integer 
);

create table lures(
       id integer primary key autoincrement,
       lure_name  varchar(100),
       lure_type  int,
);

create table lure_type(
       id integer primary key autoincrement,
       type varchar(100)
)

create table environment(
       id integer primary key autoincrement,
       /* weather stuff */
)
