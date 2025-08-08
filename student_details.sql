create table Details(
Student_ID INT NOT NULL,
Student_name varchar(20),
Age INT ,
D0B DATE,
Location Varchar(20),
primary key(Student_ID)
);

select * from Details;

insert into Details values(01 , "Mersheena",21,"2004-06-14","Coimbatore");
insert into Details values(02, "John Edwin" , 21,"2004-05-31" , "Bangalore");
select * from Details;


insert into Details values(03,"Sanjay Immanuvel",22,"2004-03-04","Chennai");
insert into Details values(04,"Angel Baslica",19,"2003-12-13","Mumbai");

select * from Details;