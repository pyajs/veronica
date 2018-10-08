set data_dir = "/home/w4n9/Code/Github/veronica/xql";

load json.`{data_dir}/test.json` as temp1;

select * from temp1 where id=1 as temp2;

save overwrite temp2 as json.`{data_dir}/data.json`;

