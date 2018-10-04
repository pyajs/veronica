load json.`/home/w4n9/Code/Github/veronica/xql/test.json` as temp1;

select * from temp1 where id=1 as temp2;

save overwrite temp2 as json.`/home/w4n9/Code/Github/veronica/xql/data.json`;

