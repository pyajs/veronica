set data_dir = "/home/w4n9/Code/Github/veronica/xql";

load csv.`{data_dir}/test.csv` as temp1;

select split(_c0," ") as words from temp1 as temp2;

-- train temp2 as word2vec.`{data_dir}/model` where inputCol="words" and minCount="2";

register word2vec.`{data_dir}/model` as w2v_predict;

select words[0] as w, w2v_predict(words[0]) as v from temp2 as result1;

select words as w, w2v_predict_array(words) as v from temp2 as result2;

select words[0] as w, w2v_predict_find(words[0], 3) as v from temp2 as result3;
