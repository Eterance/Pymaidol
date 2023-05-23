-- This template will show you full potential of ProMaid Language.

@{index1 = 0}
@{total = 0}
total2 = @{embed(total2 = 2)}
int((total2+7)/3) = @{embed(int((total2+7)/3))}
{This is a fake code, with no @ at the first}
@@{Use a @ to escape @ (pretty like razor grammar)}
@{for index, item in incontext_samples[:int((total2+7)/3)]}
-- Question {embed(index+1)}
-- Random {embed(item[random_int])}
This is embed @@{embed(item[random_int])}: @{embed(item[random_int])}
-- Random + 20: @{embed(int(data(~.random_int))+20)}
# 注释
#这也是注释
 #这照样是注释

Question (ABS): @{embed(incontext_samples[index1]['interaction'][0]['utterance'])}
Question (REL): @{embed(item["interaction"][0]["utterance"])}      # 这还是注释
Answer: Let's think step by step.
    @{for index2, item2 in interaction}
index == @{embed(index2)}
index1 == @{embed(index1)}
Step @{embed(index2+index1)} Question: @{embed(item2["utterance"])}
Step @{embed(index2-index1)} SQL: @{embed(item2["query"])}
    @{end}
According the analysis above, the final SQL is: @{embed(item["final"]["query"])}
@{index1 += 1}

@{end}
-- Question @{embed(index1+1)}     

Question: @{embed(input)}     
Answer: Let's think step by step.
This is embed (total): @{embed(total)}
@{code}
import abcd


@{end}
