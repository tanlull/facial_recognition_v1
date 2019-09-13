select * from image 

select *from profile


select create_date,i.*
from image i,profile p
where i.id = p.ba
order by create_date desc


truncate  table image

truncate table profile

